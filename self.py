from telethon import TelegramClient, events, functions
from datetime import datetime
import asyncio
import random

# اطلاعات اکانت خودت رو وارد کن
api_id = 123456  # <<-- API ID
api_hash = 'abc123yourhashhere'  # <<-- API HASH

client = TelegramClient('userbot', api_id, api_hash)

# فحش‌ها
insults = [
    "خفه شو مادرجنده کیرم تو کص ننت",
    "بیا برو خارکصه کیرم تو همه چیت",
    "خفه بچه سال",
    "قاشق زاده بس کن" 
]

# لیست کاربرانی که روشون قفل کردیم
locked_users = set()

# 💡 تابع تبدیل ساعت به فونت fancy
def fancy_time(raw_time):
    normal = "0123456789:"
    fancy = "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡:"
    trans_table = str.maketrans(normal, fancy)
    return raw_time.translate(trans_table)

# 🕒 آپدیت ساعت کنار اسم
async def update_name_loop():
    while True:
        try:
            raw_time = datetime.now().strftime(" %H:%M ")
            pretty_time = fancy_time(raw_time)
            me = await client.get_me()
            new_name = f"{me.first_name.split(' ')[0]} {pretty_time}"
            await client(functions.account.UpdateProfileRequest(first_name=new_name))
            print(f"[+] نام تغییر کرد به: {new_name}")
        except Exception as e:
            print(f"[!] خطا در تغییر نام: {e}")
        await asyncio.sleep(60)


# 😈 فحش با .insult
@client.on(events.NewMessage(pattern=r'\.insult'))
async def insult_user(event):
    if event.is_group:
        if event.reply_to_msg_id:
            reply_msg = await event.get_reply_message()
            name = reply_msg.sender.first_name if reply_msg.sender else "طرف"
            await event.reply(f"{name} {random.choice(insults)}")
        else:
            await event.reply("ریپلای کن رو پیام کسی که می‌خوای بهش فحش بدم 😈")


# 🔒 قفل روی کاربر با .lock
@client.on(events.NewMessage(pattern=r'\.lock'))
async def lock_user(event):
    if event.reply_to_msg_id:
        reply_msg = await event.get_reply_message()
        if reply_msg.sender_id:
            locked_users.add(reply_msg.sender_id)
            await event.reply(f"🔒 قفل شد روی: {reply_msg.sender.first_name}")
        else:
            await event.reply("نتونستم کاربر رو پیدا کنم.")

# 🔓 آزاد کردن کاربر با .unlock
@client.on(events.NewMessage(pattern=r'\.unlock'))
async def unlock_user(event):
    if event.reply_to_msg_id:
        reply_msg = await event.get_reply_message()
        if reply_msg.sender_id and reply_msg.sender_id in locked_users:
            locked_users.remove(reply_msg.sender_id)
            await event.reply(f"🔓 آزاد شد: {reply_msg.sender.first_name}")
        else:
            await event.reply("این یوزر تو لیست قفل نیست.")

# 👀 هر پیامی از یوزر قفل شده ببینه → فحش می‌ده
@client.on(events.NewMessage)
async def auto_insult(event):
    if event.sender_id in locked_users and event.is_group:
        await event.reply(random.choice(insults))

# 🎯 اجرای اصلی
async def main():
    await client.start()
    print("✅ سلف‌بات فعال شد!")
    await asyncio.gather(
        update_name_loop(),
        client.run_until_disconnected()
    )

if __name__ == '__main__':
    asyncio.run(main())
