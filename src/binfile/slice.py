import os
import typing

from .base import FileBase

class Slice(FileBase):
    """ represents a smaller slice of another fileobj, only giving access to the given section """
    def __init__(self, f: FileBase, *, offset:int=0, size:typing.Optional[int]=None):
        self.f = f
        self.offset = offset # start of our 'window' into the file (which is of size `size`)
        self.pos = 0 # position we're reading right now
        if size is None:
            size = self.f.seek(0)
        self.size = size

    def read(self, n:int=-1) -> bytes:
        realpos = self.f.seek(self.offset + self.pos, os.SEEK_SET)
        pos = realpos - self.offset
        if n < 0: n = self.size-pos
        rc = self.f.read(n)
        self.pos = pos + len(rc)
        return rc
    
    def seek(self, offset:int, whence:int=os.SEEK_SET) -> int:
        raise Exception("implement me")

def split(f: FileBase, delimiter: bytes) -> typing.Generator[Slice,None,None]:
    f.seek(0, os.SEEK_SET)
    sliceStart = 0
    curPos = 0
    while True:
        data:bytes = f.read(8192)
        if not data: break

        while data:
            if delimiter in data:
                idx = data.index(delimiter)
                sliceLen = curPos + idx - sliceStart
                yield Slice(f, offset=sliceStart, size=sliceLen)
                sliceStart += idx
                curPos = 0
                data = data[idx+1:] 
            else:
                curPos += len(data)
                data = b''
            

    

#def splitAfter()
#def splitBefore()