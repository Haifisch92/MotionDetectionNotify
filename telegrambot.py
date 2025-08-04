import asyncio
import aiohttp
import time
from PIL import Image
from io import BytesIO
from motion_detection import MotionDetection





class TelegramBot(MotionDetection):

    def __init__(self, token, chat_id, stream, width = None, height = None, rotation = 0, contour = 3000, tracking = True, create_window = False, queue_size=10):
        super().__init__(stream, width, height, rotation, contour, tracking, create_window, queue_size)
        self.session = None
        self.token = token
        self.chat_id = chat_id
        self.base_url = f'https://api.telegram.org/bot{token}'



    def run(self):
        async def run_async():
            try:
                self.session = aiohttp.ClientSession()
                await self.start()
            except Exception as e:
                print(e)
            finally:
                print("close aiohttp session")
                if self.session:
                    await self.session.close()              

        asyncio.run(run_async())

    """
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()
    """

    async def additional_task(self) -> list:
        return [self.poll_telegram(), self.background_task()]

    async def send_message(self, text):
        params = {'chat_id': self.chat_id, 'text': text}
        async with self.session.post(f'{self.base_url}/sendMessage', params=params) as resp:
            return await resp.json()

    async def get_updates(self, offset=None):
        params = {'timeout': 100}
        if offset is not None:
            params['offset'] = offset
        async with self.session.get(f'{self.base_url}/getUpdates', params=params) as resp:
            return await resp.json()

    async def send_photo(self, caption: str, pathToPhoto: str):
        # Apri l'immagine e convertila in RGB
        photo = Image.open(pathToPhoto).convert('RGB')

        # Salva l'immagine in memoria (BytesIO)
        with BytesIO() as output:
            photo.save(output, format='JPEG')
            output.seek(0)
            photo_bytes = output.read()

        # Prepara la richiesta multipart
        data = {'chat_id': self.chat_id, 'caption': caption}
        files = {'photo': ('photo.jpg', photo_bytes, 'image/jpeg')}

        # Manda la richiesta in async
        form = aiohttp.FormData()
        form.add_field('chat_id', str(self.chat_id))
        form.add_field('caption', caption)
        form.add_field('photo', photo_bytes, filename='photo.jpg', content_type='image/jpeg')

        async with self.session.post(f'{self.base_url}/sendPhoto', data=form) as resp:
            return await resp.json()

    async def send_video(self, caption: str, path_to_video: str):
        # Leggi il file video in bytes
        with open(path_to_video, 'rb') as f:
            video_bytes = f.read()

        # Prepara la form multipart
        form = aiohttp.FormData()
        form.add_field('chat_id', str(self.chat_id))
        form.add_field('caption', caption)
        form.add_field('video', video_bytes, filename='video.mp4', content_type='video/mp4')

        # Manda la richiesta
        async with self.session.post(f'{self.base_url}/sendVideo', data=form) as resp:
            return await resp.json()

    async def poll_telegram(self):
        offset = None

        while True:
            try:
                updates = await self.get_updates(offset)

                if updates.get("ok") and "result" in updates:
                    for update in updates["result"]:

                        if "message" in update and "text" in update["message"]:
                            chat_id = update["message"]["chat"]["id"]
                            text = update["message"]["text"]
                            
                            if text == "/foto":
                                await self.send_photo( "", self.save_picture())

                            if text == "/video":
                                if self.recording:
                                    self.toggle_recording()
                                    await self.send_video( "", self.video_filename)
                                else:
                                    self.toggle_recording()
                                    await self.send_message(f"start recording video")
                                
                            if text == "/tracking":
                                if not self.tracking:
                                    self.tracking = True
                                    await self.send_message(f"start tracking movment")
                                else:
                                    self.tracking = False
                                    await self.send_message(f"stop tracking movment")
                        offset = update["update_id"] + 1

            except Exception as e:
                print("Errore Telegram:", e)
                await asyncio.sleep(5)

            await asyncio.sleep(1)

    async def background_task(self):
        detection_time = None
        delta_minute = 1
        video_sent = True

        while True:

            message_again = False

            try:
                remining_time = time.time() - detection_time
                message_again = remining_time > (60 * delta_minute)
            except TypeError:
                message_again = True

            if self.motion and  message_again:
                detection_time = time.time()
                video_sent = False

                if not self.recording:
                    self.toggle_recording()

                await self.send_message(f"motion detected")
            
            else:
                #invia l ultimo video in chat
                if not video_sent and message_again:
                    print("invia l ultimo video in chat")
                    if self.recording:
                        self.toggle_recording()
                        await self.send_video("", self.video_filename)
                    video_sent = True

            await asyncio.sleep(0)


