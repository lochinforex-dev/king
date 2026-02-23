import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- SOZLAMALAR ---
TOKEN = "BOT_TOKENINGIZNI_SHU_YERGA_YOZING"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- HUDUDLAR MA'LUMOTI ---
REGIONS_DATA = {
    "Toshkent": {"Toshkent sh.": 0, "Angren": -3, "Bekobod": 2, "Chirchiq": -2, "Yangiyo'l": 2},
    "Andijon": {"Andijon sh.": -12, "Asaka": -11, "Xonobod": -15, "Shahrixon": -12},
    "Farg'ona": {"Farg'ona sh.": -10, "Qo'qon": -8, "Quva": -11, "Marg'ilon": -10},
    "Namangan": {"Namangan sh.": -10, "Chust": -8, "Pop": -6, "Kosonsoy": -9},
    "Sirdaryo": {"Guliston": 4, "Yangiyer": 5, "Sirdaryo": 3},
    "Jizzax": {"Jizzax sh.": 6, "Zomin": 4, "G'allaorol": 7},
    "Samarqand": {"Samarqand sh.": 9, "Kattaqo'rg'on": 12, "Urgut": 8, "Ishtixon": 10},
    "Qashqadaryo": {"Qarshi": 18, "Shahrisabz": 15, "Muborak": 23, "Kasbi": 20, "Kitob": 14, "G'uzor": 19, "Koson": 20},
    "Surxondaryo": {"Termiz": 16, "Denov": 11, "Sherobod": 18, "Boysun": 14},
    "Buxoro": {"Buxoro sh.": 24, "Gijduvon": 23, "Olot": 28, "Qorako'l": 27},
    "Navoiy": {"Navoiy sh.": 16, "Zarafshon": 22, "Uchquduq": 24, "Xatirchi": 14},
    "Xorazm": {"Urganch": 40, "Xiva": 41, "Hazorasp": 38, "Gurlan": 41},
    "Qoraqalpog'iston": {"Nukus": 44, "Mo'ynoq": 50, "To'rtko'l": 39, "Xo'jayli": 45}
}

# Ramazon 2026 Toshkent vaqti (NAMUNA - 30 kunlik qilib to'ldiriladi)
RAMADAN_CALENDAR = {
    "2026-02-23": {"saharlik": "06:02", "iftorlik": "18:14"},
    "2026-02-24": {"saharlik": "06:01", "iftorlik": "18:15"},
    "2026-02-25": {"saharlik": "05:59", "iftorlik": "18:17"},
}

# --- YORDAMCHI FUNKSIYALAR ---
def get_times(date_str, offset):
    day_data = RAMADAN_CALENDAR.get(date_str)
    if not day_data: return None
    s_obj = datetime.strptime(day_data["saharlik"], "%H:%M")
    i_obj = datetime.strptime(day_data["iftorlik"], "%H:%M")
    return {
        "sahar": (s_obj + timedelta(minutes=offset)).strftime("%H:%M"),
        "iftor": (i_obj + timedelta(minutes=offset)).strftime("%H:%M")
    }

# --- HANDLERLAR ---

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Taqvimlarni ko'rish", callback_data="show_regions")
    builder.button(text="🤲 Duolar menyusi", callback_data="show_prayers")
    builder.adjust(1)
    await message.answer("🌙 **Ramazon Taqvimi 2026** botiga xush kelibsiz!\n\nKerakli bo'limni tanlang:", parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "show_regions")
async def show_regions(call: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    for region in sorted(REGIONS_DATA.keys()):
        builder.button(text=region, callback_data=f"reg:{region}")
    builder.button(text="🏠 Bosh menyu", callback_data="to_start")
    builder.adjust(2)
    await call.message.edit_text("📍 Viloyatingizni tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("reg:"))
async def region_handler(call: types.CallbackQuery):
    region = call.data.split(":")[1]
    builder = InlineKeyboardBuilder()
    for dist in sorted(REGIONS_DATA[region].keys()):
        builder.button(text=dist, callback_data=f"dist:{region}:{dist}")
    builder.button(text="⬅️ Orqaga", callback_data="show_regions")
    builder.adjust(2)
    await call.message.edit_text(f"📍 **{region}**. Tumanni tanlang:", parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("dist:"))
async def time_handler(call: types.CallbackQuery):
    _, region, district = call.data.split(":")
    offset = REGIONS_DATA[region][district]
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    t = get_times(today, offset)
    tm = get_times(tomorrow, offset)
    
    res = f"📍 **Hudud: {district} ({region})**\n\n"
    if t: res += f"📅 **Bugun:**\n🌅 Saharlik: {t['sahar']}\n🌌 Iftorlik: {t['iftor']}\n\n"
    if tm: res += f"📅 **Ertaga:**\n🌅 Saharlik: {tm['sahar']}\n🌌 Iftorlik: {tm['iftor']}"
    
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Orqaga", callback_data=f"reg:{region}")
    builder.button(text="🏠 Bosh menyu", callback_data="to_start")
    await call.message.edit_text(res, parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "show_prayers")
async def show_prayers(call: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="🌅 Saharlik duosi", callback_data="prayer_sahar")
    builder.button(text="🌌 Iftorlik duosi", callback_data="prayer_iftor")
    builder.button(text="🏠 Bosh menyu", callback_data="to_start")
    builder.adjust(1)
    await call.message.edit_text("🤲 Duo turini tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("prayer_"))
async def prayer_text(call: types.CallbackQuery):
    p_type = call.data.split("_")[1]
    if p_type == "sahar":
        text = (
            "🌅 **Saharlik (og'iz yopish) duosi:**\n\n"
            "Navaytu an asuma sovma shahri ramazona minal fajri ilal mag'ribi, xolisan lillahi ta'ala. Allohu akbar.\n\n"
            "**Ma'nosi:** Ramazon oyining ro'zasini subhdan to kun botguncha xolis Alloh uchun tutmoqni niyat qildim. Alloh buyukdir."
        )
    else:
        text = (
            "🌌 **Iftorlik (og'iz ochish) duosi:**\n\n"
            "Allohumma laka sumtu va bika amantu va 'alayka tavakkaltu va 'ala rizqika aftartu, fag'firli ya g'offaru ma qoddamtu va ma axxortu.\n\n"
            "**Ma'nosi:** Ey Alloh, ushbu ro'zamni Sen uchun tutdim va Senga iymon keltirdim va Senga tavakkal qildim va bergan rizqing bilan iftor qildim. Ey gunohlarni afv etuvchi Zot, mening oldingi va keyingi gunohlarimni mag'firat qil."
        )
    
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Orqaga", callback_data="show_prayers")
    await call.message.edit_text(text, parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "to_start")
async def to_start(call: types.CallbackQuery):
    await start_handler(call.message)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
