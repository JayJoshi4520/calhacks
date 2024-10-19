from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from uagents import Model
from lmnt.api import Speech
import base64
from pydub import AudioSegment
from pydub.playback import play
import playsound
import ast

DeepGram_Address = 'agent1qgumx6glkn32u2te9dnan666acnwqq6mdk4r9g3ps5dvqaw5dnd6w7v2v9v'
LMNT_API_KEY = '09dabaa99b474797a6df69afaa3721d7'  


class Message(Model):
    message: str



LMNT_agent = Agent(
    name="LMNT Agent",
    port=8003,
    seed="LMNT Agent secret phrase",
    endpoint=["http://localhost:8003/submit"],
)


fund_agent_if_low(LMNT_agent.wallet.address())


def play_output(subfile):
    song = AudioSegment.from_wav(subfile)
    play(song)



@LMNT_agent.on_event("startup")
async def address(ctx: Context):

    ctx.logger.info(LMNT_agent.address)


@LMNT_agent.on_message(model=Message)
async def handle_query_response_LMNT(ctx: Context, sender: str, msg: Message):
    count = 0
    async with Speech(LMNT_API_KEY) as speech:
        full_message = ast.literal_eval(msg.message)
        for sentences in full_message:
            synthesis = await speech.synthesize(sentences, voice='lily', format='wav')
            with open(f'output{count}.wav', 'wb') as f:
                f.write(synthesis['audio'])
                play_output(f'output{count}.wav')
                count += 1
    await ctx.send(DeepGram_Address, Message(message="Audio has been Generated"))
    







