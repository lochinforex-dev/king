import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Tokeningizni yozing
bot = Bot(token="8740533809:AAFD-LeOzZeQWPqGTomuAmDPp04XOdMMlMQ")
dp = Dispatcher()

# Kino bazasi (Oddiy misol)
kinolar = {"1": "VIDEO_FILE_ID_SHU_YERGA"}

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Salom! Kino kodini yuboring.")

@dp.message()
async def echo_handler(message: Message):
    kod = message.text
    if kod in kinolar:
        await message.answer_video(kinolar[kod])
    else:
        await message.answer("Kino topilmadi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
