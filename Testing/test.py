import asyncio
import psycopg2
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv
from pathlib import Path
import os

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Подключаем env
dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path)

# Переменные из env
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения TELEGRAM_BOT_TOKEN не установлена")

# Подключение к базе данных
def get_db_connection():
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("Переменная окружения DATABASE_URL не установлена")
    return psycopg2.connect(db_url)


# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):

    user_id = message.from_user.id

    conn = get_db_connection()
    cursor = conn.cursor()   

    cursor.execute("INSERT INTO chats (user_id) VALUES (%s) ON CONFLICT DO NOTHING", (user_id,))
    conn.commit()
    conn.close()    

    await message.answer("Привет! Я бот, который поможет тебе следить за питанием твоего питомца.")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "Вот список доступных команд:\n\n"
        "/add_food <название еды> <daily|special> <интервал(для special)> - Добавить еду с частотой кормления.\n"
        "/get_food - Получить список всех добавленных продуктов и частоты их кормления.\n"
    )
    await message.answer(help_text)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())