import os
import typing

CHUNK_SIZE=8192

from .base import FileBase, FileIntf

class Slice(FileBase):
    """ represents a smaller slice of another fileobj, only giving access to the given section """
    def __init__(self, f: 'FileIntf', *, offset:int=0, size:typing.Optional[int]=None):
        if size is None:
            size = f.seek(0, os.SEEK_END)
        if offset < 0: offset = size + offset # subtract offset from size (offset is negative)
        if offset < 0: offset = 0

        self.f = f
        self.offset = offset # start of our 'window' into the file (which is of size `size`)
        self.pos = 0 # position we're reading right now
        self.size = size

    def __repr__(self) -> str:
        return f"Slice(offset={self.offset}, size={self.size}, f={repr(self.f)})"

    def read(self, n:int=-1) -> bytes:
        realpos = self.f.seek(self.offset + self.pos, os.SEEK_SET)
        pos = realpos - self.offset
        if n < 0: n = self.size-pos
        if pos+n > self.size: n = self.size-pos
        rc = self.f.read(n)
        self.pos = pos + len(rc)
        return rc
    
    def seek(self, offset:int, whence:int=os.SEEK_SET) -> int:
        if whence == os.SEEK_SET:
            self.pos = offset
        elif whence == os.SEEK_CUR:
            self.pos += offset
        elif whence == os.SEEK_END:
            self.pos = self.size - offset
        else: raise ValueError(f'seek(): invalid whence: {repr(whence)}')

        if self.pos < 0: self.pos = 0
        if self.pos > self.size: self.pos = self.size
        return self.pos

    def tell(self) -> int: return self.pos

def _split(f: FileIntf, delimiter: bytes, *, bytesBefore:int=0, bytesAfter:int=0, emptyTail:bool=True) -> typing.Generator[Slice,None,None]:
    if not delimiter: raise ValueError("split(): delimiter has to be nonempty")
    if len(delimiter) > CHUNK_SIZE/2: raise ValueError('delimiter too long')
    data = b''
    dataOffset = 0
    oldOffset = -1 # if this is
    sliceStart = 0
    while True:
        if dataOffset == oldOffset: break
        f.seek(dataOffset, os.SEEK_SET)
        oldOffset = dataOffset

        data = f.read(8192)
        if not data: break
        try:
            idx = data.index(delimiter)
        except ValueError:
            if len(data)-len(delimiter) == 0:
                break # we're at the end
            dataOffset += max(0, len(data)-len(delimiter))
            continue # not found

        sliceLen = idx
        yield Slice(f, offset=sliceStart-bytesBefore, size=sliceLen+bytesBefore+bytesAfter)
        dataOffset += idx+len(delimiter)
        sliceStart = dataOffset
    if emptyTail or f.size != sliceStart-bytesBefore:
        # there's data left after the last delimiter
        yield Slice(f, offset=sliceStart-bytesBefore)

def cutAt(f:FileIntf, *positions:int) -> typing.List[Slice]:
    rc:typing.List[Slice] = []
    lastCut = 0
    for cut in positions:
        rc.append(Slice(f, offset=lastCut, size=cut-lastCut))
        lastCut = cut
    rc.append(Slice(f, offset=lastCut))
    return rc


def split(f:FileIntf, delimiter:bytes):
    return _split(f, delimiter)
    
def splitAfter(f:FileIntf, delimiter:bytes):
    return _split(f, delimiter, bytesAfter=len(delimiter), emptyTail=False)
def splitBefore(f:FileIntf, delimiter:bytes):
    return _split(f, delimiter, bytesBefore=len(delimiter))