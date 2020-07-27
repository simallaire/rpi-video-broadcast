import time
import hashlib
import os
import cv2
import asyncio
import pathlib
import ssl
import websockets
import pickle
import signal
import logging

import numpy as np

from pprint import pprint


# Used by docker-compose down
def sigterm_handler(signal, frame):
    logger.info("Reacting to SIGTERM")
    teardown()
    exit(0)


def teardown():
    asyncio.get_event_loop().call_soon_threadsafe(
        asyncio.get_event_loop().stop)


logging.basicConfig(
    format='[%(asctime)s] %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

def prepare_data():

    buffer_size = int(video_capture.get(cv2.CAP_PROP_BUFFERSIZE))

    for i in range(buffer_size):
        success, drop = video_capture.read()

        logger.info("Dropped rgb frame")

        if not success:
            break

    success, rgb_frame = video_capture.read()
    data = pickle.dumps(rgb_frame)
    return data


async def send_frame(websocket, path):
    while True:
        logger.info("Sending frames")
        await websocket.send(prepare_data())
        #await asyncio.sleep(1)



start_server = websockets.serve(
    send_frame, port=8888 #, ssl=ssl_context
)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


