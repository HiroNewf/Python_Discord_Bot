import requests
from discord.ext import commands

class URLChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='URL_Checker')
    async def check_url_safety(self, ctx, url):
        """
        Checks the safety of a given URL using Google Safe Browsing API.
        :param url: The URL to check.
        """
        async with ctx.typing():
            result = await self.check_url_safety_google_api(url)
        await ctx.send(result)

    async def check_url_safety_google_api(self, url):
        """
        Checks the safety of a given URL using Google Safe Browsing API.
        :param url: The URL to check.
        :return: A message indicating whether the URL is safe or not.
        """
        # Google Safe Browsing API Endpoint
        api_endpoint = 'https://safebrowsing.googleapis.com/v4/threatMatches:find'

        # Request payload
        payload = {
            "client": {
                "clientId": "your-client-id",
                "clientVersion": "1.0"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "THREAT_TYPE_UNSPECIFIED", "UNWANTED_SOFTWARE"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [
                    {"url": url}
                ]
            }
        }

        # Headers
        headers = {
            "Content-Type": "application/json"
        }

        # Send request to Google Safe Browsing API
        response = requests.post(f"{api_endpoint}?key={google_api_key}", json=payload, headers=headers)

        # Check response
        if response.status_code == 200:
            json_response = response.json()
            if 'matches' in json_response and json_response['matches']:
                return f"The URL '{url}' is NOT safe according to Google Safe Browsing API."
            else:
                return f"The URL '{url}' is safe according to Google Safe Browsing API."
        else:
            return f"Failed to check the safety of the URL '{url}' using Google Safe Browsing API."

async def setup(bot):
    await bot.add_cog(URLChecker(bot))
