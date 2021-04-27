import discord
from discord.ext import commands

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from cogs.meme.meme import Meme

class Core(commands.Cog):
	"""Core commands"""	
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		try:
			await self.bot.change_presence(
				status = discord.Status.idle, 
				activity = discord.Activity(
					type = discord.ActivityType.listening,
					name = "your heartbeats"
					)
				)
			print("Activity set successfully")
		except:
			print("Cannot set activity")
		
		print("Connected to discord")

		#initializing scheduler
		scheduler = AsyncIOScheduler()

		scheduler.add_job(Meme.meme, CronTrigger(second = "0, 30, 57")) 

		#starting the scheduler
		scheduler.start()

	@commands.Cog.listener()
	async def on_member_join(self, member):
		channel = member.guild.system_channel
			
		if channel is not None:
			embed = discord.Embed(
				title = f"Welcome @{member.name}", 
				description = f"Ayeeeee! Welcome to {member.guild.name} 😁😁"
			) 
			embed.set_thumbnail(url = member.avatar_url) 
			await channel.send(embed = embed)

	@commands.command()
	async def ping(self, ctx) :
		await ctx.send(f"🏓 Pong with {str(round(self.bot.latency, 3))}")

		