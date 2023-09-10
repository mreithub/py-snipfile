import abc
import os
import typing

if hasattr(typing, 'Protocol'):
    class FileIntf(typing.Protocol):
        def getPositionInfo(self, pos:int): ...

        def read(self, n:int=-1) -> bytes: ...
        def seek(self, offset:int, whence:int=os.SEEK_SET) -> int: ...
        def size(self) -> int: ...
        def tell(self) -> int: ...

class Filelike(abc.ABC):
    " base class for all our file classes"
    def __init__(self, *, moduleName:str) -> None:
        self.moduleName = moduleName

    @abc.abstractmethod
    def getPositionInfo(self, pos:int) -> typing.Tuple[str,int]: ...

    @abc.abstractmethod
    def read(self, n:int=-1) -> bytes: ...

    @abc.abstractmethod
    def seek(self, offset:int, whence:int=os.SEEK_SET) -> int: ...

    @abc.abstractmethod
    def size(self) -> int: ...

    @abc.abstractmethod
    def tell(self) -> int: ...

    def writeTo(self, target:typing.BinaryIO):
        " writes the whole contents of this file or slice to target "
        self.seek(0)
        while True:
            data = self.read(8192)
            if not data: break
            target.write(data)
