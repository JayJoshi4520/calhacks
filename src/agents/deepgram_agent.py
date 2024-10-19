from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from uagents import Model
import os
import ast
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs
from datetime import datetime, timedelta
from io import BufferedReader
from deepgram import DeepgramClientOptions
import logging

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    StreamSource,
    PrerecordedOptions,
)


def get_data():
    try:
        config = DeepgramClientOptions(
            verbose=verboselogs.SPAM,
        )
        deepgram = DeepgramClient("455f87ad3614a2faf17b24d07b892654e3e9f03b", config)


        with open(AUDIO_FILE, "rb") as stream:
            payload: StreamSource = {
                "stream": stream,
            }
            options = PrerecordedOptions(
                model="nova-2",
            )
            response = deepgram.listen.rest.v("1").transcribe_file(payload, options)


            print("Response received:")
            
            data = ast.literal_eval(response.to_json(indent=4))

            
            if isinstance(data, dict):
                transcript = data.get('results', {}).get('channels', [{}])[0].get('alternatives', [{}])[0].get('transcript', '')
                if transcript:
                    return str(transcript) 
                else:
                    print("No transcription available.")
            else:
                print("Unexpected response format.")

    except Exception as e:
        return -1


User_Address = 'agent1qdy3k24res4jxch5h8vzthjdfpy99xyxwstllmc6g9r3j9ul6qrh22jlag5'
Gemini_address = 'agent1qwg20ukwk97t989h6kc8a3sev0lvaltxakmvvn3sqz9jdjw4wsuxqa45e8l'  


class Message(Model):
    message: str


DeepGram_agent = Agent(
    name="Deep Gram Agent",
    port=8004,
    seed="Deep Gram Agent secret phrase",
    endpoint=["http://localhost:8004/submit"],
)


fund_agent_if_low(DeepGram_agent.wallet.address())







@DeepGram_agent.on_event("startup")
async def address(ctx: Context):
    ctx.logger.info(DeepGram_agent.address)
    message = str(input("You wanna Start Press Y: "))
    res = get_data()
    await ctx.send(Gemini_address, Message(message=res))
    
@DeepGram_agent.on_message(model=Message)
async def handle_query_response(ctx: Context, sender: str, msg: Message):
    message = str(input("You wanna Start Press Y: "))
    



    
    







