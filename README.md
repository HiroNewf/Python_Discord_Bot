# PWN_Discord_Bot

## General
PWN is a discord bot built in python that provides many different commands, but its main focus is useful cybersecurity commands for both technical and non technical users. This bot is very much a work in progress and will continue to get new commands and updates as times goes on. For now its primary functions are telling the time in any timezone, cracking password hashes with the rockyou.txt wordlist, and checking URL's for suspicious content using the Google Safe Browsing API. Feel free to contribute to this project or fork and/or self host the bot and use it for your own purposes. This is and will continue to be a completely open source project. For more information about self hosting the bot reference the bottom of this readme. To invite this bot to your own discord server go [here](https://discord.com/oauth2/authorize?client_id=1190778555903258765&permissions=8&scope=bot) if you want the bot to have Administrator privileges (future proof option) and [here](https://discord.com/api/oauth2/authorize?client_id=1190778555903258765&permissions=3072&scope=bot) if you just want the current necessary privileges for the bot (good for a policy of least privileges but may break if I add new commands to the bot that require more permissions).

## Commands
PWN has a handful of useful commands and uses the prefix '^':

### General Commands
- `^help`: A general help command that lists out all of the commands the bot supports and provides general usage information as well as command examples
- `^advanced_help`: Shows the help page for advanced commands.
- `^whoami`: Provides information about the bot, including its purpose and how to contribute.
- `^hello`: A greeting/testing command. This command should just respond with "Hello!" and is mainly just used as a sort of ping command to make sure the bot is up
- `^time`: Displays the time and allows for an optional timezone argument that supports a variety of timezone formats (ETC, UTC+04:00, America/New_York). If no timezone argument is given by the user than it will default to the user's set timezone, if the user has no set timezone than it will default to UTC time.
    - Examples:
        - `^time JST`
        - `^time`
        - `^time UTC-06:00`
        - `^time Asia/Shanghai`
- `^settimezone [timezone]`: Sets the timezone for the user running the command (this will be their default timezone when running the `^time` command with no provided timezone argument). Supports all of the known timezone formats that the `^time` command does.
    - Example: `^settimezone America/Anchorage`
### Technical Commands
- `^crack [hash]`: Identifies the hash type provided and then attempts to crack the hash with the rockyou.tct wordlist. If the hash it cracked it will output the password and the hash type. If the password is not found the user will be informed that that is the case.
    - Example: `^crack 68e109f0f40ca72a15e05cc22786f8e6`
- `^URL_Checker [URL]`: Runs the provided URL against the Google's Safe Browsing database to try and determine is the URL is safe or not and then outputs that information to the user.
    - Example: `^URL_Checker https://google.com`
### Advanced Commands
> Note: the bot does not store any of the emails/passwords you run through these commands, even in the logs, but if still do not want to risk exposing this information you can do to the Have I Been Pwned website or self host the bot to achieve the same results with less risk on your part. These commands are mostly a proof of concept and are not the best way at making sure your data is secure.
- `^advanced_commands`: A command used to enable or disable all of the advanced commands of this discord bot, it is set to disabled by default.
 - Examples:
    - `^advanced_commands enable`
    - `^advanced_commands disable`
- `^email_checker`: This command will take the provided email and check it against Have I Been Pwned database to see if it has been exposed in any known breaches. Please do **NOT** provide your email as an argument for the command, the bot will DM you for the email after you run the `^email_checker` command with no arguments. 
- `^password_checker`: This command will take the provided password and check it against Have I Been Pwned database to see if it has been exposed in any known breaches. Please do **NOT** provide your password as an argument for the command, the bot will DM you for the email after you run the `^password_checker` command with no arguments.
## Self Hosting / Usage
Currently I do not have a server setup to host this bot so it is just being hosted by a VM of mine on my primary computer. This of course means that it's uptime is terrible and while I do plan to fix this issue in the future, you may be interested in hosting the bot yourself. Rather you want to host it in it's current form you wish to add more commands / changes and then host your forked version the steps will be the same and I will give a high level overview of those steps below.

1. Download the source-code: you need the `bot.py` file as well as the two json files in this repo.
2. Setup a bot page for yourself using Discord's Developer Portal and acquire a TOKEN for your bot.
3. Replace the placeholder of "your_bot_token_here" in the config.json file with your bot token (do not expose this publicly).
4. Get yourself a Google API key by going to the Google Cloud Console, starting a new project and generating an API key for yourself (do not expose this publicly).
5. Take your Google API key and replace the placeholder of "your_google_api_key_here" in the api_keys.json file with your API key.
6. Get an API key for Have I Been Pwned [here](https://haveibeenpwned.com/API/Key) (or skip this step if you do not desire to use the advanced commands of this bot)
7. Take your HIBP API key and replace the placeholder of "your_hibp_api_key_here" in the api_keys.json file with your API key
8. Generate an invite URL for your bot in the OAuth2 tab of your Discord Developers page. Select "bot" for the scope and currently the bot only needs the permissions of "Send Messages" and "Read Messages/View Channels", this may change in the future and you could always just select Administrator privileges for the sake of future proofing.
9. Copy and paste the link into a new tab in your browser and select the discord server you want to add the bot to. (Make sure you have the permissions in said discord server to invite bots with whatever perms you gave the bot in the previous step).
10. Download the rockyou.txt wordlist from github and place it in the same directory as your bot.py file.
11. Download the 'Dog' folder in this repo and place it in the same directory as your bot.py file. 
12. Go to the computer/VM that you will be hosting the bot on and run the `bot.py` file with the command `python3 bot.py`. This should start up the bot and changes its discord activity status from invisible to online. Now the bot should respond to commands and everything should work as intended.
13. Make sure to check back on this repo regularly and update your bot.py file to the newest version to continue to get patches and updates for your self hosted version of the bot. 

**Note**: Something useful to know if you are self hosting is that the bot create log files. Within the working directory of the bot it will create a folder called 'Logs' and within that folder it will create more folders for each month its year in the format of 'January 2024'. Within each of the these month folders will be .log files timestamped with the day they were created and each event within said log will also be timestamped. This could prove to be helpful when setting up and troubleshooting the bot, especially if you find yourself making modifications to the code. 
