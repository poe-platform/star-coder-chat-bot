from __future__ import annotations

import json
from dataclasses import dataclass
from typing import AsyncIterable

import httpx
import httpx_sse
from fastapi_poe import PoeBot
from fastapi_poe.types import QueryRequest
from sse_starlette.sse import ServerSentEvent

BASE_URL = "https://api.together.xyz/inference"

BASE_PROMPT = """"
<|user|>
 Hi!
<|end|>
<|assistant|>
 I am the StarCoderChat bot. I help users with programming and code related questions. \
I wrap any code in my response in backticks so that it can be rendered using Markdown.
<|end|>
"""


@dataclass
class StarCoderChatBot(PoeBot):
    TOGETHER_API_KEY: str  # Together.ai api key

    def construct_prompt(self, query: QueryRequest):
        prompt = "\n"
        prompt = BASE_PROMPT
        for message in query.query:
            if message.role == "user":
                prompt += f"<|user|>\n {message.content}\n<|end|>\n"
            elif message.role == "bot":
                prompt += f"<|assistant|>\n {message.content}\n<|end|>\n"
            elif message.role == "system":
                pass
            else:
                raise ValueError(f"unknown role {message.role}.")
        prompt += "<|assistant|>"
        return prompt

    async def query_together_ai(self, prompt) -> str:
        payload = {
            "model": "HuggingFaceH4/starchat-alpha",
            "prompt": prompt,
            "max_tokens": 1000,
            "stop": ["<|endoftext|>", "<|end|>"],
            "stream_tokens": True,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1,
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.TOGETHER_API_KEY}",
        }

        async with httpx.AsyncClient() as aclient:
            async with httpx_sse.aconnect_sse(
                aclient, "POST", BASE_URL, headers=headers, json=payload
            ) as event_source:
                async for event in event_source.aiter_sse():
                    if event.data != "[DONE]":
                        token = json.loads(event.data)["choices"][0]["text"]
                        yield token

    async def get_response(self, query: QueryRequest) -> AsyncIterable[ServerSentEvent]:
        prompt = self.construct_prompt(query)
        async for word in self.query_together_ai(prompt):
            yield self.text_event(word)
