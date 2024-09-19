"""
---
(c) 2024 David SPORN
---
This is part of py-isa-m68k -- Toolbox for the Motorola 68k Instruction Set Architecture.

py-isa-m68k is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

py-isa-m68k is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with py-isa-m68k.
If not, see <https://www.gnu.org/licenses/>. 
---
"""

from enum import Enum
from typing import List
from ..py_models import Interval, NodeRT

TypeOfFragment = Enum(
    "TypeOfFragment", ["SOURCE_FILE", "LINE__COMMENT", "LINE__STATEMENT"]
)


MARK_OF_COMMENT_LINE = ["*", ";"]

# FragmentOfCode
# {
#     NodeRT node : relationships between fragment
#     Interval range : location of the fragment
#     any type : tag for processing
#     dict[any] args : any relevant supplemental data
# }


# TODO : FragmentOfCode IS an NodeRT
class FragmentOfCode(NodeRT):
    def __init__(
        self, type: TypeOfFragment, range: Interval, *, parent: NodeRT = None, **kwargs
    ):
        super().__init__(parent=parent)
        self._type = type
        self._range = range
        self._args = kwargs

    @property
    def type(self) -> TypeOfFragment:
        return self._type

    @property
    def range(self) -> Interval:
        return self._range

    @property
    def args(self) -> dict:
        return self._args


class StaticParser:
    def __init__(self):
        pass

    def parseSource(self, charStream: str) -> list[FragmentOfCode]:
        sizeOfStream = len(charStream)
        rootFragment = FragmentOfCode(
            TypeOfFragment.SOURCE_FILE, Interval(0, length=sizeOfStream)
        )
        result = []
        mark = 0

        def processLine(line):
            sizeOfLine = len(line)
            if sizeOfLine > 0:
                range = Interval(mark, length=sizeOfLine)
                firstChar = charStream[mark]
                fragment = FragmentOfCode(
                    (
                        TypeOfFragment.LINE__COMMENT
                        if firstChar in MARK_OF_COMMENT_LINE
                        else TypeOfFragment.LINE__STATEMENT
                    ),
                    range,
                    parent=rootFragment,
                )
                result.append(fragment)

        def process(i, c):
            nonlocal mark
            if c in ["\n"]:
                # end of line
                processLine(charStream[mark:i].rstrip())
                mark = i + 1

        for i, c in enumerate(charStream):
            process(i, c)
        if mark < sizeOfStream - 1:
            processLine(charStream[mark:].rstrip())
        return result
