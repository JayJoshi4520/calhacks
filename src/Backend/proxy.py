from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import base64

# Define FastAPI app
app = FastAPI()

# The URL where your LMNT agent is running
AGENT_URL = "http://localhost:8003/submit"

# Request model for FastAPI
class BlobRequest(BaseModel):
    message: str  # The message containing sentences to be converted into audio

# Response model for FastAPI
class BlobResponse(BaseModel):
    blobs: list[str]  # List of base64-encoded wav files

# The URL where your Gemini agent is running
GEMINI_AGENT_URL = "http://localhost:8001/submit"

# Request model for FastAPI
class MessageRequest(BaseModel):
    message: str  # The message to be sent to the Gemini agent

# Response model for FastAPI
class MessageResponse(BaseModel):
    text: str  # The response text returned by the Gemini agent


# Endpoint to forward requests to the LMNT agent
@app.post("/generate_audio/")
async def generate_audio(req: BlobRequest):
    try:
        # Prepare the request data for the LMNT agent
        agent_request = {
            "blob_data": req.message
        }
        
        # Send the POST request to the LMNT agent
        response = requests.post(AGENT_URL, json=agent_request)

        # Check if the request to the agent was successful
        if response.status_code == 200:
            response_data = response.json()  # Extract the response from the agent
            
            # Return the array of base64-encoded .wav blobs as the response
            return BlobResponse(blobs=response_data["blobs"])
        else:
            raise HTTPException(status_code=response.status_code, detail="Agent call failed")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with agent: {str(e)}")


# Endpoint to forward requests to the Gemini agent
@app.post("/send_message/")
async def send_message(req: MessageRequest):
    try:
        # Prepare the request data for the Gemini agent
        agent_request = {
            "message": req.message
        }
        
        # Send the POST request to the Gemini agent
        response = requests.post(GEMINI_AGENT_URL, json=agent_request)

        # Check if the request to the agent was successful
        if response.status_code == 200:
            response_data = response.json()  # Extract the response from the agent
            
            # Return the agent's response
            return MessageResponse(text=response_data["text"])
        else:
            raise HTTPException(status_code=response.status_code, detail="Agent call failed")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with agent: {str(e)}")


# Example of how to start FastAPI (in the command line, not in this script)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
