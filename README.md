# PWN_Discord_Bot

## General
PWN is a discord bot built in python that provides many different commands, but its main focus is useful cybersecurity commands for both technical and non technical users. This bot is very much a work in progress and will continue to get new commands and updates as times goes on. For now its primary functions are telling the time in any timezone, cracking password hashes with the rockyou.txt wordlist, and checking URL's for suspicious content using the Google Safe Browsing API. Feel free to contribute to this project or fork and/or self host the bot and use it for your own purposes. This is and will continue to be a completely open source project. For more information about self hosting the bot reference the bottom of this readme. To invite this bot to your own discord server go [here](https://discord.com/oauth2/authorize?client_id=1190778555903258765&permissions=8&scope=bot) if you want the bot to have Administrator privileges (future proof option) and [here](https://discord.com/api/oauth2/authorize?client_id=1190778555903258765&permissions=3072&scope=bot) if you just want the current necessary privileges for the bot (good for a policy of least privileges but may break if I add new commands to the bot that require more permissions).

## Commands
PWN has a handful of useful commands and uses the prefix '^':

- `^help`: A general help command that lists out all of the commands the bot supports and provides general usage information as well as command examples
- `^hello`: A greeting/testing command. This command should just respond with "Hello!" and is mainly just used as a sort of ping command to make sure the bot is up
- `^time`: Displays the time and allows for an optional timezone argument that supports a variety of timezone formats (ETC, UTC+04:00, America/New_York). If no timezone argument is given by the user than it will default to the user's set timezone, if the user has no set timezone than it will default to UTC time.
    - Examples:
        - `^time JST`
        - `^time`
        - `^time UTC-06:00`
        - `^time Asia/Shanghai`
- `^settimezone [timezone]`: Sets the timezone for the user running the command (this will be their default timezone when running the `^time` command with no provided timezone argument). Supports all of the known timezone formats that the `^time` command does.
    - Example: `^settimezone America/Anchorage`
- `^crack [hash]`: Identifies the hash type provided and then attempts to crack the hash with the rockyou.tct wordlist. If the hash it cracked it will output the password and the hash type. If the password is not found the user will be informed that that is the case.
    - Example: `^crack 68e109f0f40ca72a15e05cc22786f8e6`
- `^URL_Checker [URL]`: Runs the provided URL against the Google's Safe Browsing database to try and determine is the URL is safe or not and then outputs that information to the user.
    - Example: `^URL_Checker https://google.com`

## Self Hosting / Usage
Currently I do not have a server setup to host this bot so it is just being hosted by a VM of mine on my primary computer. This of course means that it's uptime is terrible and while I do plan to fix this issue in the future, you may be interested in hosting the bot yourself. Rather you want to host it in it's current or add more commands / changes and then host your forked version the steps will be the same and I will give a high level overview of those steps below.

1. Download the source-code: you need the `bot.py` file as well as the two json files in this repo.
2. Setup a bot page for yourself using Discord's Developer Portal and acquire a TOKEN for your bot.
3. Replace the placeholder of "your_bot_token_here" in the config.json file with your bot token (do not expose this publicly).
4. Get yourself a Google API key by going to the Google Cloud Console, starting a new project and generating an API key for yourself (do not expose this publicly).
5. Take your Google API key and replace the placeholder of "your_google_api_key_here" in the api_keys.json file with this API key.
7. Generate an invite URL for your bot in the OAuth2 tab of your Discord Developers page. Select "bot" for the scope and currently the bot only needs the permissions of "Send Messages" and "Read Messages/View Channels", this may change in the future and you could always just select Administrator privileges for the sake of future proofing.
8. Copy and paste the link into a new tab in your browser and select the discord server you want to add the bot to. (Make sure you have the permissions in said discord server to invite bots with whatever perms you gave the bot in the previous step).
9. Download the rockyou.txt wordlist from github and place it in the same directory as your bot.py file.
10. Go to the computer/VM that you will be hosting the bot on and run the `bot.py` file with the command `python3 bot.py`. This should start up the bot and changes its discord activity status from invisible to online. Now the bot should respond to commands and everything should work as intended.
11. Make sure to check back on this repo regularly and update your bot.py file to the newest version to continue to get patches and updates for your self hosted version of the bot. 
