import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- 1. SOZLAMALAR ---
TOKEN = "8113803802:AAHQOQnnAdCAkiCGiFOD0RBmOJ5eR1_LF-Y"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 2. O‘ZBEKISTONNING BARCHA TUMANLARI (TO‘LIQ) ---
REGIONS_DATA = {
    "Toshkent": {"Toshkent sh.": 0, "Angren": -3, "Bekobod": 2, "Chirchiq": -2, "G'azalkent": -3, "Piskent": 2, "Yangiyo'l": 2, "Olmaliq": 1, "Buka": 4, "Chinoz": 3, "Oqqo'rg'on": 2, "Parkent": -1, "Toshkent tum.": 0, "Zangiota": 0, "Qibray": -1, "Yuqorichirchiq": -2, "O'rtachirchiq": 1, "Quyichirchiq": 3},
    "Andijon": {"Andijon sh.": -12, "Asaka": -11, "Xonobod": -15, "Shahrixon": -12, "Marhamat": -11, "Paxtaobod": -14, "Qo'rg'ontepa": -14, "Buloqboshi": -12, "Izboskan": -13, "Xo'jaobod": -12, "Jalaquduq": -13, "Oltinko'l": -12, "Baliqchi": -11, "Bo'ston": -10, "Ulug'nor": -9},
    "Farg'ona": {"Farg'ona sh.": -10, "Qo'qon": -8, "Quva": -11, "Marg'ilon": -10, "Rishton": -9, "Oltiariq": -9, "Yozyovon": -10, "Beshariq": -5, "Uchko'prik": -8, "Bag'dod": -9, "Buvayda": -8, "Dang'ara": -8, "Furqat": -6, "Qo'shtepa": -10, "Toshloq": -10, "O'zbekiston tum.": -6, "So'x": -8},
    "Namangan": {"Namangan sh.": -10, "Chust": -8, "Pop": -6, "Uychi": -11, "Uchqo'rg'on": -12, "Kosonsoy": -9, "Mingbuloq": -8, "To'raqo'rg'on": -9, "Chartaq": -11, "Norin": -11, "Namangan tum.": -10, "Yangiqo'rg'on": -10},
    "Sirdaryo": {"Guliston": 4, "Yangiyer": 5, "Sirdaryo": 3, "Boyovut": 4, "Sardoba": 6, "Oqoltin": 6, "Xovos": 5, "Sayhunobod": 3, "Mirzaobod": 5},
    "Jizzax": {"Jizzax sh.": 6, "Zomin": 4, "Do'stlik": 8, "G'allaorol": 7, "Paxtakor": 7, "Mirzachul": 9, "Arnasoy": 9, "Baxmal": 8, "Forish": 10, "Zarbdor": 7, "Sharof Rashidov": 6, "Yangiobod": 5},
    "Samarqand": {"Samarqand sh.": 9, "Kattaqo'rg'on": 12, "Urgut": 8, "Ishtixon": 10, "Bulung'ur": 8, "Narpay": 12, "Payariq": 10, "Jomboy": 9, "Nurobod": 11, "Oqdaryo": 10, "Pastdarg'om": 10, "Toyloq": 9, "Qo'shrabot": 11, "Paxtachi": 13, "Samarqand tum.": 9},
    "Qashqadaryo": {"Qarshi": 18, "Shahrisabz": 15, "Muborak": 23, "Kasbi (Mug'lon)": 20, "Kitob": 14, "G'uzor": 19, "Chiroqchi": 16, "Dehqonobod": 18, "Koson": 20, "Nishon": 21, "Mirishkor": 24, "Ko'kdala": 17, "Yakkabog'": 15, "Qamashi": 17, "Qarshi tum.": 18},
    "Surxondaryo": {"Termiz": 16, "Denov": 11, "Sherobod": 18, "Sho'rchi": 12, "Boysun": 14, "Sariosiyo": 11, "Jarqo'rg'on": 15, "Qumqo'rg'on": 13, "Muzrobot": 19, "Oltinsoy": 12, "Uzun": 10, "Qiziriq": 15, "Bandixon": 14, "Angor": 17, "Termiz tum.": 16},
    "Buxoro": {"Buxoro sh.": 24, "Gijduvon": 23, "Olot": 28, "Qorako'l": 27, "Vobkent": 23, "Gazli": 27, "Qorovulbozor": 25, "Shofirkon": 24, "Kogon": 24, "Jondor": 25, "Peshku": 24, "Romitan": 25, "Buxoro tum.": 24, "Qorovulbozor": 25},
    "Navoiy": {"Navoiy sh.": 16, "Zarafshon": 22, "Uchquduq": 24, "Nurota": 18, "Xatirchi": 14, "Qiziltepa": 17, "Tomdi": 22, "Karmana": 16, "Konimex": 18, "Navbahor": 15, "Qiziltepa": 17},
    "Xorazm": {"Urganch": 40, "Xiva": 41, "Hazorasp": 38, "Gurlan": 41, "Shovot": 42, "Xonqa": 40, "Bog'ot": 39, "Yangiariq": 41, "Yangibozor": 42, "Qo'shko'pir": 43, "Tuproqqal'a": 36, "Urganch tum.": 40},
    "Qoraqalpog'iston": {"Nukus": 44, "Mo'ynoq": 50, "To'rtko'l": 39, "Qo'ng'irot": 48, "Beruniy": 39, "Xo'jayli": 45, "Chimboy": 46, "Ellikqala": 38, "Kegeyli": 45, "Shumanay": 47, "Qanliko'l": 46, "Taxtako'pir": 44, "Qorao'zak": 44, "Bo'zatov": 45, "Taxiatosh": 45, "Amudaryo": 40}
}

