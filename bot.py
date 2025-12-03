# telegram_auto_post_bot.py
# Full Telegram auto-post bot with image rotation, hourly schedule, custom menus, /start and /sendnow commands, Flask server for Render + UptimeRobot

import asyncio
import nest_asyncio
import logging
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler
from flask import Flask

nest_asyncio.apply()

# ========================= CONFIG ==============================
BOT_TOKEN = "8395409278:AAFXw8GMjYQp1DRkFOAkQUFtW0AvqG8GGqM"
CHANNEL_ID = -1002980186562

# ========================= CAPTIONS ============================
CAPTIONS = [
    ("images/1.jpg", """💎 ĐĂNG KÝ NHẬN 68K – NHẬN NGAY 500K!
🪄 Chỉ cần xác minh thông tin cá nhân – nhận tiền liền tay 
⚡️ Nhanh tay tham gia – đừng bỏ lỡ cơ hội có tiền free
🎁 Đăng ký ngay hôm nay để nhận nhiều phần quà hấp dẫn
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""),
    
    ("images/2.jpg", """🎰 SLOT FEVER 200% – QUÀ TỚI TAY-MAY TỚI LIỀN !
💸 Thưởng 200% nạp lần đầu – lên đến 6,888,000 VND
⚙️ Hoàn tất nạp tiền qua website WINBOOK – nhận thưởng tự động
⏳ Cơ hội có hạn – tham gia liền tay kẻo lỡ
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""),
    
   ("images/3.jpg", """🔥 NẠP 1 NHẬN 2 – THƯỞNG 100% NGAY!
 💵 Thưởng chào mừng 100% – thắng lớn đến 3,888,000 VND
 🎮 Áp dụng cho Slots, Bắn Cá, Thể Thao & Live Casino 
⚡️ Nhanh tay nạp – cơ hội nhân đôi vốn đang chờ bạn!
 🎯 x20 vòng cược rinh ngay 3,888,888 VND 
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""),
    
    ("images/4.jpg", """💥 NẠP ĐÂU TẶNG ĐÓ – THÊM 10% MỖI NGÀY!!
💸 Càng nạp càng được – tiền tự nhân lên!   
➕ Thưởng 10% mỗi ngày – nhận thưởng 6,000,000 VND
⏱ Cơ hội “đẻ thêm tiền” mỗi 24h tại WINBOOK
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""),
    
    ("images/5.jpg", """⚽ ĐẶT CƯỢC LẦN ĐẦU - KHÔNG SỢ RỦI RO ! 
🛡 WINBOOK bảo vệ 100% cho vé cược đầu tiên!
🔥 Chỉ áp dụng tại SABA Sports – trận lớn, kèo hot! 
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""),
    
    ("images/6.jpg", """🎉 MỜI BẠN BÈ - NHẬN HOÀN TIỀN KHÔNG GIỚI HẠN ! 
🔗 Dùng mã QR hoặc link giới thiệu để mời người chơi mới
💰 Mỗi lượt mời thành công: nhận hoàn 0.3%
🕓 Hoàn tiền phát lúc 16:00 ngày hôm sau
♾️ Không giới hạn số tiền hoàn!
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""),
    
    ("images/7.jpg", """🎁 THƯỞNG NẠP TUẦN 30% – NHẬN QUÀ MỖI TUẦN!
📈 Nhận 30% thưởng nạp – tối đa 6,000,000 VND
⚙️ Chỉ cần nạp tiền & hoàn doanh thu cược hợp lệ
📝 Đăng ký nhanh qua Mẫu Nạp Tiền trên WINBOOK
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""),
    
    ("images/8.jpg", """💥 THƯỞNG 50% – TRỌN BỘ SLOTS, LIVE & SPORTS!
👤 Thành viên WINBOOK nhận thưởng 1 lần duy nhất
💰 Nhận ngay 50% thưởng – tối đa 500,000 VND
🎰 Slots & Bắn Cá – Thưởng 50%, X5 vòng cược
🎬 Trò Chơi Trực Tiếp – Thưởng 50%, X5 vòng cược
⚽ Thể Thao – Thưởng 50%, X5 vòng cược
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""),
    
    ("images/9.jpg", """💰 CÀNG CHƠI CÀNG LỜI -HOÀN TỚI 1,2% !
🔄 Tự động hoàn tiền mỗi ngày – không giới hạn
👑 Chỉ dành cho thành viên WINBOOK
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""),

    ("images/10.jpg", """💰 THƯỞNG 5% MỖI NGÀY KHI CHỌN XỔ SỐ !
 🎯 Mỗi ngày nhận 5% ngay lập tức 
⏳ Ưu đãi có hạn – Nhận thưởng mỗi ngày lên đến 1,000 VND
💰X1 vòng cược nhanh tay chọn số
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""),
]

# ========================= MENU =================================
menu_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🔰 Đăng ký NHẬN 68K", url="https://www.winbook1.com"),
        InlineKeyboardButton("💬 Live Chat", url="https://direct.lc.chat/19366399/")
    ],
    [
        InlineKeyboardButton("👩‍💼 TELE CS001", url="https://t.me/WinbookCSKH001"),
        InlineKeyboardButton("👨‍💼 TELE CS002", url="https://t.me/WinbookCSKH002")
    ],
    [
        InlineKeyboardButton("📢 Kênh Chính", url="https://t.me/WinbookEvent"),
        InlineKeyboardButton("💭 Nhóm Chat", url="https://t.me/winbook8888")
    ],
    [
        InlineKeyboardButton("🌐 FANPAGE CHÍNH", url="https://www.facebook.com/profile.php?id=100076695622884")
    ]
])

# ========================= INIT =================================
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()
current_index = 0
app = Flask(__name__)

# ========================= FUNCTIONS ============================
async def post_image_loop():
    global current_index
    while True:
        img, cap = CAPTIONS[current_index]
        try:
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=open(img, "rb"),
                caption=cap,
                reply_markup=menu_keyboard
            )
            logging.info(f"Đã đăng hình số {current_index + 1}")
        except Exception as e:
            logging.error(f"Lỗi khi gửi: {e}")

        # TĂNG INDEX NẰM Ở NGOÀI TRY
        current_index = (current_index + 1) % len(CAPTIONS)

        await asyncio.sleep(60)

# Commands
async def start(update, context):
    text = (
        "🤖 *Bot WinbookEvent đang hoạt động!*\n"
        "💚 Auto-post đang chạy.\n\n"
        "Bạn có thể dùng các lệnh:\n"
        "• /sendnow – Gửi ngay bài kế tiếp\n"
        "• /start – Kiểm tra trạng thái bot\n"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=menu_keyboard
    )


async def sendnow(update, context):
    global current_index
    img, cap = CAPTIONS[current_index]

    await bot.send_photo(
        chat_id=update.effective_chat.id,    # gửi cho người gọi lệnh
        photo=open(img, "rb"),
        caption=cap,
        reply_markup=menu_keyboard
    )

    current_index = (current_index + 1) % len(CAPTIONS)

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("sendnow", sendnow))

# Flask route for uptime
@app.route('/')
def home():
    return "Bot alive"

# ========================= MAIN =================================
import threading

# Run Flask in a separate thread (để Render giữ bot sống)
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=10000), daemon=True).start()

async def main_async():
    asyncio.create_task(post_image_loop())  # gửi hình tự động
    await application.run_polling()         # nhận lệnh /start, /sendnow

asyncio.run(main_async())
