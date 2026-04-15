import sqlite3
from aiogram import Bot, Dispatcher, executor, types

# Bot tokeningizni shu yerga qo'ying
API_TOKEN = '8740533809:AAFD-LeOzZeQWPqGTomuAmDPp04XOdMMlMQ'
ADMIN_ID = 12345678  # O'zingizning ID raqamingizni yozing

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Ma'lumotlar bazasini yaratish
db = sqlite3.connect("kino_baza.db")
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS movies (
    code TEXT PRIMARY KEY,
    file_id TEXT
)""")
db.commit()

@dp.message_handler(commands=['start'])
async def start(m: types.Message):
    await m.answer("Assalomu alaykum! Kino kodini yuboring.")

# ADMIN uchun: Video va kodni bazaga qo'shish
@dp.message_handler(content_types=['video'])
async def add_movie(m: types.Message):
    if m.from_user.id == ADMIN_ID:
        if m.caption:
            code = m.caption
            f_id = m.video.file_id
            cursor.execute("INSERT OR REPLACE INTO movies VALUES (?, ?)", (code, f_id))
            db.commit()
            await m.reply(f"✅ Saqlandi! Kod: {code}")
        else:
            await m.reply("❌ Xato! Videoning izoh (caption) qismiga kodni yozing.")

# FOYDALANUVCHI uchun: Kod yozsa kinoni topib berish
@dp.message_handler()
async def get_movie(m: types.Message):
    cursor.execute("SELECT file_id FROM movies WHERE code=?", (m.text,))
    res = cursor.fetchone()
    if res:
        await bot.send_video(m.chat.id, res[0], caption=f"Kino kodi: {m.text}")
    else:
        await m.answer("⚠️ Kechirasiz, bu kod bilan kino topilmadi.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
