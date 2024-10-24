# PWN_Discord_Bot

## General
PWN is a discord bot built in python that is very much a work in progress and will continue to get new commands and updates as times goes on. To invite this bot to your own discord server go [here](https://discord.com/api/oauth2/authorize?client_id=1190778555903258765&permissions=3072&scope=bot).

## Commands
PWN has a handful of useful commands and uses the prefix '^':

### General Commands
- `^help`: A general help command that lists out all of the commands the bot supports and provides general usage information as well as command examples
- `^hello`: A greeting/testing command. This command should just respond with "Hello!" and is mainly just used as a sort of ping command to make sure the bot is up
- `^dog`: Gives you a random picture of a dog (out of like 5 images, but whatever) 
- `^time`: Displays the time and allows for an optional timezone argument that supports a variety of timezone formats (ETC, UTC+04:00, America/New_York). If no timezone argument is given by the user than it will default to the user's set timezone, if the user has no set timezone than it will default to UTC time.
    - Examples:
        - `^time JST`
        - `^time`
        - `^time UTC-06:00`
        - `^time Asia/Shanghai`
- `^settimezone [timezone]`: Sets the timezone for the user running the command (this will be their default timezone when running the `^time` command with no provided timezone argument). Supports all of the known timezone formats that the `^time` command does.
    - Example: `^settimezone America/Anchorage`
- `^poll [question] [options...]`: Creates a poll with the given question and options. You can provide up to 9 options.
    - Example: `^poll What's your favorite color? Red Blue Green`
- `^translate [language] [text]`: Translates the provided text into the specified language.
    - Example: `^translate es Hello, world!`
- `^8ball [question]`: Ask the magic 8-ball a question and receive an answer.
    - Example: `^8ball Will it rain today?`
- `^role_info [role_name]`: Provides information about a specific role, including members who have that role.
    - Example: `^role_info Admin`
### Technical Commands
- `^crack [hash]`: Identifies the hash type provided and then attempts to crack the hash with the rockyou.txt wordlist. If the hash it cracked it will output the password and the hash type. If the password is not found the user will be informed that that is the case.
    - Example: `^crack 68e109f0f40ca72a15e05cc22786f8e6`
- `^URL_Checker [URL]`: Runs the provided URL against the Google's Safe Browsing database to try and determine is the URL is safe or not and then outputs that information to the user.
    - Example: `^URL_Checker https://google.com`

### Resource Link Commands
- `^resumeguide`: Provides the link to Hiro's resume guide.
- `^templates`: Provides the link Hiro's resume templates and examples.
- `^blog`: Provides the link to Hiro's blog.
- `^forfoxsake`: Provides the link to Erubius's website & blog.
- `^fivepillars`: Provides the link to the fivepillars github page.

### Moderation Commands 
- `^kick @user [reason]`: Kicks a user from the server with an optional reason.
- `^ban @user [reason]`: Bans a user from the server with an optional reason.
- `^timeout @user [time in seconds] [reason]`: Temporarily mutes a user for a specified amount of time.
- `^rename @user [new nickname]`: Renames a user to the specified nickname on the server.

## Self Hosting / Usage
Currently I do not have a server setup to host this bot so it is just being hosted by a VM of mine on my primary computer. This of course means that it's uptime is terrible and while I do plan to fix this issue in the future, you may be interested in hosting the bot yourself. Whether you want to host it in it's current form you wish to add more commands / changes and then host your forked version the steps will be the same and I will give a high level overview of those steps below.

1. Clone the repo.
2. Setup a bot page for yourself using Discord's Developer Portal and acquire a TOKEN for your bot.
3. Replace the placeholder of "your_bot_token_here" in the config.json file with your bot token (do not expose this publicly).
4. Get yourself a Google API key by going to the Google Cloud Console, starting a new project and generating an API key for yourself (do not expose this publicly).
5. Take your Google API key and replace the placeholder of "your_google_api_key_here" in the api_keys.json file with your API key.
6. Generate an invite URL for your bot in the OAuth2 tab of your Discord Developers page. Select "bot" for the scope and currently the bot only needs the permissions of "Send Messages" and "Read Messages/View Channels", this may change in the future and you could always just select Administrator privileges for the sake of future proofing.
7. Copy and paste the link into a new tab in your browser and select the discord server you want to add the bot to. (Make sure you have the permissions in said discord server to invite bots with whatever perms you gave the bot in the previous step).
8. Run the `bot.py` file with the command `python3 bot.py`. This should start up the bot and changes its discord activity status from invisible to online. Now the bot should respond to commands and everything should work as intended.
9. Make sure to check back on this repo regularly and update your bot.py file to the newest version to continue to get patches and updates for your self hosted version of the bot. 

> **Note**: Something useful to know if you are self hosting is that the bot create log files. Within the working directory of the bot it will create a folder called 'Logs' and within that folder it will create more folders for each month its year in the format of 'January 2024'. Within each of the these month folders will be .log files timestamped with the day they were created and each event within said log will also be timestamped. This could prove to be helpful when setting up and troubleshooting the bot, especially if you find yourself making modifications to the code. 
