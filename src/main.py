from agents.user import user 
from agents.gemini_agent import Gemini_agent  
from agents.lmnt_agent import LMNT_agent
from agents.deepgram_agent import DeepGram_agent


from uagents import Bureau


if __name__ == "__main__":

    bureau = Bureau(endpoint="http://127.0.0.1:5000/submit", port=8000)

    bureau.add(DeepGram_agent)
    bureau.add(LMNT_agent)
    bureau.add(Gemini_agent)

    bureau.run()
