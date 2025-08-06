
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
import asyncio
import os

API_TOKEN = os.getenv("8204097621:AAFdFSZ0KACpsJkwHPT6alNrQ0ANQcZ-wbM")  # Токен будет браться из переменной окружения

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

user_piki_sum = {}

class PikiForm(StatesGroup):
    waiting_for_piki = State()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ввести пики")],
        [KeyboardButton(text="Сумма пиков")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=main_kb)

@dp.message(F.text == "Ввести пики")
async def enter_piki(message: types.Message, state: FSMContext):
    await message.answer("Введите число пиков:")
    await state.set_state(PikiForm.waiting_for_piki)

@dp.message(PikiForm.waiting_for_piki)
async def process_piki(message: types.Message, state: FSMContext):
    try:
        piki = int(message.text)
        user_id = message.from_user.id
        current_sum = user_piki_sum.get(user_id, 0)
        user_piki_sum[user_id] = current_sum + piki
        await message.answer(f"Пики добавлены. Текущая сумма: {user_piki_sum[user_id]}")
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите целое число.")

@dp.message(F.text == "Сумма пиков")
async def show_piki_sum(message: types.Message):
    user_id = message.from_user.id
    total = user_piki_sum.get(user_id, 0)
    await message.answer(f"Текущая сумма пиков: {total}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
