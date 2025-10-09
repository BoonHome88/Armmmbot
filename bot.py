import os
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler(timezone="Asia/Bangkok")

@bot.event
async def on_ready():
    print(f"🤖 บอทออนไลน์แล้ว: {bot.user}")
    scheduler.add_job(send_message, 'cron', hour=9, minute=0, args=[
        "🌞 สวัสดีตอนเช้า! วันนี้ท้องฟ้าสดใส",
        "https://i.imgur.com/your-image.jpg"
    ])
    scheduler.add_job(send_message, 'cron', hour=12, minute=0, args=[
        "🍚 เที่ยงแล้ว อย่าลืมกินข้าว"
    ])
    scheduler.add_job(send_message, 'cron', hour=18, minute=0, args=[
        "🌇 เย็นแล้ว พักผ่อนบ้างนะ",
        "https://i.imgur.com/your-second-image.jpg"
    ])
    scheduler.start()

async def send_message(message, image_url=None):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        if image_url:
            embed = discord.Embed(description=message)
            embed.set_image(url=image_url)
            await channel.send(embed=embed)
        else:
            await channel.send(message)

bot.run(TOKEN)
