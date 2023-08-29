# StarCoderChat Bot

Chatbot powered by the StarCoderChat model.

## How do I run this myself?

- Refer to the quick start for general instructions on how to create server bots and
  deploy them on modal.com
- In Modal, create a secret named `star-coder-chat-secret` containing both your
  `TOGETHER_API_KEY` (obtainable by signing up at together.ai) and the `POE_ACCESS_KEY`
  you wish to use.
- Run `modal serve main.py`
- Create a bot on [poe.com](https://poe.com/create_bot?server=1) and provide your server
  url and access key.
