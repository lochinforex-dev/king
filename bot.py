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

# --- 2. HUDUDLAR ---
REGIONS_DATA = {
    "Toshkent": {"Toshkent sh.": 0, "Angren": -3, "Bekobod": 2, "Chirchiq": -2, "Olmaliq": 1, "Chinoz": 3, "Yangiyo'l": 2, "Piskent": 2},
    "Andijon": {"Andijon sh.": -12, "Asaka": -11, "Xonobod": -15, "Shahrixon": -12, "Paxtaobod": -14, "Marhamat": -11},
    "Farg'ona": {"Farg'ona sh.": -10, "Qo'qon": -8, "Quva": -11, "Marg'ilon": -10, "Rishton": -9, "Beshariq": -5},
    "Namangan": {"Namangan sh.": -10, "Chust": -8, "Pop": -6, "Uychi": -11, "Kosonsoy": -9},
    "Sirdaryo": {"Guliston": 4, "Yangiyer": 5, "Sirdaryo": 3, "Boyovut": 4, "Sardoba": 6},
    "Jizzax": {"Jizzax sh.": 6, "Zomin": 4, "G'allaorol": 7, "Do'stlik": 8, "Paxtakor": 7},
    "Samarqand": {"Samarqand sh.": 9, "Kattaqo'rg'on": 12, "Urgut": 8, "Ishtixon": 10, "Bulung'ur": 8, "Narpay": 12},
    "Qashqadaryo": {"Qarshi": 18, "Shahrisabz": 15, "Muborak": 23, "Kasbi (Mug'lon)": 20, "Kitob": 14, "G'uzor": 19, "Koson": 20, "Chiroqchi": 16},
    "Surxondaryo": {"Termiz": 16, "Denov": 11, "Sherobod": 18, "Sho'rchi": 12, "Boysun": 14, "Sariosiyo": 11},
    "Buxoro": {"Buxoro sh.": 24, "Gijduvon": 23, "Olot": 28, "Qorako'l": 27, "Vobkent": 23, "Kogon": 24},
    "Navoiy": {"Navoiy sh.": 16, "Zarafshon": 22, "Uchquduq": 24, "Nurota": 18, "Xatirchi": 14},
    "Xorazm": {"Urganch": 40, "Xiva": 41, "Hazorasp": 38, "Gurlan": 41, "Shovot": 42, "Xonqa": 40},
    "Qoraqalpog'iston": {"Nukus": 44, "Mo'ynoq": 50, "To'rtko'l": 39, "Qo'ng'irot": 48, "Beruniy": 39, "Xo'jayli": 45}
}

