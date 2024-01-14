# PWN_Discord_Bot-WIP
## General 
PWN is a discord bot built in python that provides many different commands, but its main focus is useful cybersecurity commands for both technical and non technical users. This bot is very much a work in progress and will continue to get new commands and updates as times goes on. For now its primiary functions are telling the time in any timezone, cracking password hashes with the rockyou.txt wordlist, and checking URL's for suspicious content using the Google Safe Browsing API. Feel free to contribute to this project or fork and/or self host the bot and use it for your own purposes. This is and will continue to be a completely open source project. For more information about self hosting the bot reference the bottom of this readme. 

## Commands
PWN has a handful of useful commands and uses the prefix '^':

* `^help`: A general help command that lists out all of the commands the bot supports and provides general useage information as well as command examples
* `^hello`: A greeting/testing command. This command should just respond with "Hello!" and is mainly just used as a sort of ping command to make sure the bot is up
* `^time`: Displays the time and allows for an optional timezone arguement that supports a varity of timezone formats (ETC, UTC+04:00, America/New_York). If no timezone arguement is given by the user than it will default to the user's set timezone, if the user has no set timezone than it will default to UTC time. 
  * Examples:
    * `^time JST`
    * `^time`
    * `^time UTC-06:00`
    * `^time Asia/Shanghai`
* `^settimezone [timezone]`: Sets the timezone for the user running the command (this will be their default timezone when running the `^time` command with no provided timezone arguement). Supports all of the known timezone formats that the `^time` command does.   
  * Example: `^settimezone America/Anchorage`
* `^crack`: Identifies the hash type provided and then attempts to crack the hash with the rockyou.tct wordlist. If the hash it cracked it will output the password and the hash type. If the password is not found the user will be informed that that is the case. 
  * Example: `^crack 68e109f0f40ca72a15e05cc22786f8e6`
* `^URL_Checker`: Runs the provided URL against the Google's Safe Browsing database to try and determine is the URL is safe or not and then outputs said informaiton to the user. 
  * Example: `^URL_Checker https://google.com`

## Self Hosting / Usage 


Eh I'll make this ReadMe later, but hey look! The bot does things... sometimes
![image](https://github.com/HiroNewf/Python_Discord_Bot/assets/64501695/e86236de-ae85-44ef-a3b2-32b48f4d5b18)
