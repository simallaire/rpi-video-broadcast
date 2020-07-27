import asyncio
import pathlib
import ssl
import websockets
import pickle
import argparse
import cv2
import numpy as np
from timeit import default_timer as timer

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server-ip", type=str,
                    help="Specify the server's ip")
parser.add_argument("-d", "--delay", type=int,
                    help="Delay between frames")
args = parser.parse_args()

async def fetch_frames():
    if args.server_ip:
        uri = "ws://"+args.server_ip+":8888"


    async with websockets.connect(
        uri
    ) as websocket:
        i = 0
        start = timer()
        while True:
            i = i + 1
            data = await websocket.recv()
            frames = pickle.loads(data, fix_imports=True, encoding="bytes")
            cv2.imshow("RGB", frames)
            if args.delay:
                cv2.waitKey(int(args.delay))
            else:
                cv2.waitKey(1000)
            end = timer()
            print("Frame {}: {:.2f}sec / {:.2f}fps".format(i, (end-start), 1/(end-start)))
            start = timer()
asyncio.get_event_loop().run_until_complete(fetch_frames())

