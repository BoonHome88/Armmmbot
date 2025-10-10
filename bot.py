import os
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
import asyncio

# โหลดตัวแปรจาก environment (Railway หรือ Local .env)
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Timezone
tz = pytz.timezone("Asia/Bangkok")

# Scheduler
scheduler = AsyncIOScheduler(timezone=tz)

# ข้อความและ Activity ของแต่ละหมวด
MESSAGES = {
    "vehicle": {
        "text": "# แจ้งเตือนลบยานพาหนะ\nชาวเมืองทุกท่านอย่าลืมขึ้นยานพาหนะของท่านนะครับ <@&1419750622517006393>",
        "image": "https://img5.pic.in.th/file/secure-sv1/ddb3485e9cd775cf7f.jpg",
        "times": ["10:28", "14:28", "22:28", "03:28"],
        "color": 0xffb658,
        "activity": "กำลังจะลบรถนะครับทุกคน 🚗"
    },
    "Airdrop": {
        "text": "# แจ้งเตือนเข้า Airdrop ครับเพื่อนๆ\nชาวเมืองทุกท่านระวังโดนปรับนะครับ <@&1419750622517006393> <@&1419750622517006394>",
        "image": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2UyeWl2aXVjemQ5ZHpxaDQ4M3MwdzI4ZG5xaGVpb3djNDRrN2R4MyZlcD12MV9pbnRlcm5hbF9naWQmY3Q9Zw/ne3qb8GHvteK4QGtbs/giphy.gif",
        "times": ["19:45", "19:55", "22:45", "22:55"],
        "color": 0xff5858,
        "activity": "กำลังรอสมาชิกเข้าแอร์ดรอปนะครับ 😎"
    },
}

# Activity ตอนรอส่งข้อความ
WAITING_ACTIVITY = "อ้ายบุญโฮมกำลังนั่งเบิ่งคุณ... 👀"

# URL สำหรับ Streaming Activity
STREAM_URL = "https://www.twitch.tv/boonhomelive"

# ฟังก์ชันตั้ง Activity แบบ Streaming
async def set_activity(text, url=STREAM_URL):
    await bot.change_presence(activity=discord.Streaming(name=text, url=url))

# ฟังก์ชันส่งข้อความและเปลี่ยน Activity
async def send_message(category: str):
    data = MESSAGES.get(category)
    if not data:
        return

    # เปลี่ยน Activity ตามหมวด
    await set_activity(data["activity"])

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        embed = discord.Embed(description=data["text"], color=data["color"])
        embed.set_image(url=data["image"])
        await channel.send(embed=embed)
        print(f"[{datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}] ✅ Message sent ({category}) to {channel.name}")

    # กลับไป Activity ตอนรอส่งข้อความ
    await set_activity(WAITING_ACTIVITY)

# คำสั่ง Discord
@bot.command()
async def sendnow(ctx, category: str = "vehicle"):
    if category not in MESSAGES:
        await ctx.send(f"❌ หมวด '{category}' ไม่มีอยู่")
        return
    await send_message(category)
    await ctx.send(f"✅ ส่งข้อความหมวด '{category}' เรียบร้อยแล้ว!")

@bot.command()
async def next(ctx, category: str = None):
    now = datetime.now(tz)
    jobs = scheduler.get_jobs()
    upcoming = []
    for job in jobs:
        if category:
            if job.args[0] == category and job.next_run_time and job.next_run_time > now:
                upcoming.append(job.next_run_time)
        else:
            if job.next_run_time and job.next_run_time > now:
                upcoming.append(job.next_run_time)
    if upcoming:
        next_time = min(upcoming)
        await ctx.send(f"🕒 ข้อความถัดไปจะถูกส่งเวลา `{next_time.strftime('%H:%M %d/%m/%Y')}` (เวลาไทย)")
    else:
        await ctx.send("❌ ยังไม่มีงานที่ตั้งเวลาไว้")

@bot.command()
async def status(ctx):
    await ctx.send(f"✅ บอททำงานอยู่ตอนนี้ ({datetime.now(tz).strftime('%H:%M:%S %d/%m/%Y')})")

# เมื่อ bot พร้อม
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    # ตั้ง Activity ตอนรอ
    await set_activity(WAITING_ACTIVITY)
    print(f"🎮 Bot Streaming activity set: {WAITING_ACTIVITY}")

    # ตั้ง scheduler หลัง bot พร้อม
    for cat, info in MESSAGES.items():
        for t in info["times"]:
            hour, minute = map(int, t.split(":"))
            scheduler.add_job(
                send_message,
                trigger=CronTrigger(hour=hour, minute=minute, timezone=tz),
                args=[cat],
                coalesce=True,
                misfire_grace_time=60
            )

    scheduler.start()
    print("🕒 Scheduler started. Waiting for next job...")

bot.run(TOKEN)
