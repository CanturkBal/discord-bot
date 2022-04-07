
from re import search
from tkinter import S
import wikipedia
from attr import has, s
from click import command, pass_context
import discord
from discord.ext import commands
import random
from datetime import datetime
from discord.ext.commands import has_permissions, MissingPermissions
import string
import youtube_dl
import os

bot = commands.Bot(command_prefix="!r ",help_command = None)
@bot.event
async def on_ready():
    print("bot is online")
@bot.command()
async def ping(context):
    await context.send("Pong!")
@bot.command()
async def coinflip(context):
    myEmbed1 = discord.Embed(title = "")
    
    list = ["heads","tales"]
    num = random.choice(list)
    if num == "heads":
        await context.send("heads")
        myEmbed1.set_image(url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3rA62gJeuZk9YneMno6I65ymAFzSAaFtNHQ&usqp=CAU")
        await context.send(embed = myEmbed1)

    elif num == "tales":

        await context.send("tales")
        myEmbed1.set_image(url = "https://upload.wikimedia.org/wikipedia/commons/6/64/1TL_obverse.png")
        await context.send(embed = myEmbed1)
        
@bot.command(aliases = ["about"])
async def help(context):
    myEmbed = discord.Embed(title = "commands",description = "these are the commands that you can use for this bot",color = discord.Colour.dark_blue())
    myEmbed.set_thumbnail(url = "https://play-lh.googleusercontent.com/0oO5sAneb9lJP6l8c6DH4aj6f85qNpplQVHmPmbbBxAukDnlO7DarDW0b-kEIHa8SQ",)
    myEmbed.add_field(name = "!r ping", value = "this command replies back with you pong whenever you write !r ping",inline = False)
    myEmbed.add_field(name = "!r coinflip",value = "this command allows you to do a coin flip",inline = False)
    myEmbed.add_field(name = "!r rps" ,value = "you can play rock paper scizzor with this bot",inline = False)
    myEmbed.add_field(name  = "!r wikipedia {the thing that you want to search for}",value = "you can search something on wikipedia",inline = False)
    myEmbed.add_field(name = "!r (java,python,javascript)",value = "gives info abaout the certain proggraming language",inline = False)
    myEmbed.add_field(name = "!r date",value = "gives the current date",inline = False)
    myEmbed.add_field(name = "!r covid",value= "gives the current covid 19 deaths,recoveries and cases",inline = False)
    myEmbed2 = discord.Embed(title = "moderation commands",description = "you have to write '!r edit' to use commands",color = discord.Colour.dark_blue())
    myEmbed2.add_field(name = "!r edit servername {changed name} ",value = "changes the serves's name",inline = False)
    myEmbed2.add_field(name = "!r edit region {changed region}",value = "changes the region of your server",inline = False)
    myEmbed2.add_field(name = "!r edit ctx {new created text channel name}", value = "creates a new  text channel",inline = False )
    myEmbed2.add_field(name = "!r edit cvc {new created voice channel name}",value = "creates a new voice channel",inline =False)
    myEmbed2.add_field(name = "!r kick {user's name and tag}",value = "kicks the selected user",inline = False)
    myEmbed2.add_field(name = "!r ban",value = "bans a user",inline = False)
    myEmbed2.add_field(name = "!r clear {how many messages that you want to delete}",value = "deletes messages",inline = False )
    
    await context.send(embed = myEmbed)
    await context.send(embed = myEmbed2)


@bot.group()
async def edit(context):
    pass
@edit.command(pass_context = True)
@has_permissions(manage_guild = True)

async def servername(context,*,input):#making input as a one input
     await context.guild.edit(name = input)
     await context.send("succesfully changed the name of the server")

@edit.command(pass_context = True)
@has_permissions(administrator = True)

async def region(context,*,input):#making input as a one input
     await context.guild.edit(region = input)
     await context.send("succesfully changed the region to " + input)
@edit.command(pass_context = True)
@has_permissions(manage_channels = True)

async def ctx(context,*,input):#making input as a one input
    
     await context.guild.create_text_channel(name = input)
     await context.send("succesfully added " + input + " to the text channel")
@edit.command(pass_context = True)
@has_permissions(manage_channels = True)
async def cvc(context,*,input):#making input as a one input
    #going to go back and add
    
     await context.guild.create_voice_channel(name = input,)
     await context.send("succesfully added " + input + " to the text channel")
@bot.command(pass_context = True)
@has_permissions(kick_members = True)

async def kick(context,member : discord.Member,*, reason = None):

    await context.guild.kick(member,reason = reason)
    await context.send(f"kicked {member} succesfully")

@bot.command(pass_context = True)
@has_permissions(ban_members = True)

async def ban(context,member: discord.Member,*,reason = None):
    await context.guild.ban(member,reason = reason)
    await context.send(f"banned {member} succesfully")
@bot.command(pass_context = True)
@has_permissions(ban_members = True)
async def unban(ctx, *, input):
    name, discriminator = input.split("#")
    banned_members = await ctx.guild.bans()
    for bannedmember in banned_members:
        username = bannedmember.user.name
        disc = bannedmember.user.discriminator
        if name == username and discriminator == disc:
            await ctx.guild.unban(bannedmember.user)
            await ctx.send("unbanned succesfully")
@bot.command()
@has_permissions(manage_messages = True)
async def clear(context,amount,day:int = None,month: int = None ,year: int = datetime.now().year):
    if amount == "/":
        if day == None or month == None:
            return
        else:
            context.channel.purge(after = datetime(year,month,day))
    else:
        await context.channel.purge(limit = int(amount) + 1)
def is_me(context):
     return context.author.id == 817803939474047007
##ERROR HANDLERS
@clear.error
async def errorhandler(context,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await context.send("You have to specify either a date or number")
    if isinstance(error,commands.CommandInvokeError):
        await context.send("you can only have a slash or a  number as first input")

@kick.error
async def errorhandler(context,error):
    if isinstance(error,commands.errors.MemberNotFound):
        await context.send("there is no user named like that")
    if isinstance(error,commands.CommandInvokeError):
        await context.send("You dont have the permission!!")

@ban.error
async def errorhandler(context,error):
    if isinstance(error,commands.errors.MemberNotFound):
        await context.send("there is no user named like that")
    if isinstance(error,commands.CommandInvokeError):
        await context.send("You dont have the permission!")
@unban.error
async def errorhandler(context,error):
    if isinstance(error,commands.errors.MemberNotFound):
        await context.send("there is no user named like that")
    if isinstance(error,commands.CommandInvokeError):
        await context.send("You dont have the permission!")
@region.error
async def errorhandler(context,error):
    if isinstance(error,commands.errors.CommandInvokeError):
        await context.send("Pls enter a valid region name")
@ctx.error
async def errorhandler(context,error):
    if isinstance(error,commands.CommandInvokeError):
        await context.send("You dont have the permission!")
@cvc.error
async def errorhandler(context,error):
    if isinstance(error,commands.CommandInvokeError):
        await context.send("You dont have the permission!")






@bot.command()
async def python(context):
    python = discord.Embed(title = "python",description = "what is python",color = discord.Colour.dark_blue())
    python.set_thumbnail(url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/640px-Python-logo-notext.svg.png")
    python.add_field(name = "what is python",value = "Python is a programming language with objects, modules, threads, and automatic memory management.",inline = False)
    python.add_field(name = "what is python used for",value = "Python is a computer programming language often used to build websites and software, automate tasks, and conduct data analysis",inline = False)
    python.add_field(name = "hello world command",value = "print('hello world')",inline = False)
    await context.send(embed = python)
@bot.command()
async def javascript(context):
    js = discord.Embed(title = "java script",description = "what is java script",color = discord.Colour.green())
    js.set_thumbnail(url = "https://www.mehmetkirazli.com/wp-content/uploads/2014/02/javascript-dersleri-1280x720.jpg")
    js.add_field(name = "what is java script",value = "JavaScript is a scripting or programming language that allows you to implement complex features on web pages ",inline = False)
    js.add_field(name = "what is java script used for",value = "Javascript is used by programmers across the world to create dynamic and interactive web content like applications and browsers.",inline = False)
    js.add_field(name = "hello world command",value = "console.log('Hello, World!');",inline = False)
    await context.send(embed = js)
@bot.command()
async def java(context):
    java = discord.Embed(title = "java",description = "what is java",color = discord.Colour.green())
    java.set_thumbnail(url = "https://www.oracle.com/oce/press/assets/CONT2F6AE229113D42EC9C59FAED5BAA0380/native/og-social-java-logo.gif")
    java.add_field(name = "what is java",value = "Java is a programming language and computing platform first released by Sun Microsystems in 1995. It has evolved from humble beginnings to power a large share of today’s digital world, by providing the reliable platform upon which many services and applications are built. ",inline = False)
    java.add_field(name = "what is java used for",value = "One of the most widely used programming languages, Java is used as the server-side language for most back-end development projects, including those involving big data and Android development. Java is also commonly used for desktop computing, other mobile computing, games, and numerical computing",inline = False)
    java.add_field(name ="java hello world command",value = "public class hello{ \n public static void main(string args[]){\n System.out.println('hello world') \n } \n } ")
    await context.send(embed = java)
@bot.command()
async def date(context):
    import datetime
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    await context.send(f"{day}/{month}/{year}")

@bot.command()
async def wikipedia(context, *, input):
    import wikipedia
    result = wikipedia.summary(input,sentences = 2 )
    wikipe = discord.Embed(title = input ,description = result,color = discord.Colour.red())
    wikipe.set_thumbnail(url = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Wikipedia-logo-v2-tr.svg/1200px-Wikipedia-logo-v2-tr.svg.png")
    await context.send(embed = wikipe)
@bot.command()
async def covid(context):
    import requests
    r = requests.get("https://coronavirus-19-api.herokuapp.com/all")
    data = r.json()
    covid_data = f'confirmed cases: {data["cases"]} \n Deaths: {data["deaths"]} \n Recovered: {data["recovered"]}'
    covid = discord.Embed(title = "DAILY COVID CASES",description = "these are the daily covid cases,deaths and recoveries",color = discord.Colour.red())
    covid.set_thumbnail(url ="https://www.cumhuriyet.com.tr/Archive/2022/1/9/1898787/kapak_111006.jpg")
    covid.add_field(name = "confirmed cases: ",value = {data["cases"]},inline = False )
    covid.add_field(name = "Deaths:",value = {data["deaths"]},inline = False)
    covid.add_field(name = "recoveries",value = {data["recovered"]},inline = False )
    await context.send(embed = covid)
@bot.command()
async def weather(context,city):
            import requests
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=4c80c3cf38fbb5aa2482aafd65ba5891"
            res = requests.get(url)
            data = res.json()
            weather = data["weather"][0]["main"]
            temp = data["main"]["temp"] #fahrenheit
            desp = data["weather"] [0] ['description']
            temp = round((temp-32)*5/9) #to celcius
            weatherEmbed = discord.Embed(title = f'weather of city',color = discord.Colour.green())
            weatherEmbed.add_field(name = "degrees:",value = temp,inline = False)
            weatherEmbed.add_field(name = 'weather',value = weather,inline = False)
            weatherEmbed.add_field(name = "description",value = desp,inline = False)
            if desp == "clear sky":
                weatherEmbed.set_thumbnail(url = "https://cdn3.iconfinder.com/data/icons/weather-and-weather-forecast/32/sunny-512.png")
            elif desp == "few clouds": 
              weatherEmbed.set_thumbnail(url = "https://www.kindpng.com/picc/m/122-1227285_scattered-clouds-weather-symbol-hd-png-download.png")
            elif desp == "broken clouds":
                weatherEmbed.set_thumbnail(url = "https://static.thenounproject.com/png/2429843-200.png")
            elif desp == "scattered clouds":
                weatherEmbed.set_thumbnail(url = "https://flyclipart.com/thumb2/climate-cloud-cloudy-overcast-sky-sun-weather-icon-647424.png")
            elif desp == "rain":
                weatherEmbed.set_thumbnail(url = "data:image/jpeg;base64,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")
            
            await context.send(embed = weatherEmbed)
@bot.command()
@has_permissions(mute_members = True)

async def mute(context,user :discord.Member):
    await user.edit(mute = True)
    context.send(f"muted {user} succesfully")
@bot.command()
@has_permissions(mute_members = True)

async def unmute(context,user :discord.Member):
    await user.edit(mute = False)
    context.send(f"unmuted {user} succesfully")

@bot.command()
@has_permissions(deafen_members = True)

async def deafen(context,user :discord.Member):
    await user.edit(deafen = True)
    context.send(f"deafed{user} succesfully")
@bot.command()
@has_permissions(deafen_members = True)

async def undeafen(context,user :discord.Member):
    await user.edit(mute = False)
    await context.send(f"succesfully undeafed {user}")
@bot.command()
@has_permissions(mute_members = True)
async def voicekick (context,user :discord.Member):
    await user.edit(voice_channel = None)
    await context.send(f"succesfully kicked{user}")

@bot.command()
async def rps(ctx, hand):
    hands = ["✌️","✋","👊"]
    bothand = random.choice(hands)
    await ctx.send(bothand)
    if hand == bothand:
        await ctx.send("Its a Draw!")
    elif hand == "✌️":
        if bothand == "👊":
            await ctx.send("I won!")
        if bothand == "✋":
            await ctx.send("You won!")
    elif hand == "✋":
        if bothand == "👊":
            await ctx.send("You won!")
        if bothand == "✌️":
            await ctx.send("I won!")
    elif hand == "👊":
        if bothand == "✋":
            await ctx.send("I won!")
        if bothand == "✌️":
            await ctx.send("You won!")
#error handling
@mute.error
async def errorhandling(context,error):
    if isinstance(error,commands.CommandInvokeError):
        await context.send("pls enter a valid name")
@unmute.error
async def errorhandling(context,error):
    if isinstance(error,commands.CommandInvokeError):
        await context.send("pls enter a valid name")
@deafen.error
async def errorhandling(context,error):
    if isinstance(error,commands.CommandInvokeError):
        await context.send("pls enter a valid name")
@undeafen.error
async def errorhandling(context,error):
    if isinstance(error,commands.CommandInvokeError):
        await context.send ("enter a valid name")
@weather.error
async def errorhandling(context,error):
    if isinstance(error,commands.errors.MissingRequiredArgument):
        await context.send(" enter a valid place")

@bot.command()
async def unload(context):
    bot.unload_extension("cogs")
    await context.send("unloaded!")

@bot.command()
async def reload(context):
    bot.reload_extension("cogs")
    await context.send("reloaded")









bot.load_extension('cogs')
bot.run("enter your token")
