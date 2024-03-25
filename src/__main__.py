import asyncio
import logging

from g4f import Provider
from g4f.client import Client


def start_llmassist():
    client = Client(
        provider=Provider.RetryProvider(
            [Provider.Liaobots],
            shuffle=False
        )
    )
    response = client.chat.completions.create(
        model="",
        messages=[{"role": "user", "content": "Hello"}],
    )
    print(response.choices[0].message.content)


async def main():
    await asyncio.to_thread(start_llmassist)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
