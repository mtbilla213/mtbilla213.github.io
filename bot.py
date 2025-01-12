import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from config import Config
from mongodb import MongoDB

logging.basicConfig(level=logging.INFO)
config = Config()

bot = Bot(token=config.misc.bot_token)
dp = Dispatcher()
mongodb = MongoDB(uri=config.db.uri, db_name=config.db.name)

async def register_user(user_id: int, username: str = None, first_name: str = None):
    try:
        is_new = await mongodb.add_user(
            user_id=user_id,
            username=username,
            first_name=first_name
        )
        
        if is_new:
            keyboard = types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [types.InlineKeyboardButton(
                        text=config.strings.webapp_button,
                        web_app=types.WebAppInfo(url=config.misc.webapp_url)
                    )]
                ]
            )
            
            await bot.send_message(
                chat_id=user_id,
                text=config.strings.start_message,
                reply_markup=keyboard
            )
        
        return True
    except Exception as e:
        logging.error(f"Error registering user: {e}")
        return False

@dp.message(CommandStart())
async def start_command(message: types.Message):
    await register_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )

# Add specific filter for web_app_data
@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    try:
        logging.info(f"Received web app data: {message.web_app_data.data}")
        data = json.loads(message.web_app_data.data)
        
        if data.get("type") == "init_user":
            user_id = int(data.get("user_id"))
            logging.info(f"Processing web app user: {user_id}")
            
            await register_user(
                user_id=user_id,
                username=data.get("username"),
                first_name=data.get("first_name")
            )
    except Exception as e:
        logging.error(f"Error in handle_webapp_data: {e}")

async def main():
    try:
        logging.info("Starting bot...")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())