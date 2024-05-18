import asyncio
import os
import random

import dotenv
import pyrogram
from pyrogram import filters
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

dotenv.load_dotenv()


def generate_keyboard():
    keyboard = []
    for _ in range(2):
        row = []
        for _ in range(2):
            row.append(
                InlineKeyboardButton(
                    f"btn{random.randint(10, 99)}", callback_data="ignore"
                )
            )
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("update", callback_data="update")])
    keyboard.append([InlineKeyboardButton("reset", callback_data="reset")])
    return InlineKeyboardMarkup(keyboard)


async def on_start(client, message):
    await message.reply(".", reply_markup=generate_keyboard())


async def on_update(client, callback_query):
    await callback_query.message.edit_reply_markup(generate_keyboard())


async def on_reset(client, callback_query):
    await callback_query.message.edit_reply_markup(None)


async def main():
    client = pyrogram.Client(
        "bot",
        api_id=os.environ["API_ID"],
        api_hash=os.environ["API_HASH"],
        bot_token=os.environ["BOT_TOKEN"],
    )
    [
        client.add_handler(h)
        for h in [
            MessageHandler(on_start, filters.command("start")),
            CallbackQueryHandler(on_update, filters.regex("^update$")),
            CallbackQueryHandler(on_reset, filters.regex("^reset$")),
        ]
    ]
    await client.start()
    print("App started")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
