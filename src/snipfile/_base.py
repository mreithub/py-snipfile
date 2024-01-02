import abc
import os
import typing

class PositionInfo:
    def __init__(self, file: 'Filelike', name: typing.Optional[str], pos:int):
        self.file = file
        self.name = name
        self.pos = pos


# interfaces for python-style fileobjects (for type hinting purposes)
# in the past I was using typing.BinaryIO for that purpose, but not even all python files follow that protocol (e.g. NamedTemporaryFile)
class _PyFile(typing.Protocol):
    " interface for python-style fileobjects (the bare minimum we require for snipfile to be able to wrap these) "
    def read(self, n:int) -> bytes: ...
    def seek(self, __offset:int, __whence:int=os.SEEK_SET) -> int: ...
    def tell(self) -> int: ...

class _PyWritableFile(typing.Protocol):
    " interface for python-style file objects we want to write to (bare minimum we require for writeTo() to work) "
    def write(self, __data:typing.Union[bytes, bytearray]) -> int: ...



class FileIntf(typing.Protocol):
    def getPositionInfo(self, pos:int) -> PositionInfo: ...

    def read(self, n:int=-1) -> bytes: ...
    def seek(self, offset:int, whence:int=os.SEEK_SET) -> int: ...
    def size(self) -> int: ...
    def tell(self) -> int: ...


class Filelike(abc.ABC):
    " base class for all our file classes"
    def __init__(self, *, moduleName:str) -> None:
        self.moduleName = moduleName

    @abc.abstractmethod
    def getPositionInfo(self, pos:int) -> PositionInfo:
        """ translates pos into the path and absolute position in the underlying file; can be used to provide valuable position info to the user """

    @abc.abstractmethod
    def read(self, n:int=-1) -> bytes: ...

    @abc.abstractmethod
    def seek(self, offset:int, whence:int=os.SEEK_SET) -> int:
        """ seek() to the given position, relative to `whence`, e.g.:
- seek(n) behaves like seek(0, os.SEEK_SET)
- seek(n, os.SEEK_SET) moves the file cursor to position 100"
- seek(n, os.SEEK_CUR) moves the file cursor to tell()+n
- seek(n, os.SEEK_END) moves the file cursor to size()+n
"""

    @abc.abstractmethod
    def size(self) -> int: ...

    @abc.abstractmethod
    def tell(self) -> int: ...

    def writeTo(self, target:'_PyWritableFile'):
        " writes the whole contents of this file or slice to target "
        self.seek(0)
        while True:
            data = self.read(8192)
            if not data: break
            target.write(data)
