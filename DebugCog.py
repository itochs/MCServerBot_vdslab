from discord import Guild, Member, Role, TextChannel
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

from MCServerBot import MCServerBot
from serverstatus import ServerStatus


class Debug(commands.Cog):
    def __init__(self, bot : MCServerBot) -> None:
        super().__init__()
        self.bot : MCServerBot = bot
        self.server_admin_id : int = 851408507194572821
        self.mc_channel = self.bot.get_channel(965978774963359817)
        self.guild : Guild = self.bot.get_guild(965978774963359814)
        self.server_admin_roll : Role = self.guild.get_role(1040592221264683099)
    
    
    @commands.command()
    async def debug(self, context : Context):
        if __debug__:
            user = context.message.author
            if(type(user) is not Member):
                print(type(user))
                return
            user : Member
            user_role  = user.get_role(1040592221264683099)
            user_has_admin_role = user_role and user_role is self.server_admin_roll
            user_is_admin = user.id == self.server_admin_id
            if not user_has_admin_role and not user_is_admin:
                await context.send("you are not admin")
                return
            
            await context.send("you are admin!!")
            if self.loopDebug.is_running():
                await context.send("stop loop @851408507194572821")
                self.loopDebug.cancel()
            else:
                await context.send("start loop @851408507194572821")
                self.loopDebug.start()
                
    
    @tasks.loop(seconds=10)
    async def loopDebug(self):
        if __debug__:
            await self.mc_channel.send("loop")

def setup(bot):
    return bot.add_cog(Debug(bot=bot))
