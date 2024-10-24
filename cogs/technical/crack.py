import re
import hashlib
import asyncio
from discord.ext import commands

class Crack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='crack')
    async def identify_hash(self, ctx, hash_input):
        """
        Identifies the hash type and attempts to crack the password with rockyou.txt
        Example command: ^crack 68e109f0f40ca72a15e05cc22786f8e6
        """
        async with ctx.typing():
            result = await self.crack_password(hash_input)
        await ctx.send(result)

    async def crack_password(self, hash_input):
        """
        Attempts to crack the password for a given hash with rockyou.txt
        Example command: ^crack 68e109f0f40ca72a15e05cc22786f8e6
        """
        hash_formats = {
            'MD5': re.compile(r'^[0-9a-fA-F]{32}$'),
            'SHA-1': re.compile(r'^[0-9a-fA-F]{40}$'),
            'SHA-256': re.compile(r'^[0-9a-fA-F]{64}$'),
            'SHA-512': re.compile(r'^[0-9a-fA-F]{128}$'),
            'bcrypt': re.compile(r'^\$2[aby]\$[0-9]+\$[0-9a-zA-Z./]+'),
            'NTLM': re.compile(r'^[0-9a-fA-F]{32}:[0-9a-fA-F]{32}$'),
            'LM': re.compile(r'^[0-9a-fA-F]{16}$'),
            # Add more hash formats as needed
        }

        hash_type = None
        for type_, regex in hash_formats.items():
            if regex.match(hash_input):
                hash_type = type_
                break

        if hash_type is None:
            return 'Invalid hash format'

        async def check_and_delay(password, delay=0.1):
            await asyncio.sleep(delay)
            return f'Password found: {password} for hash type: {hash_type}'

        rockyou_path = 'rockyou.txt'  # Update with the correct path
        with open(rockyou_path, 'r', encoding='latin-1') as file:
            for password in file:
                password = password.strip()
                hashed_password = self.hash_password(password, hash_type)
                if hashed_password == hash_input:
                    return await check_and_delay(password)

        return f'No password match found for the given hash type'

    def hash_password(self, password, hash_type):
        if hash_type == 'MD5':
            return hashlib.md5(password.encode()).hexdigest()
        elif hash_type == 'SHA-1':
            return hashlib.sha1(password.encode()).hexdigest()
        elif hash_type == 'SHA-256':
            return hashlib.sha256(password.encode()).hexdigest()
        elif hash_type == 'SHA-512':
            return hashlib.sha512(password.encode()).hexdigest()
        elif hash_type == 'bcrypt':
            return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        elif hash_type == 'NTLM':
            return hashlib.new('md4', password.encode('utf-16le')).hexdigest()
        elif hash_type == 'LM':
            return hashlib.new('lm', password.encode()).hexdigest()[:16]

        return None  # Return None if the hash_type is not recognized

async def setup(bot):
    await bot.add_cog(Crack(bot))
