from telethon import TelegramClient
from datetime import datetime, timedelta, timezone
import os

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')

SOURCE = '@notehistkz'
DEST = '@notehistkz2'

async def main():
    async with TelegramClient('forwarder_bot', api_id, api_hash) as client:
        # Calculate 24h cutoff
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(hours=24)

        messages_to_forward = []

        async for message in client.iter_messages(SOURCE):
            # Stop once we hit older messages
            if message.date < cutoff:
                break

            messages_to_forward.append(message)

        # Reverse to keep chronological order
        messages_to_forward.reverse()

        if messages_to_forward:
            await client.forward_messages(DEST, messages_to_forward)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())