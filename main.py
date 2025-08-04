from telegrambot import TelegramBot
import tomllib



def main():
    print("start objectmotion notify!")
    token = ""
    chat_id = None
    stream = ""
    video_width = None
    video_height = None
    rotation = 90
    contour = 3000

    with open("config.toml", "rb") as conf:
        data = tomllib.load(conf)

        try:
            token = data["telegram"]["token"]
            if token == "":
                raise Exception("token value cannot empty") 
        except KeyError:
            raise Exception("there arent token value in config file or in wrong section") 

        try:
            chat_id = data["telegram"]["chat_id"]
            if chat_id == "":
                raise Exception("chat_id value cannot empty") 

        except KeyError:
            raise Exception("there arent chat_id value in config file or in wrong section") 

        try:
            stream = data["camera"]["stream"]
            if stream == "0":
                stream = 0
            if stream == "":
                raise Exception("stream value cannot empty") 

        except KeyError:
            raise Exception("there arent stream value in config file or in wrong section") 

        try:
            video_width = data["camera"]["video_width"]
            video_height = data["camera"]["video_height"]
        except KeyError:
            video_width = None
            video_height = None
            print("error on get width and heigt")

        try:
            rotation = data["camera"]["rotation"]
        except KeyError:
            pass

        try:
            contour = data["camera"]["contour"]
        except KeyError:
            pass

    
    bot = TelegramBot(token, chat_id, stream, video_width, video_height, rotation, contour, True, False)
    bot.run()


if __name__ == "__main__":
    main()
