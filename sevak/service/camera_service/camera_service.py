
# Objective : This service captures image, stream from a PiCamera and publishes data to the MQTT Broker
#               Whether you want a image or stream depends over how you use this service.

import argparse
import time
import cv2


from .interface import CameraInterface
from agents.communicator import Communicator
from loggers.logger import Logger
from collections import OrderedDict
from utils.serialise_deserialise import SerialiseDeserialise

class CameraService(CameraInterface):
    # Tries to load a VideoCapture object 
    # If that fails : raises Exception
    def __init__(self, camera_idx : int = -1):
        assert isinstance(camera_idx, int)
        self.capture = cv2.VideoCapture(camera_idx)
        if not self.capture or not self.capture.isOpened():
            raise Exception(f"Can't open the camera idx {camera_idx}")
    
    # Retry might be the case that the stream has died
    def retry(self, camera_idx : int = 0) -> bool:
        if not self.capture or self.capture.isOpened():
            # Wait for a moment before sending a new VideoCapture object.
            self.capture.release()
            time.sleep(1)
            capture = cv2.VideoCapture(camera_idx)
            # Set in-place
            self.capture = capture
        
        return self.capture and self.capture.isOpened()

    def get_fps(self):
        return self.capture.get(cv2.CAP_PROP_FPS)
    
    # Warmup camera for about 1 second.
    def warmup(self):
        time_start = time.perf_counter()
        frames_taken = 0
        frames_taken_success = 0
        while time.perf_counter() - time_start < 1:
            got_frame = self.captue.read()
            frames_taken += got_frame
            frames_taken_success += got_frame
        
        Logger.log("Warmup() complete : {frames_taken_success} frames taken out of {frames_taken} during warmup.")
    
    # Takes a single frame and returns it if that is possible
    def get_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            Logger.log("get_frame doesn't work right now. Maybe retry capturing image.")
            return None
        return frame

    # Takes a whole stream and returns a Stream Object if that is possible.
    def get_stream(self, timeout = 60):
        class StreamObject:
            def __init__(other, video_stream):
                other.timeout = timeout
                other.time_start = time.perf_counter()
                other.video_stream = video_stream

            def __iter__(other):
                other.frames_taken = 0
                return other
            
            def __next__(other):
                if time.perf_counter() - other.time_start < other.timeout:
                    ret, frame =  other.video_stream.read() 
                    if not ret:
                        Logger.log("get_frame doesn't work right now. Maybe retry capturing image.")
                        return None
                    other.frames_taken += 1
                    return frame
                else:
                    print(f"Total Frames taken : {other.frames_taken}")
                    raise StopIteration
        
        # New to Inner Classes in Python ? 
        # Doc : https://www.datacamp.com/tutorial/inner-classes-python
        return StreamObject(self.capture)

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        '--fps',
        type=float,
        default=1,
        help='Frame per second in streaming mode. (default: 1)'
    )
    ap.add_argument(
        '--broker-ip',
        default='localhost',
        help='MQTT broker IP.'
    )
    ap.add_argument(
        '--type',
        default='single_image',
        help='Possible Options are "single_image" or "stream". I guess the names are good enough for you.'
    )
    ap.add_argument(
        '--broker-port',
        default=1883,
        type=int,
        help='MQTT broker port.'
    )
    ap.add_argument('--topic',
        default='data/get_image/rgbimage',
        help='The topic to send the captured frames, see more in agents/__init__.py.'
    )

    return vars(ap.parse_args())


def main():
    args = parse_args()
    print(args)
    
    comm_config = OrderedDict({
        'sub_topics': {},
        'broker': {
            'ip': args['broker_ip'],
            'port': args['broker_port']
        }
    })
    comm_agent = Communicator(comm_config)
    
    camera_service = CameraService(camera_idx = 0)

    print(camera_service)
    
    out_fps = args['fps']
    if args.get("type") == "single_image":
        frame = camera_service.get_frame()
        if frame is None:
            working_now = camera_service.retry()
            if not working_now:
                Logger.log("Retry failed.")
                raise Exception("Camera output isn't working.")
        retval, jpg_bytes = cv2.imencode(".jpg", frame)
        mqtt_payload = SerialiseDeserialise.serialise_jpg(jpg_bytes)
        comm_agent.send_message_to_broker(args.get("topic"), mqtt_payload)

    elif args.get("type") == "stream":
        cam_fps = camera_service.get_fps()
        # Suppose out_fps is 30fps and cam_fps is 60fps
        # This means to make out_fps you would have to choose 1 frame out of 2 consecutive frames.
        # Wait frames would be 2
        wait_frames = int(cam_fps / out_fps)
        if cam_fps > 30 or cam_fps < 1:
            logger.warn(f'Camera FPS is {cam_fps} (>30 or <1). Setting it to 30.')
            cam_fps = 30
        
        # We want 30 seconds of streaming content. 
        # You can make this as big as possible.
        # TODO : Maybe default it to INT_MAX. 
        stream_object = camera_service.get_stream(timeout = 30)
        iter_stream = iter(stream_object)
        counter = 0
        while True:
            try:
                frame = next(iter_stream)
                if frame is None:
                    working_now = camera_service.retry()
                    if not working_now:
                        Logger.log("Retry failed.")
                        raise Exception("Camera output isn't working.")
            except StopIteration:
                break
            counter += 1
            if counter == wait_frames:
                counter = 1
                # Now you have wasted wait_frames - 1, you can send a new frame to MQTT broker.
                retval, jpg_bytes = cv2.imencode(".jpg", frame)
                mqtt_payload = SerialiseDeserialise.serialise_jpg(jpg_bytes)
                comm_agent.send_message_to_broker(args.get("topic"), mqtt_payload)

    else:
        raise NotImplementedError(f"{args.get('type')} is not supported right now. Try help.")


if __name__ == "__main__":
    main() 