#import

from defer import return_value
import discord
from discord.ext import commands 
from discord.ext.commands import has_permissions, MissingPermissions
from form import Form
from reactions import ReactConfirm
import json
import asyncio
from discord.user import User
import requests
import aiohttp
import datetime
import os
import io
import logging
import textwrap
from traceback import format_exception
import time
from random import randint
import urllib.parse, urllib.request, re


prefix = "!!"

bot = commands.Bot(command_prefix=prefix)

bot.remove_command("help")

@bot.event
async def on_ready():
    print (f'Bejelentkeztünk: {bot.user.name}#{bot.user.discriminator} - {bot.user.id} nevében')
    await bot.change_presence(activity=discord.Game(name='Bálna BOT - BÉTA'))

bot.owner_id = 825005165572259900
api_key = "d1635ea13b4f9c870cc81fa621d2fc4b"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, discord.ext.commands.CommandNotFound):
        await ctx.send(err)
    else:
        await ctx.send("Unknown error.")
        print(ctx.message.content, err)
    
@bot.event
async def on_message_delete(message):
    await message.channel.send("Egy üzenet itt törölve lett!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content[:len(prefix)] == prefix:
        await bot.process_commands(message)

@bot.command()
async def segítség(ctx):
    user = ctx.message.author
    await ctx.send("**A segítséget privát üzenetben küldtem el.**")

    embed = discord.Embed(title="Segítség", color= ctx.author.color)
    embed.description = "Weboldalunk \n [Nyomj ide](http://www.balnabot.ml). \n Parancsaim \n [Nyomj ide](http://balnabot.ml/pages/commands.html). \n Csapatunk \n [Nyomj ide](http://balnabot.ml/pages/team.html). \n BOT meghívása \n [Nyomj ide](https://discord.com/oauth2/authorize?client_id=865287960189468712&permissions=8&scope=bot). \n Support szerver \n [Nyomj ide](https://discord.gg/F9guPytWUg)."
    await user.send(embed=embed)

@bot.command() 
async def say(ctx, *,message1):
    if not ctx.message.author.bot:
        await ctx.message.channel.trigger_typing()
        await ctx.message.delete()
        await ctx.send(message1)
    else:
        pass

@bot.command()
async def clear(ctx, amount: int):
	await ctx.channel.purge(limit=amount + 1)
	await ctx.send(f'Sikeresen töröltem {amount} üzenetet! ✅')

@bot.command()
async def ping(ctx):
    await ctx.send('A pingem: {} ms'.format(round(bot.latency * 1000)))

"""@bot.command(name='ping', aliases=['latency'])
async def ping(ctx):
    
    m = await ctx.reply(content='Pingelés...', mention_author=False)
    #await ctx.message.delete()
    createdAt = int(time.monotonic())
    e = discord.Embed(title='Pong!', colour=discord.Colour.blurple())
    e.add_field(name='Bot ping:',
    value=f'`{format(round(bot.latency * 1000))}ms`')
    ping = (time.monotonic() - createdAt) * 1000
    e.add_field(name='Message Roundtrip:', value=f'`{ping}ms`')
    e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await m.edit(content=None, embed=e)"""

@bot.command()
async def ban(ctx, *, member: discord.Member, reason=None):
    if ctx.author.guild_permissions.ban_members==True:
        await member.ban(reason=reason)
        await ctx.send(f'{member.name} ki lett bannolva Ő általa: {ctx.author.name}!')

"""@bot.command()
async def embedrule(ctx):
	
    if ctx.author.guild_permissions.ban_members==True:
		
        await ctx.message.delete()
        embed = discord.Embed(
            title='Szabályzat - www.balnabot.ml',
            description='''1. Ne küldj sértő üzeneteket, képeket, GIF-eket. Ha mégis így döntesz, akkor használj spoiler-t
    2. Tiszteld a szerver többi tagját, és a Staffokat.
    3. Ne küldj NSFW (Erotika/Gyomorforgató tartalom) üzeneteket, képeket, GIF-eket.
    4. Ne spamelj, ne hírdess engedély nélkül más szervereket.
    5. Tartsd be a Discord TOS-t https://discord.com/terms
    6. Mindig nézd meg, hogy melyik szobába küldöd az üzenetedet
    7. Ne kéregessél rangokat/rangot!
    8. Ne próbálj meg olyan parancsot írni az egyik botnak, hogy ha ahhoz nincsen jogod!
    ** A szabályok nem ismerése nem mentesít a büntetés alól.
    ''',
            color=discord.Color.green()
        )
        
        embed.set_author(name='Bálna BOT Support & Dev & Teszt szerver')
        embed.set_footer(text='A vezetőség a szabályzat módosításának a jogát fenntartja!')
        
        await ctx.send(embed=embed)
"""

@bot.command()
async def sayembed(ctx, *,titleE):
        
        await ctx.message.channel.trigger_typing()
        await ctx.message.delete()
        sayembedd = discord.Embed(
            title=f"{ctx.message.author.name} ezt küldi:",
            description=titleE,
            color=discord.Color.green()
        )

        await ctx.send(embed=sayembedd)

"""@bot.event()
async def on_message_edit(message_before, message_after):
    edembed=discord.Embed(title="{} edited a message".format(message_before.member.name), 
    description="", color="Blue")
    edembed.add_field(name= message_before.content ,value="This is the message before any edit", 
    inline=True)
    edembed.add_field(name= message_after.content ,value="This is the message after the edit", 
    inline=True)
    channel=bot.get_channel(channel_id)
    await channel.send(channel, embed=edembed)"""
    
@bot.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    if avamember is None:
        avamember = ctx.author
    
    
    userAvatarUrl = avamember.avatar_url
    embedavatar = discord.Embed(
        title = f"{avamember} profilképe:",
        
        color=000000,

        timestamp=ctx.message.created_at
    )
    embedavatar.set_image(url=avamember.avatar_url)
    embedavatar.set_footer(text=f"Parancsot használta: {ctx.author}")
    await ctx.send(embed=embedavatar)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author      
    
    
    embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
    
    embed.set_author(name=f"Felhasználói információk - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Parancsot használta: {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Felhasználóneve:", value=member.display_name)
    embed.add_field(name="Felhasználó létrehozva:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %P UTC"))
    embed.add_field(name="BOT?", value=member.bot)

    await ctx.send(embed=embed)

