# Importing necessary libraries
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from uagents import Model
import google.generativeai as genai



LMNT_API_KEY = 'agent1q0apuzjk92w9x4rsrcaz2agpnl0hlu9xh468ccu66lhdq37z82n6sjdgq7f'



class Message(Model):
    message: str

class Response(Model):
    text: str

Gemini_agent = Agent(
    name="Gemini Agent",
    port=8001,
    seed="Gemini Agent secret phrase",
    endpoint=["http://localhost:8001/submit"],
)


fund_agent_if_low(Gemini_agent.wallet.address())


genai.configure(api_key="AIzaSyBLvM9A5jxeU3q1UXBuM_MVE1eV2E73l-g") 


model = genai.GenerativeModel("gemini-pro")


chat = model.start_chat(history=[])

inappropriate_words = [
    "violence", "kill", "murder", "blood", "gore", "death", 
    "drugs", "alcohol", "intoxicated", "gambling", 
    "sex", "nude", "porn", "prostitute", "abuse", "slavery", 
    "bomb", "terrorist", "gun", "knife", "suicide",
    "racism", "hate", "discrimination", "slur", 
    "curse", "swear", "damn", "hell", 
    "f***", "s***", "b****", "a**", "c***",
    "homophobic", "transphobic", "xenophobia", "misogyny"
]

print("Chat session has started. Type 'quit' to exit.")

def filter_inappropriate(text, inappropriate_words):
    words = text.split()
    for word in words:
        if word in inappropriate_words:
            return True


async def handle_message(message):
    while True:

        user_message = message + "make santance structure so that childeren can understand and ignore inappropriate content"



        if user_message.lower() == "quit":
            return "Exiting chat session."


        response = chat.send_message(user_message, stream=True)


        full_response_text = []


        for chunk in response:
            full_response_text.append(str(chunk.text))

        return full_response_text



@Gemini_agent.on_event("startup")
async def address(ctx: Context):

    ctx.logger.info(Gemini_agent.address)



@Gemini_agent.on_message(model=Message)
async def handle_query_response(ctx: Context, sender: str, msg: Message):

    message = await handle_message(msg.message)
    print("Bellow is type in gemini")
    print(type(message))
    ctx.logger.info(message)
    await ctx.send(LMNT_API_KEY, Message(message=str(message)))

@Gemini_agent.on_query(model=Message, replies={Response})
async def handle_query_api_response(ctx: Context, sender: str, msg: Message):

    try: 
        response = await handle_message(msg.message)
        print("Bellow is type in gemini")
        print(type(response))
        ctx.logger.info(response)
        await ctx.send(sender, Response(text=str(response)))
    except Exception:
        await ctx.send(sender, Response(text="fail"))
