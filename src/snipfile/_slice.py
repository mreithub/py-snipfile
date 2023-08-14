import os
import typing

CHUNK_SIZE=8192

from ._base import Filelike

class Slice(Filelike):
    """ represents a smaller slice of another fileobj, only giving access to the given section """
    def __init__(self, f: Filelike, *, offset:int=0, size:typing.Optional[int]=None):
        if size is None: size = f.size()
        if offset < 0: offset = size + offset # subtract offset from size (offset is negative)
        if offset < 0: offset = 0

        if offset > f.size(): offset = f.size()
        if offset + size > f.size(): size = f.size() - offset

        self.f = f
        self.offset = offset # start of our 'window' into the file (which is of size `size`)
        self._pos = 0 # position we're reading right now
        self._size = size

    def __repr__(self) -> str:
        return f"Slice(offset={self.offset}, size={self.size}, f={repr(self.f)})"

    def getPositionInfo(self, pos: int) -> typing.Tuple[str, int]:
        return self.f.getPositionInfo(self.offset + pos)

    def read(self, n:int=-1) -> bytes:
        realpos = self.f.seek(self.offset + self._pos, os.SEEK_SET)
        pos = realpos - self.offset
        if n < 0: n = self._size-pos
        if pos+n > self._size: n = self._size-pos
        rc = self.f.read(n)
        self._pos = pos + len(rc)
        return rc
    
    def seek(self, offset:int, whence:int=os.SEEK_SET) -> int:
        if whence == os.SEEK_SET:
            self._pos = offset
        elif whence == os.SEEK_CUR:
            self._pos += offset
        elif whence == os.SEEK_END:
            self._pos = self.size() - offset
        else: raise ValueError(f'seek(): invalid whence: {repr(whence)}')

        if self._pos < 0: self._pos = 0
        if self._pos > self.size(): self._pos = self.size()
        return self._pos

    def size(self) -> int: return self._size
    def tell(self) -> int: return self._pos

def _split(f: Filelike, delimiter: bytes, *, bytesBefore:int=0, bytesAfter:int=0, emptyTail:bool=True) -> typing.Generator[Slice,None,None]:
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

def cutAt(f:Filelike, *positions:int) -> typing.List[Slice]:
    rc:typing.List[Slice] = []
    lastCut = 0
    for cut in positions:
        rc.append(Slice(f, offset=lastCut, size=cut-lastCut))
        lastCut = cut
    rc.append(Slice(f, offset=lastCut))
    return rc


def split(f:Filelike, delimiter:bytes):
    return _split(f, delimiter)
    
def splitAfter(f:Filelike, delimiter:bytes):
    return _split(f, delimiter, bytesAfter=len(delimiter), emptyTail=False)
def splitBefore(f:Filelike, delimiter:bytes):
    return _split(f, delimiter, bytesBefore=len(delimiter))