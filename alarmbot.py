import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
from datetime import datetime
import os
from dotenv import load_dotenv

# .env 파일에서 환경변수 불러오기
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

scheduler = AsyncIOScheduler(timezone='Asia/Seoul')

@bot.event
async def on_ready():
    print(f'{bot.user} 봇이 온라인입니다!')

    # 매일 0시, 3시, 6시... 정각마다 알림 전송
    scheduler.add_job(send_alarm, 'cron', hour='0,3,6,9,12,15,18,21', minute=0)
    scheduler.start()

async def send_alarm():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        now = datetime.now(pytz.timezone('Asia/Seoul')).strftime('%H:%M')
        await channel.send(f"<@&{ROLE_ID}> 결계 시간입니다 ({now})")

@bot.command()
async def test(ctx):
    await ctx.send(f'결계알림봇입니다.')

bot.run(TOKEN)
