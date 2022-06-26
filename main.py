import time
from typing import List
import socket
import lightbulb
from hikari import GatewayBot, intents, Embed, Color
from hikari.events import MessageCreateEvent
from pathlib import Path
from rules import MessageRule, MessageRules
import yaml
import re
from lightbulb import BotApp, SlashContext, MessageContext
import os
import ipaddress
import dotenv

from shodan import Shodan

dotenv.load_dotenv()

if not Path('rules.yaml').exists():
    raise Exception('Brak pliku z zasadami')

with open('rules.yaml', 'r') as rules_file:
    rules: MessageRules = MessageRules(__root__=yaml.safe_load(rules_file))

print(rules.__root__, sep='\n')
bot = BotApp(os.getenv('DISCORD_BOT_TOKEN'), prefix='shodan ', intents=intents.Intents.ALL)
sh = Shodan(os.getenv('SHODAN_API_TOKEN'))


@bot.listen(MessageCreateEvent)
async def print_any_event(event: MessageCreateEvent):
    if event.message.content is None:
        return

    for rule in rules.__root__:
        if re.match(rule.regex_pattern, event.message.content):
            await event.message.respond(rule.response)


def sanitize_addr(maybe_ip: str):
    try:
        ipaddress.ip_address(maybe_ip)
        return maybe_ip
    except ValueError:
        try:
            return socket.gethostbyname(maybe_ip)
        except socket.gaierror:
            return None


@bot.command()
@lightbulb.option('host', 'ip hosta')
@lightbulb.command('ping', 'wysyła pong')
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.MessageCommand)
async def ping(ctx: SlashContext | MessageContext):
    valid_ip = sanitize_addr(ctx.options['host'] or ctx.options.target.content)
    if valid_ip is None:
        await ctx.respond('To nie jest poprawny adres ip lub nazwa hosta!')
        return

    r = await sh.get_host(valid_ip)
    embed = Embed()
    embed.title = 'Ping details'
    for f in r.__fields__:
        embed.add_field(f, r.__getattribute__(f))
    embed.color = Color.from_hex_code('9099FF')
    await ctx.respond(embed=embed)

if __name__ == '__main__':
    bot.run()
