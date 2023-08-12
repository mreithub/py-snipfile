import abc
import os

class FileBase(abc.ABC):
    def __init__(self, *, moduleName:str) -> None:
        self.moduleName = moduleName

    @abc.abstractmethod
    def read(self, n:int=-1) -> bytes: ...

    @abc.abstractmethod
    def seek(self, offset: int, whence:int=os.SEEK_SET) -> int: ...
