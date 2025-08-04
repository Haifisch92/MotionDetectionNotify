import cv2
import asyncio
from abc import ABC, abstractmethod
from datetime import datetime

class MotionDetection:

    def __init__(self, stream, width = None, height = None, rotation = 0, contour = 3000, tracking = True, create_window = False, queue_size=10):
        self.stream = stream
        self.rotation = rotation
        self.contour = contour
        self.frame_queue = asyncio.Queue(maxsize=queue_size)
        self.cap = None
        self.window = create_window
        self.previous_frame = None
        self.frame = None
        self.motion = False
        self.tracking = tracking
        self.recording = False
        self.out = None
        self.video_filename = None
        self.running = False

        cap = cv2.VideoCapture(stream)
        if not cap.isOpened():
            raise Exception("Errore: impossibile aprire lo stream.")

        print("Stream avviato con successo.")
        self.cap = cap
        self.width = width if width != None else int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = height if height != None else int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def __del__(self):
        if self.cap != None:
            self.cap.release()
            print("video capture released")

        if self.out != None:
            self.out.release()
            print("output file released")


    def run(self):
        try:
            asyncio.run(self.start())
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            self.stop()
            print(f"Errore: {e}")

    async def start(self):
        
        self.running = True

        tasks = []
        
        tasks.append(self.read_frames())
        if self.window:
            tasks.append(self.display_frames())

        tasks.extend(await self.additional_task())
        await asyncio.gather(*tasks)
        print("fine task")

    @abstractmethod
    async def additional_task(self) -> list:
        return []

    async def read_frames(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Fine dello stream o errore.")
                await self.frame_queue.put(None)
                break

            frame = cv2.resize(frame, (self.width, self.height))

            if self.rotation == 90:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            elif self.rotation == 180:
                frame = cv2.rotate(frame, cv2.ROTATE_180)
            elif self.rotation == 270:
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            if self.recording and self.out is not None:
                self.out.write(frame)

            if self.tracking:
                frame = self.get_motion(frame)
            else:
                self.motion = False

            self.frame = frame

            if self.window:
                await self.frame_queue.put(frame)
            
            await asyncio.sleep(0)  # lascia spazio ad altri task

    async def display_frames(self):
        while self.running:
            frame = await self.frame_queue.get()
            if frame is None:
                break
            cv2.imshow("Stream Video", frame)

            pressedKey = cv2.waitKey(1) & 0xFF
            if pressedKey == ord('q'):
                cv2.destroyAllWindows()
                self.window = False
                self.running = False
                break
            elif pressedKey == ord('r'):
                self.toggle_recording()
            elif pressedKey == ord('p'):
                self.save_picture()

        self.stop()

    def get_motion(self, frame):
        # Converting color image to gray_scale image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Converting gray scale image to GaussianBlur 
        # so that change can be find easily
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # In first iteration we assign the value 
        # of previous_frame to our first frame
        if self.previous_frame is None:
            self.previous_frame = gray
            return frame

        # Difference between static background 
        # and current frame(which is GaussianBlur)
        diff_frame = cv2.absdiff(self.previous_frame, gray)

        # Update previous_frame
        self.previous_frame = gray

        # If change in between static background and
        # current frame is greater than 30 it will show white color(255)
        thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

        # Finding contour of moving object
        cnts,_ = cv2.findContours(thresh_frame.copy(), 
                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
            if cv2.contourArea(contour) < self.contour:
                self.motion = False
                return frame

            self.motion = True

            (x, y, w, h) = cv2.boundingRect(contour)
            # making green rectangle around the moving object
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)


        return frame

    def toggle_recording(self):
        if not self.recording:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{timestamp}.mp4"
            self.out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (self.width, self.height))
            self.recording = True
            self.video_filename = filename
            return True
        else:
            self.out.release()
            self.out = None
            self.recording = False  
            return False

    def save_picture(self):
        frame = self.frame
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        return filename

    def stop(self):
        self.running = False


# Avvio
if __name__ == "__main__":
    STREAM_URL = 0
    VIDEO_HEIGHT = None
    VIDEO_WIDTH = None
    CONTOUR = 3000
    ROTATION = 0
    streamer = MotionDetection(STREAM_URL, VIDEO_WIDTH, VIDEO_HEIGHT, ROTATION, CONTOUR, True, True)
    streamer.run()



