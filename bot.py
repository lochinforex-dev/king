import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# TOKENINGIZNI KIRITING
TOKEN = "BU_YERGA_BOT_TOKENINI_YOZING" 
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Barcha viloyat va tumanlar vaqt farqlari
REGIONS_DATA = {
    "Andijon": {"Andijon sh.": -12, "Asaka": -11, "Xonobod": -15},
    "Buxoro": {"Buxoro sh.": 24, "Gijduvon": 23, "Olot": 28},
    "Farg'ona": {"Farg'ona sh.": -10, "Qo'qon": -8, "Quva": -11},
    "Jizzax": {"Jizzax sh.": 6, "Zomin": 4, "Do'stlik": 8},
    "Namangan": {"Namangan sh.": -10, "Chust": -8, "Pop": -6},
    "Navoiy": {"Navoiy sh.": 16, "Zarafshon": 22, "Uchquduq": 24},
    "Qashqadaryo": {"Qarshi sh.": 18, "Kasbi (Mug'lon)": 20, "Shahrisabz": 15, "Muborak": 23},
    "Qoraqalpog'iston": {"Nukus": 44, "Mo'ynoq": 50, "To'rtko'l": 39},
    "Samarqand": {"Samarqand sh.": 9, "Kattaqo'rg'on": 12, "Urgut": 8},
    "Sirdaryo": {"Guliston": 4, "Yangiyer": 5, "Sirdaryo": 3},
    "Surxondaryo": {"Termiz sh.": 16, "Denov": 11, "Sherobod": 18},
    "Toshkent": {"Toshkent sh.": 0, "Angren": -3, "Bekobod": 2, "Chirchiq": -2},
    "Xorazm": {"Urganch": 40, "Xiva": 41, "Hazorasp": 38}
}

# 2026-yil 23-fevral (Bugun) uchun Toshkent vaqti
BASE_TIMES = {"saharlik": "06:02", "iftorlik": "18:14"}

def adjust_time(base_time, offset):
    t = datetime.strptime(base_time, "%H:%M")
    return (t + timedelta(minutes=offset)).strftime("%H:%M")

@dp.message(Command("start"))
async def start(message: types.Message):
    builder = InlineKeyboardBuilder()
    for reg in sorted(REGIONS_DATA.keys()):
        builder.button(text=reg, callback_data=f"r:{reg}")
    builder.adjust(2)
    await message.answer("🌙 Ramazon Taqvimi 2026\n\nViloyatingizni tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("r:"))
async def select_dist(call: types.CallbackQuery):
    region = call.data.split(":")[1]
    builder = InlineKeyboardBuilder()
    for dist in sorted(REGIONS_DATA[region].keys()):
        builder.button(text=dist, callback_data=f"d:{region}:{dist}")
    builder.button(text="⬅️ Orqaga", callback_data="back")
    builder.adjust(2)
    await call.message.edit_text(f"📍 {region} viloyati. Tumanni tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("d:"))
async def show_time(call: types.CallbackQuery):
    _, region, district = call.data.split(":")
    offset = REGIONS_DATA[region][district]
    sahar = adjust_time(BASE_TIMES["saharlik"], offset)
    iftor = adjust_time(BASE_TIMES["iftorlik"], offset)
    await call.message.edit_text(f"📍 Hudud: {district}\n🌅 Saharlik: {sahar}\n🌌 Iftorlik: {iftor}")

@dp.callback_query(F.data == "back")
async def back(call: types.CallbackQuery):
    await start(call.message)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
