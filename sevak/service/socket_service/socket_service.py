# Objective : To open a websocket connection with some ${HOST} and some ${PORT}.
from webbrowser import get
from service import camera_service
import websockets
import asyncio
import os
import json

from configs import config
from collections import OrderedDict
from configparser import ConfigParser
from agents.communicator import Communicator
from service.camera_service.camera_service import CameraService

class SocketService:
    def __init__(self, host : str, port : int, timeout : int):
        self.host = host 
        self.port = port 
        self.timeout = timeout 
        self.already_connected = set()
        self.camera_service = CameraService()
        self.config = ConfigParser()
        with open(config.get_config_file_path(), "r") as f:
            self.config.read_file(f)
        self.comm_agent = Communicator(
                    comm_config= OrderedDict({
                        "topics" : ["data/get_image", "data/get_stream"],
                        "subbed_topics" : {
                            "data/get_image" : self.camera_service.get_image, 
                            "data/get_stream" : self.camera_service.get_stream
                        }, 
                        "broker" : {
                            "host" : self.config.get("mqtt_broker", "ipv4"),
                            "port" : self.config.get("mqtt_broker", "port")
                        }
                    }))
    
    # Connect to the other client
    # If the other client is down, exit gracefully.
    def create_connection(self):
        with websockets.connect(
            uri = f"ws://{self.host}/{self.port}",
            ping_timeout = self.timeout) as connection: 
            self.already_connected.add(connection)
    
    async def handler(self, websocket):
        consumer_task = asyncio.create_task(self.consumer_handler(websocket))
        producer_task = asyncio.create_task(self.producer_handler(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
    
    # Sends data to websocket
    async def producer_handler(self, websocket):
        while True: 
            message_to_send = await self.produce()
            await websocket.send(message_to_send)

    # Receives data from websocket
    async def consumer_handler(self, websocket):
        async for message in websocket:
            await self.consume(message)
    
    # Business Logic for consume
    def consume(self, message):
        message_payload = json.loads(message)
        task = message_payload.get("task")
        assert task is not None

        # tasks can be a list[A, B, C] which have to run in serial orderedDict
        tasks = task.get("tasks")
        for task in tasks:
            payload = task.get("payload")
            if task.get("name") == "take_image":
                self.comm_agent.send_message_to_broker(
                    topic = "take_image", 
                    payload = payload
                )
            elif task.get("name") == "take_stream":
                self.comm_agent.send_message_to_broker(
                    topic = "take_stream", 
                    payload = payload
            )
    
    # Business Logic for Produce
    def produce(self):
        return self.comm_agent.on_message() 
                
if __name__ == '__main__':
    config_path = config.get_config_file_path()
    with open(config_path, "r") as conf:
        config = ConfigParser()
        config.read_file(conf)
    assert config is not None
    assert config.has_section("socket") is True

    socket_service = SocketService(
        host = config.get("socket", "ipv4"),
        port = config.get("socket", "port"),
        timeout = config.get("socket", "timeout"),
    )

    # TODO : How to run this service as a standalone for its life ?
    socket_service.loop_forever()