# --- 3. TO'LIQ 30 KUNLIK JADVAL (20-MART QAT'IY QO'SHILDI) ---
RAMADAN_CALENDAR = {
    "2026-02-19": {"saharlik": "05:44", "iftorlik": "18:03"},
    "2026-02-20": {"saharlik": "05:42", "iftorlik": "18:04"},
    "2026-02-21": {"saharlik": "05:41", "iftorlik": "18:06"},
    "2026-02-22": {"saharlik": "05:40", "iftorlik": "18:07"},
    "2026-02-23": {"saharlik": "05:38", "iftorlik": "18:08"},
    "2026-02-24": {"saharlik": "05:37", "iftorlik": "18:10"},
    "2026-02-25": {"saharlik": "05:35", "iftorlik": "18:11"},
    "2026-02-26": {"saharlik": "05:34", "iftorlik": "18:12"},
    "2026-02-27": {"saharlik": "05:32", "iftorlik": "18:14"},
    "2026-02-28": {"saharlik": "05:31", "iftorlik": "18:15"},
    "2026-03-01": {"saharlik": "05:29", "iftorlik": "18:16"},
    "2026-03-02": {"saharlik": "05:28", "iftorlik": "18:17"},
    "2026-03-03": {"saharlik": "05:26", "iftorlik": "18:19"},
    "2026-03-04": {"saharlik": "05:25", "iftorlik": "18:20"},
    "2026-03-05": {"saharlik": "05:23", "iftorlik": "18:21"},
    "2026-03-06": {"saharlik": "05:22", "iftorlik": "18:22"},
    "2026-03-07": {"saharlik": "05:20", "iftorlik": "18:24"},
    "2026-03-08": {"saharlik": "05:18", "iftorlik": "18:25"},
    "2026-03-09": {"saharlik": "05:17", "iftorlik": "18:26"},
    "2026-03-10": {"saharlik": "05:15", "iftorlik": "18:27"},
    "2026-03-11": {"saharlik": "05:14", "iftorlik": "18:29"},
    "2026-03-12": {"saharlik": "05:12", "iftorlik": "18:30"},
    "2026-03-13": {"saharlik": "05:10", "iftorlik": "18:31"},
    "2026-03-14": {"saharlik": "05:08", "iftorlik": "18:32"},
    "2026-03-15": {"saharlik": "05:07", "iftorlik": "18:33"},
    "2026-03-16": {"saharlik": "05:05", "iftorlik": "18:35"},
    "2026-03-17": {"saharlik": "05:03", "iftorlik": "18:36"},
    "2026-03-18": {"saharlik": "05:02", "iftorlik": "18:37"},
    "2026-03-19": {"saharlik": "05:00", "iftorlik": "18:38"},
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
    builder.button(text="🤲 Ramazon duolari", callback_data="show_prayers")
    builder.adjust(1)
    await message.answer("🌙 **Ramazon 2026**\n\n19-fevraldan 20-martgacha bo'lgan to'liq taqvim.", reply_markup=builder.as_markup())

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
    for dist in sorted(REGIONS_DATA[region].keys()):
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
    
    res = f"📍 **{district} ({region})**\n\n"
    if t:
        res += f"📅 Bugun: {today_str}\n🌅 Saharlik: **{t['sahar']}**\n🌌 Iftorlik: **{t['iftor']}**\n"
    else:
        res += "📅 Bugun Ramazon taqvimida yo'q.\n"
    
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 To'liq 30 kunlik jadval", callback_data=f"full:{region}:{district}")
    builder.button(text="🏠 Menu", callback_data="to_start")
    builder.adjust(1)
    await call.message.edit_text(res, parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("full:"))
async def full_calendar_handler(call: types.CallbackQuery):
    _, region, district = call.data.split(":")
    offset = REGIONS_DATA[region][district]
    
    sorted_dates = sorted(RAMADAN_CALENDAR.keys())
    
    # 1-qism (1-15 kunlar)
    res1 = f"📅 **{district} (1-15 kunlar):**\n\nKun | Sana | Sahar | Iftor\n"
    for i in range(15):
        d = sorted_dates[i]
        t = get_times(d, offset)
        res1 += f"{i+1} | {d[8:]}-{d[5:7]} | {t['sahar']} | {t['iftor']}\n"
    
    # 2-qism (16-30 kunlar, 20-martni o'z ichiga oladi)
    res2 = f"📅 **{district} (16-30 kunlar):**\n\nKun | Sana | Sahar | Iftor\n"
    for i in range(15, len(sorted_dates)):
        d = sorted_dates[i]
        t = get_times(d, offset)
        res2 += f"{i+1} | {d[8:]}-{d[5:7]} | {t['sahar']} | {t['iftor']}\n"

    await call.message.answer(res1)
    builder = InlineKeyboardBuilder()
    builder.button(text="🏠 Menu", callback_data="to_start")
    await call.message.answer(res2, reply_markup=builder.as_markup())

@dp.callback_query(F.data == "show_prayers")
async def show_prayers(call: types.CallbackQuery):
    text = (
        "🌅 **Saharlik duosi:**\n"
        "Navaytu an asuma sovma shahri ramazona minal fajri ilal mag'ribi, xolisan lillahi ta'ala. Allohu akbar.\n\n"
        "🌌 **Iftorlik duosi:**\n"
        "Allohumma laka sumtu va bika aamantu va ‘alayka tavakkaltu va ‘ala rizqika aftartu, "
        "fag‘firliy maa qoddamtu va maa axxortu, birohmatika yaa arhamar roohimiyn."
    )
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
