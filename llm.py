import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

with open("personality", "r", encoding="utf-8") as file:
    personality = file.read()

async def api_call(message):

    config = [{"role": "system", "content": personality
        },
            {"role": "user", "content": message
        }
    ]

    if not isinstance(message, str):
        config[1]["content"] = message.content

    response = await client.chat.completions.create(
        model="openrouter/free",
        messages=config,
        timeout=60
    )

    return response.choices[0].message.content