'''@bot.command()
async def on_member_join(self, member): 
    for channel in member.guild.channels: 
        channel = bot.get_channel(channel_id)
        if str(channel) == "join-leave": 
            embedjoin = discord.Embed(color=0x4a3d9a) 
            embedjoin.add_field(name="Welcome", value=f"{member.name} has joined {member.guild.name}", inline=False) 
            embedjoin.set_image(url="https://i.pinimg.com/originals/8c/9a/07/8c9a079986a4ce112882fea6db3ffdee.gif") 
            await channel.send(embed=embedjoin)
        else:
            print("teszt1")
'''

@bot.command()
async def dog(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/dog')
      factjson = await request2.json()

   embeddog = discord.Embed(title="Kutyuli!", color=discord.Color.dark_purple(), timestamp=ctx.message.created_at)
   embeddog.set_image(url=dogjson['link'])
   embeddog.set_footer(text=factjson['fact'])
   await ctx.send(embed=embeddog)

@bot.command()
async def cat(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat')
      catjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/cat')
      factjson = await request2.json()

   embedcat = discord.Embed(title="Cicaa!", color=discord.Color.dark_purple(), timestamp=ctx.message.created_at)
   embedcat.set_image(url=catjson['link'])
   embedcat.set_footer(text=factjson['fact'])
   await ctx.send(embed=embedcat)

@bot.command()
async def birb(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/birb')
      catjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/birb')
      factjson = await request2.json()

   embedcat = discord.Embed(title="Madaracska!", color=discord.Color.dark_purple(), timestamp=ctx.message.created_at)
   embedcat.set_image(url=catjson['link'])
   embedcat.set_footer(text=factjson['fact'])
   await ctx.send(embed=embedcat)

@bot.command()
async def fox(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/fox')
      catjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/fox')
      factjson = await request2.json()

   embedcat = discord.Embed(title="Rókácska!", color=discord.Color.dark_purple(), timestamp=ctx.message.created_at)
   embedcat.set_image(url=catjson['link'])
   embedcat.set_footer(text=factjson['fact'])
   await ctx.send(embed=embedcat)

@bot.command()
async def meme(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/meme')
      memejson = await request.json()

   #x = datetime.datetime.now()
   embedmeme = discord.Embed(title=f"Új meme!", color=discord.Color.dark_purple(), timestamp=ctx.message.created_at)
   embedmeme.set_image(url=memejson['image'])
   embedmeme.set_footer(text=memejson['caption'])
   await ctx.send(embed=embedmeme)

@bot.command()
async def anime(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/animu/hug')
      animejson = await request.json()

   #x = datetime.datetime.now()
   embedanime = discord.Embed(title=f"Új Anime!", color=discord.Color.dark_purple(), timestamp=ctx.message.created_at)
   embedanime.set_image(url=animejson['link'])
   await ctx.send(embed=embedanime)

"""@bot.command()
async def gif(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/canvas/triggered')
      catjson = await request.json()

   embedcat = discord.Embed(title="Madaracska!", color=discord.Color.dark_purple())
   embedcat.set_image(url=catjson['link'])
   embedcat.set_footer(text=f"Parancsot használta: {ctx.author}")
   await ctx.send(embed=embedcat)"""

@bot.command(name='invite', description='Create an invite link')
async def invite(ctx, reason):
    invite = await ctx.guild.create_invite(reason=reason)
    await ctx.author.send(str(invite)) # Send the invite to the user
    invite.inviter = ctx.author
    bot.dispatch('invite_command', invite)

@bot.event
async def on_invite_command(invite):
    channel_id = 867082207112855612
    channel = bot.get_channel(channel_id) # Remember how to get channel IDs?
    embed = discord.Embed(title="New Invite",description=f"Created by {invite.inviter}\nCode: {str(invite)}")
    await channel.send(embed=embed)

"""@bot.command(name="eval", aliases=["exec"])
@commands.is_owner()
async def _eval(ctx, *, code):
    code = clean_code(code)

    local_variables = {
        "discord": discord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message
    }

    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
            )

            obj = await local_variables["func"]()
            result = f"{stdout.getvalue()}\n-- {obj}\n"
    except Exception as e:
        result = "".join(format_exception(e, e, e.__traceback__))

    pager = Pag(
        timeout=100,
        entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
        length=1,
        prefix="```py\n",
        suffix="```"
    )

    await pager.start(ctx)

"""

def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n"))[1:][:-3]

    return content

async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            await bot.send_message(ctx.message.channel, page)
    else:
        pages = bot.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            await bot.send_message(ctx.message.channel, page)

"""@bot.event
async def on_command_error(error, ctx):
    
	if not commandList in str(ctx.command):
		if isinstance(error, commands.CommandNotFound):
			pass
		elif isinstance(error, commands.MissingRequiredArgument):
			await send_cmd_help(ctx)
		elif isinstance(error, commands.BadArgument):
			await send_cmd_help(ctx)
	else:
		await ctx.bot.send_message(ctx.message.channel, errorMessage)
"""
    
"""@bot.command()
async def userinfo(ctx, member: discord.Member):


    embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f"Felhasználói információk - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Parancsot használta: {ctx.author}", icon_url=ctx.avatar_url)

    embed.add_field(name="ID: ", value=member.id)
    embed.add_field(name="Neve: ", value=member.display_name)
    embed.add_field(name="Fiók létrehozva: ", value=member.created_at.strftime("%A"))
    

    ctx.send(embed=embed)"""

@bot.command()
async def ötlet(ctx, tartalom):
    await ctx.message.delete()
    channel = bot.get_channel(864947116697452564)
    otletMsg = str(ctx.message.content)
    msg = otletMsg[7:]
    #x = datetime.datetime.now()
    embed = discord.Embed(title="Új ötlet érkezett!", color=ctx.author.color, timestamp=ctx.message.created_at)
    embed.add_field(name=f"Tőle: {ctx.author.name}", value=msg)
    embed.set_thumbnail(url="http://3200.hu/wp-content/uploads/2017/08/%C3%B6tlet.jpg")
    #embed.set_footer(text=f"{x.year}. {x.month}. {x.day}. {x.hour}:{x.minute}:{x.second}")
    await channel.send(embed=embed)

@bot.command()
async def szerverek(ctx):
    embed = discord.Embed(title="https://www.balnabot.ml", color=ctx.author.color, timestamp=ctx.message.created_at)
    embed.add_field(name="Szerverek: ", value=len(bot.guilds))
    embed.set_footer(text=f"Parancsot használta: {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def exec(ctx, *code):
    return_value = eval(' '.join(code))
    if return_value:
        await ctx.send(return_value)
    else:
        await ctx.send("Successfull, but no return value.")

@bot.command()
async def időjárás(ctx, *, city: str):
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    channel = ctx.message.channel
    if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsiuis = str(round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            weather_description = z[0]["description"]
            embed = discord.Embed(title=f"Időjárás itt: {city_name}",
                              color=ctx.guild.me.top_role.color,
                              timestamp=ctx.message.created_at,)
            embed.add_field(name="Időjárás", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Hőfok(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
            embed.add_field(name="Páratartalom(%)", value=f"**{current_humidity}%**", inline=False)
            embed.add_field(name="Légköri nyomás(hPa)", value=f"**{current_pressure}hPa**", inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Parancsot használta {ctx.author.name}")
            await channel.send(embed=embed)
    else:
        await channel.send("A megadott város nem található.")
    if city is None:
        await ctx.send("Helytelen használat!")


bot.run("TOKEN")
