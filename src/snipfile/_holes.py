import typing
from . import _base
from . import _join
from . import _slice

@typing.overload
def punchHole(f: _base.Filelike, *, start:int, size:int) -> _base.Filelike: ...
@typing.overload
def punchHole(f: _base.Filelike, *, start:int, end:int) -> _base.Filelike: ...


def punchHole(f: _base.Filelike, *, start:int, size:typing.Optional[int]=None, end:typing.Optional[int]=None) -> _base.Filelike:
    if end is None:
        if size is None: 
            raise ValueError("please provide a size or end to snipfile.Hole()")
        end = start+size
    elif size is not None:
        raise ValueError("snipfile.Hole only accepts one of size/end")

    size = end-start
    if size < 0: raise ValueError("punchHole(): got hole of negative hole size")
    if start < 0: raise ValueError(f"punchHole() got negative start={repr(start)}")

    before, hole_, after = _slice.cutAt(f, start, end)
    assert hole_.size() == size
    return _join.join(before, after)