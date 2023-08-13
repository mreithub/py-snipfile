from io import SEEK_END
import io
import os
import typing

from .base import FileBase

class File(FileBase):
    " wraps filelike objects "
    def __init__(self, fileobj:typing.Union[typing.BinaryIO, str]):
        super().__init__(moduleName='file')
        if isinstance(fileobj, str):
            fileobj = open(fileobj, 'rb')
        self.size = fileobj.seek(0, os.SEEK_END)
        fileobj.seek(0)
        self.f = fileobj
        #self.name = fileobj.name

    def read(self, n:int=-1) -> bytes: return self.f.read(n)
    def seek(self, offset: int, whence:int=os.SEEK_SET) -> int:
        return self.f.seek(offset, whence)
    def tell(self) -> int: return self.f.tell()

def fromBytes(data:bytes) -> File:
    return File(io.BytesIO(data))