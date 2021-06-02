import discord
from discord.ext import commands

import os
import psycopg2
import pytz


class Birthday(commands.Cog):
    """Never forget birthday of your friends"""

    def __init__(self):
        # Set up database
        DATABASE_URL = os.environ["DATABASE_URL"]

        self.dbcon = psycopg2.connect(DATABASE_URL, sslmode = "require")
        self.cursor = self.dbcon.cursor()

        # Make a table if not already made
        query = """CREATE TABLE IF NOT EXISTS bday(
                id          BIGINT  NOT NULL,
                guild_id    BIGINT  NOT NULL,
                bday_date   INT     NOT NULL,
                bday_month  INT     NOT NULL,
                tz          TEXT    NOT NULL
                )"""
        self.cursor.execute(query)
        self.dbcon.commit()
        print("bday Table created")

    @commands.guild_only()
    @commands.group(invoke_without_command = True)
    async def bday(self, ctx):
        """To set your bday type `luci bday set`
        If you want to edit a bday type `luci bday edit`"""
        pass

    @bday.command(name = "set")
    async def setbday(self, ctx, member: discord.Member, date, tz = "GMT"):
        """Usage: luci bday set @Lucifer Chase 27/02 kolkata
        If you don't care about the timezone thing leave it blank"""

        date = date.split("/")
        for i in range(2):
            if (i == 0 and date[i] > 31 or date[i] < 0):
                await ctx.send("Bruh! Fill a valid date")
            elif (i == 1 and date[i] > 12 or date[i] < 0):
                await ctx.send("Bruh! Fill a valid date")
        bday_date, bday_month = date

        list_of_timezones = list(pytz.all_timezones)
        
        for i in range(len(list_of_timezones)):
            if (tz.title() in list_of_timezones[i]):
                tz = list_of_timezones[i]
                break
        else:
            await ctx.send("Uh oh! Timezone not found 👀")
            await ctx.send("You can check list of timezones using `luci timezones [continent name]`")
            return

        query = f"""INSERT INTO bday VALUES
                ({member.id}, {member.guild.id}, {bday_date}, {bday_month}, '{tz}')"""

        try:
            self.cursor.execute(query)
            self.dbcon.commit()
        except Exception as error:
            await ctx.send(f"```css\n{error}```")
            await ctx.send(str("Are you doing everything correctly?" + 
                "Might want to check usage `luci help bday set`" + 
                "Or if the problem persists ping `@Lucifer Chase`"))
        else:
            embed = discord.Embed(title = "Success! <a:nacho:839499460874862655>", color = 0x00FFFF)
            embed.add_field(name = "Member", value = member.nick)
            embed.add_field(name = "Date", value = "/".join(date))
            embed.add_field(name = "Timezone", value = tz)

            await ctx.send(embed = embed)
            await ctx.send("If you want to edit, type `luci help bday set`")

    @bday.command(name = "edit")
    async def editbday(self, ctx, member: discord.Member, date, tz = "UTC"):
        """Usage: luci bday edit @Lucifer Chase 27/02 kolkata
        If you don't care about the timezone thing leave it blank"""

        date = date.split("/")
        for i in range(2):
            if (date[i] == 1):
                date[i] = "0" + date[i]
            elif (i == 0 and date[i] > 31 or date[i] < 0):
                await ctx.send("Bruh! Fill a valid date")
            elif (i == 1 and date[i] > 12 or date[i] < 0):
                await ctx.send("Bruh! Fill a valid date")
        bday_date, bday_month = date

        list_of_timezones = list(pytz.all_timezones)
        
        for i in range(len(list_of_timezones)):
            if (tz.title() in list_of_timezones[i]):
                tz = list_of_timezones[i]
                break
        else:
            await ctx.send("Uh oh! Timezone not found 👀")
            await ctx.send("You can check list of timezones using `luci timezones [continent name]`")
            return

        query = f"DELETE FROM bday WHERE id = {member.id}"

        try:
            self.cursor.execute(query)
            self.dbcon.commit()
        except Exception as error:
            await ctx.send(f"```css\n{error}```")
            await ctx.send("Are you sure you have added your bday to the database in the first place?")

        query = f"""INSERT INTO bday VALUES
                ({member.id}, {member.guild.id}, {bday_date}, {bday_month}, '{tz}')"""

        try:
            self.cursor.execute(query)
            self.dbcon.commit()
        except Exception as error:
            await ctx.send(f"```css\n{error}```")
            await ctx.send(str("Are you doing everything correctly?" + 
                "Might want to check usage `luci help bday set`" + 
                "Or if the problem persists ping `@Lucifer Chase`"))
        else:
            embed = discord.Embed(title = "Success! <a:nacho:839499460874862655>", color = 0x00FFFF)
            embed.add_field(name = "Member", value = member.nick)
            embed.add_field(name = "Date", value = "/".join(date))
            embed.add_field(name = "Timezone", value = tz)

            await ctx.send(embed = embed)
            await ctx.send("If you want to edit, type `luci help bday set`")

