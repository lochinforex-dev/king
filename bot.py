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

# --- 2. RASMIY HUDUDLAR VA OFFSETLAR (Rasmga asosan) ---
REGIONS_DATA = {
    "Qashqadaryo": {
        "Qarshi sh.": 0, "Kasbi (Mug'lon)": 1, "Koson": 1, "Nishon": 1,
        "Muborak": 3, "Mirishkor": 2, "Chiroqchi": -2, "G'uzor": -1,
        "Shahrisabz": -3, "Yakkabog'": -3, "Kitob": -3, "Qamashi": -2,
        "Ko'kdala": 0, "Dehqonobod": -1
    }
}

# --- 3. RASMIY TAQVIM (Qarshi vaqti bilan) ---
RAMADAN_CALENDAR = {
    "2026-02-19": {"saharlik": "06:07", "iftorlik": "18:22"},
    "2026-02-20": {"saharlik": "06:06", "iftorlik": "18:23"},
    "2026-02-21": {"saharlik": "06:05", "iftorlik": "18:25"},
    "2026-02-22": {"saharlik": "06:04", "iftorlik": "18:26"},
    "2026-02-23": {"saharlik": "06:02", "iftorlik": "18:27"},
    "2026-02-24": {"saharlik": "06:01", "iftorlik": "18:28"},
    "2026-02-25": {"saharlik": "06:00", "iftorlik": "18:29"},
    "2026-02-26": {"saharlik": "05:59", "iftorlik": "18:30"},
    "2026-02-27": {"saharlik": "05:57", "iftorlik": "18:31"},
    "2026-02-28": {"saharlik": "05:56", "iftorlik": "18:32"},
    "2026-03-01": {"saharlik": "05:54", "iftorlik": "18:33"},
    "2026-03-02": {"saharlik": "05:53", "iftorlik": "18:34"},
    "2026-03-03": {"saharlik": "05:52", "iftorlik": "18:35"},
    "2026-03-04": {"saharlik": "05:50", "iftorlik": "18:36"},
    "2026-03-05": {"saharlik": "05:49", "iftorlik": "18:37"},
    "2026-03-06": {"saharlik": "05:47", "iftorlik": "18:38"},
    "2026-03-07": {"saharlik": "05:46", "iftorlik": "18:39"},
    "2026-03-08": {"saharlik": "05:44", "iftorlik": "18:40"},
    "2026-03-09": {"saharlik": "05:43", "iftorlik": "18:41"},
    "2026-03-10": {"saharlik": "05:41", "iftorlik": "18:42"},
    "2026-03-11": {"saharlik": "05:40", "iftorlik": "18:43"},
    "2026-03-12": {"saharlik": "05:38", "iftorlik": "18:44"},
    "2026-03-13": {"saharlik": "05:36", "iftorlik": "18:45"},
    "2026-03-14": {"saharlik": "05:35", "iftorlik": "18:46"},
    "2026-03-15": {"saharlik": "05:33", "iftorlik": "18:47"},
    "2026-03-16": {"saharlik": "05:32", "iftorlik": "18:48"},
    "2026-03-17": {"saharlik": "05:30", "iftorlik": "18:49"},
    "2026-03-18": {"saharlik": "05:28", "iftorlik": "18:50"},
    "2026-03-19": {"saharlik": "05:27", "iftorlik": "18:51"},
    "2026-03-20": {"saharlik": "05:25", "iftorlik": "18:52"}
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
    builder.button(text="📍 Qashqadaryo tumanlari", callback_data="show_districts")
    builder.button(text="🤲 Duolar", callback_data="show_prayers")
    builder.adjust(1)
    await message.answer("🌙 **Ramazon 2026**\nQashqadaryo viloyati rasmiy taqvimi.", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "show_districts")
async def show_districts(call: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    districts = REGIONS_DATA["Qashqadaryo"]
    for dist in sorted(districts.keys()):
        builder.button(text=dist, callback_data=f"dist:{dist}")
    builder.button(text="🏠 Menu", callback_data="to_start")
    builder.adjust(2)
    await call.message.edit_text("📍 Tumanni tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("dist:"))
async def time_handler(call: types.CallbackQuery):
    district = call.data.split(":")[1]
    offset = REGIONS_DATA["Qashqadaryo"][district]
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    t = get_times(today_str, offset)
    
    res = f"📍 **{district}**\n\n"
    if t:
        res += f"📅 Bugun: {today_str}\n🌅 Saharlik: **{t['sahar']}**\n🌌 Iftorlik: **{t['iftor']}**\n"
    else:
        res += "⚠️ Bugun uchun ma'lumot yo'q.\n"
    
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Kelgusi kunlar jadvali", callback_data=f"full:{district}")
    builder.button(text="🏠 Menu", callback_data="to_start")
    builder.adjust(1)
    await call.message.edit_text(res, parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("full:"))
async def full_calendar_handler(call: types.CallbackQuery):
    district = call.data.split(":")[1]
    offset = REGIONS_DATA["Qashqadaryo"][district]
    
    # MUHIM: Bugungi sanani aniqlaymiz
    today = datetime.now().date()
    
    res = f"📅 **{district} uchun kelgusi kunlar:**\n\n"
    res += "Sana | Sahar | Iftor\n"
    res += "---|---|---\n"
    
    found_any = False
    for date_str in sorted(RAMADAN_CALENDAR.keys()):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # FAQAT BUGUNDAN KEYINGI KUNLARNI KO'RSATISH
        if date_obj > today:
            t = get_times(date_str, offset)
            res += f"{date_str[8:]}-{date_str[5:7]} | **{t['sahar']}** | **{t['iftor']}**\n"
            found_any = True

    if not found_any:
        res = "⚠️ Ramazon oyi yakunlandi yoki kelgusi kunlar haqida ma'lumot yo'q."

    builder = InlineKeyboardBuilder()
    builder.button(text="🏠 Menu", callback_data="to_start")
    await call.message.answer(res, parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "to_start")
async def to_start(call: types.CallbackQuery):
    await start_handler(call.message)

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

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
