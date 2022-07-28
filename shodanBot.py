from shodan import Shodan
import os
from discord.ext import commands
import discord
#from dotenv import load_dotenv

# load token from .env
#load_dotev()
#TOKEN = os.environ['DISCORD_TOKEN']
# or use simple variable
TOKEN = 'DISCORD_TOKEN'
key = 'SHODAN_API_KEY'
try:
        api = Shodan(key)
except APIError:
        print("[-] Invalid Key..")

# limit of results, change as you see fit
limit = 5

bot = commands.Bot(command_prefix="?")
@bot.command(name="shodan")
async def search(ctx, args):

        counter = 0

        qResult = api.search(args)
        if len(qResult) == 0:
                await ctx.channel.send("[-] No Results Found..")

        for info in qResult['matches']:
                ip = info['ip_str']
                port = info['port']
                os = info['os']
                if os == None:
                        os = 'unknown'
                data = info['data']
                country = info['location']['country_name']
                city = info['location']['city']
                title = "[>>] Shodan Results for " + args
                embed = discord.Embed(title=title)
                embed.add_field(name="IP:Port", value=f'{ip}:{port}', inline=True)
                if os != 'unknown':
                        embed.add_field(name="OS", value=f'{os}', inline=False)
                embed.add_field(name="location", value=f'{country}, {city}', inline=False)
                embed.add_field(name="Banner", value=f'{data}', inline=False)
                await ctx.send(embed=embed)
                counter += 1
                if counter == limit:
                        break
bot.run(TOKEN)