# --- 3. TO'LIQ 30 KUNLIK TAQVIM (20-MART HAM BOR!) ---
RAMADAN_CALENDAR = {
    "2026-02-18": {"saharlik": "05:45", "iftorlik": "18:02"}, "2026-02-19": {"saharlik": "05:44", "iftorlik": "18:03"},
    "2026-02-20": {"saharlik": "05:42", "iftorlik": "18:04"}, "2026-02-21": {"saharlik": "05:41", "iftorlik": "18:06"},
    "2026-02-22": {"saharlik": "05:40", "iftorlik": "18:07"}, "2026-02-23": {"saharlik": "05:38", "iftorlik": "18:08"},
    "2026-02-24": {"saharlik": "05:37", "iftorlik": "18:10"}, "2026-02-25": {"saharlik": "05:35", "iftorlik": "18:11"},
    "2026-02-26": {"saharlik": "05:34", "iftorlik": "18:12"}, "2026-02-27": {"saharlik": "05:32", "iftorlik": "18:14"},
    "2026-02-28": {"saharlik": "05:31", "iftorlik": "18:15"}, "2026-03-01": {"saharlik": "05:29", "iftorlik": "18:16"},
    "2026-03-02": {"saharlik": "05:28", "iftorlik": "18:17"}, "2026-03-03": {"saharlik": "05:26", "iftorlik": "18:19"},
    "2026-03-04": {"saharlik": "05:25", "iftorlik": "18:20"}, "2026-03-05": {"saharlik": "05:23", "iftorlik": "18:21"},
    "2026-03-06": {"saharlik": "05:22", "iftorlik": "18:22"}, "2026-03-07": {"saharlik": "05:20", "iftorlik": "18:24"},
    "2026-03-08": {"saharlik": "05:18", "iftorlik": "18:25"}, "2026-03-09": {"saharlik": "05:17", "iftorlik": "18:26"},
    "2026-03-10": {"saharlik": "05:15", "iftorlik": "18:27"}, "2026-03-11": {"saharlik": "05:14", "iftorlik": "18:29"},
    "2026-03-12": {"saharlik": "05:12", "iftorlik": "18:30"}, "2026-03-13": {"saharlik": "05:10", "iftorlik": "18:31"},
    "2026-03-14": {"saharlik": "05:08", "iftorlik": "18:32"}, "2026-03-15": {"saharlik": "05:07", "iftorlik": "18:33"},
    "2026-03-16": {"saharlik": "05:05", "iftorlik": "18:35"}, "2026-03-17": {"saharlik": "05:03", "iftorlik": "18:36"},
    "2026-03-18": {"saharlik": "05:02", "iftorlik": "18:37"}, "2026-03-19": {"saharlik": "05:00", "iftorlik": "18:38"},
    "2026-03-20": {"saharlik": "04:58", "iftorlik": "18:40"}
}

def get_times(date_str, offset):
    day_data = RAMADAN_CALENDAR.get(date_str)
    if not day_data: return None
    s_obj = datetime.strptime(day_data["saharlik"], "%H:%M")
    i_obj = datetime.strptime(day_data["iftorlik"], "%H:%M")
    return {
        "sahar": (s_obj + timedelta(minutes=offset)).strftime("%H:%M"),
        "iftor": (i_obj + timedelta(minutes=offset)).strftime("%H:%M")
    }

# --- 4. HANDLERLAR ---
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="📍 Hududni tanlash", callback_data="show_regions")
    builder.button(text="🤲 Duolar", callback_data="show_prayers")
    builder.adjust(1)
    await message.answer("🌙 **Ramazon 2026**\nO'zbekistonning barcha tumanlari kiritilgan taqvim.", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "show_regions")
async def show_regions(call: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    for region in sorted(REGIONS_DATA.keys()):
        builder.button(text=region, callback_data=f"reg:{region}")
    builder.button(text="🏠 Menu", callback_data="to_start")
    builder.adjust(2)
    await call.message.edit_text("📍 Viloyatni tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("reg:"))
async def region_handler(call: types.CallbackQuery):
    region = call.data.split(":")[1]
    builder = InlineKeyboardBuilder()
    districts = REGIONS_DATA[region]
    for dist in sorted(districts.keys()):
        builder.button(text=dist, callback_data=f"dist:{region}:{dist}")
    builder.button(text="⬅️ Orqaga", callback_data="show_regions")
    builder.adjust(2)
    await call.message.edit_text(f"📍 **{region}**. Tumanni tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("dist:"))
async def time_handler(call: types.CallbackQuery):
    _, region, district = call.data.split(":")
    offset = REGIONS_DATA[region][district]
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    t = get_times(today_str, offset)
    
    res = f"📍 **{district} ({region})**\n"
    if t:
        res += f"📅 Sana: {today_str}\n🌅 Saharlik: **{t['sahar']}**\n🌌 Iftorlik: **{t['iftor']}**"
    else:
        res += "\nBugun uchun ma'lumot yo'q."

    builder = InlineKeyboardBuilder()
    builder.button(text="🏠 Menu", callback_data="to_start")
    await call.message.edit_text(res, parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "show_prayers")
async def show_prayers(call: types.CallbackQuery):
    text = "🌅 **Saharlik:** Navaytu an asuma sovma shahri ramazona minal fajri ilal mag'ribi...\n\n🌌 **Iftorlik:** Allohumma laka sumtu va bika aamantu... birohmatika yaa arhamar roohimiyn."
    builder = InlineKeyboardBuilder()
    builder.button(text="🏠 Menu", callback_data="to_start")
    await call.message.edit_text(text, parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "to_start")
async def to_start(call: types.CallbackQuery):
    await start_handler(call.message)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
