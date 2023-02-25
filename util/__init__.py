from .JsonHandler import JsonHandler
import os
import openai
from dotenv import load_dotenv

load_dotenv()

config = os.environ
openai.api_key = config['OPENAI_API_KEY']

threads = JsonHandler('threads.json')
SEPARATOR = '\n'

def chatGPT(prompt, preppend=None):
    preppend = (
        '(You are a discord bot called MemBot who reminds us to do our Membean '
        'vocabulary homework. Your response must relate to Membean. Mention Mem'
        'bean. Three 15 minute sessions of Membean MUST be done each week. Only'
        ' one 15 minute session can be completed per day.)'
    ) if not preppend else preppend
    
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f'{preppend}{SEPARATOR}{prompt}',
        temperature=0.5,
        max_tokens=2000,
        n=1,
        stop=None,
    )
    return response.choices[0].text.strip()

async def initial_message(message, client): return (
    f'{message.author.display_name}: ' + ' '.join((
        await message.channel.parent.fetch_message(message.channel.id)
    ).content.split(client.command_prefix)[-1].split(' ')[1:])
)