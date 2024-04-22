import re

from discord.ext import commands

class TimeConverter(commands.Converter):
    def __init__(self) -> None:
        self.__time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
        self.__time_dict = {"h":3600, "s":1, "m":60, "d":86400}

    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(self.__time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += self.__time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time