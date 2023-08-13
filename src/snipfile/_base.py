import abc
import os
import typing

if hasattr(typing, 'Protocol'):
    class FileIntf(typing.Protocol):
        size:int
        def read(self, n:int=-1) -> bytes: ...
        def seek(self, offset:int, whence:int=os.SEEK_SET) -> int: ...
        def tell(self) -> int: ...

class Filelike(abc.ABC):
    def __init__(self, *, moduleName:str) -> None:
        self.moduleName = moduleName

    @abc.abstractmethod
    def read(self, n:int=-1) -> bytes: ...

    @abc.abstractmethod
    def seek(self, offset:int, whence:int=os.SEEK_SET) -> int: ...

    @abc.abstractmethod
    def tell(self) -> int: ...