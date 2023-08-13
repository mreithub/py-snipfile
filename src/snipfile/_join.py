
import os
import typing
from . import _base

class JoinedFiles(_base.FileBase):
    def __init__(self, parts:'typing.List[_base.FileIntf]'):
        super().__init__(moduleName='join')
        self.parts = parts
        self.pos:int = 0
        self.size:int = sum(part.size for part in parts)
        self.offsets:typing.List[int] = []
        self._currentIndex = 0
        offset = 0
        for part in parts:
            self.offsets.append(offset)
            offset += part.size

    def _getRelativeOffset(self, offset:int):
        startOfPart = self.offsets[self._currentIndex]
        return offset - startOfPart

    def __repr__(self) -> str:
        return f"JoinedFiles({', '.join([repr(part) for part in self.parts])})"
    def read(self, n: int = -1) -> bytes:
        if n < 0: n = self.size - self.pos
        if n <= 0: return b''

        rc = b''
        idx = self._currentIndex
        while idx < len(self.parts):
            f = self.parts[idx]
            f.seek(self._getRelativeOffset(self.pos))
            data = f.read(n - len(rc))
            if not data: break
            rc += data
            idx += 1
        return rc

    def seek(self, offset: int, whence: int = os.SEEK_SET) -> int:
        if whence == os.SEEK_SET:
            self.pos = offset
        elif whence == os.SEEK_CUR:
            self.pos += offset
        elif whence == os.SEEK_END:
            self.pos = self.size - offset
        else: raise ValueError(f"seek(): unsupported whence param: {whence}")

        if self.pos < 0: self.pos = 0
        if self.pos > self.size: self.pos = self.size

        # find the part that matches our position
        idx = 0
        for i, offset in enumerate(self.offsets):
            if self.pos < offset: break
            idx = i
        self._currentIndex = idx

        return self.pos
 
    def tell(self) -> int: return self.pos

def join(*parts: '_base.FileIntf'):
    return JoinedFiles(list(parts))