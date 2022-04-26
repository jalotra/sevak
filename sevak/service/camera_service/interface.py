import abc

class CameraInterface(metaclass = abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        get_frame = hasattr(subclass, "get_frame") and callable(subclass.get_frame)
        get_stream = hasattr(subclass, "get_stream") and callable(subclass.stream_frame)

        if not (get_frame or get_stream):
            raise NotImplementedError
    
    @abc.abstractmethod
    def get_frame():
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_stream():
        raise NotImplementedError
