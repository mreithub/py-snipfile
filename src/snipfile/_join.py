
import os
import typing
from ._base import Filelike

class JoinedFiles(Filelike):
    def __init__(self, parts:'typing.List[Filelike]'):
        super().__init__(moduleName='join')
        self.parts = parts
        self._pos:int = 0
        self._size:int = sum(part.size() for part in parts)
        self._offsets:typing.List[int] = []
        self._currentIndex = 0
        offset = 0
        for part in parts:
            self._offsets.append(offset)
            offset += part.size()

    def _getRelativeOffset(self, offset:int):
        startOfPart = self._offsets[self._currentIndex]
        return offset - startOfPart

    def __repr__(self) -> str:
        return f"JoinedFiles({', '.join([repr(part) for part in self.parts])})"
    def read(self, n: int = -1) -> bytes:
        if n < 0: n = self._size - self._pos
        if n <= 0: return b''

        rc = b''
        idx = self._currentIndex
        while idx < len(self.parts):
            f = self.parts[idx]
            f.seek(self._getRelativeOffset(self._pos))
            data = f.read(n - len(rc))
            if not data: break
            rc += data
            idx += 1
        return rc

    def seek(self, offset: int, whence: int = os.SEEK_SET) -> int:
        if whence == os.SEEK_SET:
            self._pos = offset
        elif whence == os.SEEK_CUR:
            self._pos += offset
        elif whence == os.SEEK_END:
            self._pos = self._size - offset
        else: raise ValueError(f"seek(): unsupported whence param: {whence}")

        if self._pos < 0: self._pos = 0
        if self._pos > self._size: self._pos = self._size

        # find the part that matches our position
        idx = 0
        for i, offset in enumerate(self._offsets):
            if self._pos < offset: break
            idx = i
        self._currentIndex = idx

        return self._pos
 
    def size(self) -> int: return self._size
    def tell(self) -> int: return self._pos

def join(*parts: Filelike):
    return JoinedFiles(list(parts))