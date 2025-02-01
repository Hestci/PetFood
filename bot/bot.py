import asyncio
import psycopg2
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv
from pathlib import Path
import os
import re

# Включаем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    cursor.execute("INSERT INTO chat (user_id) VALUES (%s) ON CONFLICT DO NOTHING", (user_id,))
    logger.info(f"User {user_id} inserted or already exists.")
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


# router = Router() # Разобраться с роутами


@dp.message(Command("add_food"))
async def cmd_add_food(message: types.Message, command):
    # Если не переданы никакие аргументы
    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы")
        return

    # Логируем аргументы
    logger.info(f"Аргументы команды: {command.args}")

    # Регулярное выражение для обработки аргументов
    pattern = r"^(.*?)\s+(daily|special)$"
    match = re.match(pattern, command.args)

    # Если аргументы не соответствуют шаблону
    if not match:
        await message.answer("Ошибка: неверный формат аргументов. Используйте: <описание> <daily|special>")
        return

    # Извлекаем данные из регулярного выражения
    description = match.group(1).strip()  # Описание
    food_type = match.group(2).strip()    # Тип (daily или special)

    # Логируем результат
    logger.info(f"Описание: {description}, Тип: {food_type}")

        # Если тип "special", запрашиваем интервал
    if food_type == "special":
        await message.answer("Раз в сколько дней давать еду?")
        #await state.set_state(FoodStates.waiting_for_interval)  # Переводим в состояние ожидания интервала
    else:

        # Написать sql запросс

        
        # Отправляем ответ пользователю
        await message.answer(f"Еда добавленна: {description}, Тип: {food_type}")

@





# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())