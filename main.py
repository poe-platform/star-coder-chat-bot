import os

from fastapi_poe import make_app
from modal import Image, Secret, Stub, asgi_app

from star_coder_chat import StarCoderChatBot

image = Image.debian_slim().pip_install_from_requirements("requirements.txt")
stub = Stub("star-coder-chat-app")


@stub.function(image=image, secret=Secret.from_name("star-coder-chat-secret"))
@asgi_app()
def fastapi_app():
    bot = StarCoderChatBot(TOGETHER_API_KEY=os.environ["TOGETHER_API_KEY"])
    app = make_app(bot, access_key=os.environ["POE_ACCESS_KEY"])
    return app
