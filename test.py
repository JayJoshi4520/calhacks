# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from signal import SIGINT, SIGTERM
import asyncio
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs
from time import sleep

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

load_dotenv()

# We will collect the is_final=true messages here so we can use them when the person finishes speaking
is_finals = []


async def main():
        
    deepgram: DeepgramClient = DeepgramClient("455f87ad3614a2faf17b24d07b892654e3e9f03b")


    dg_connection = deepgram.listen.asyncwebsocket.v("1")
    async def on_message(self, result, **kwargs):
        global is_finals
        sentence = result.channel.alternatives[0].transcript
        if len(sentence) == 0:
            return
        if sentence.lower() == "close.":
            shutdown()
        if result.is_final:
            # We need to collect these and concatenate them together when we get a speech_final=true
            # See docs: https://developers.deepgram.com/docs/understand-endpointing-interim-results
            is_finals.append(sentence)

            # Speech Final means we have detected sufficent silence to consider this end of speech
            # Speech final is the lowest latency result as it triggers as soon an the endpointing value has triggered
            if result.speech_final:
                utterance = " ".join(is_finals)
                print(f"Speech Final: {utterance}")
                is_finals = []
            else:
                # These are useful if you need real time captioning and update what the Interim Results produced
                print(f"Is Final: {sentence}")
                await shutdown(SIGTERM, asyncio.get_event_loop(), dg_connection, microphone)
                return sentence
        else:
            # These are useful if you need real time captioning of what is being spoken
            print(f"Interim Results: {sentence}")


    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)


    # connect to websocket
    options: LiveOptions = LiveOptions(
        model="nova-2",
        language="en-US",
        # Apply smart formatting to the output
        smart_format=True,
        # Raw audio format deatils
        encoding="linear16",
        channels=1,
        sample_rate=16000,
        # To get UtteranceEnd, the following must be set:
        interim_results=True,
        utterance_end_ms="1000",
        vad_events=True,
        # Time in milliseconds of silence to wait for before finalizing speech
        endpointing=300,
    )

    addons = {
        # Prevent waiting for additional numbers
        "no_delay": "true"
    }

    print("\n\nStart talking! Press Ctrl+C to stop...\n")
    if await dg_connection.start(options, addons=addons) is False:
        print("Failed to connect to Deepgram")
        return

    # Open a microphone stream on the default input device
    microphone = Microphone(dg_connection.send)

    # start microphone
    microphone.start()

    # wait until cancelled
    microphone.finish()
    dg_connection.finish()

    print("Finished")



async def shutdown(signal, loop, dg_connection, microphone):
    print(f"Received exit signal {signal.name}...")
    microphone.finish()
    await dg_connection.finish()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    print(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    print("Shutdown complete.")


