from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from uagents import Model

import playsound

class Message(Model):
    message: str


Gemini_Address = "agent1qwg20ukwk97t989h6kc8a3sev0lvaltxakmvvn3sqz9jdjw4wsuxqa45e8l" 



def play_output():
    playsound('../output.wav')

user = Agent(
    name="user",
    port=8000,
    seed="user secret phrase",
    endpoint=["http://localhost:8000/submit"],
)


fund_agent_if_low(user.wallet.address())


@user.on_event("startup")
async def agent_address(ctx: Context):
    ctx.logger.info(user.address)
    message = str(input("You:"))
    await ctx.send(Gemini_Address, Message(message=message))

@user.on_message(model=Message)
async def handle_query_response(ctx: Context, sender: str, msg: Message):
    message = str(input("You:"))
    print("This is user: " + sender)
    play_output()
