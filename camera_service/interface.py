
import abc


class CameraInterface(metaclass = abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        one = hasattr(subclass, "get_frame") and callable(subclass.get_frame)
        two = hasattr(subclass, "stream_frame") and callable(subclass.stream_frame)
    
    @abc.abstractmethod
    def get_frame():
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_stream():
        raise NotImplementedError
