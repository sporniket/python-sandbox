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
from py_models import Interval, NodeRT


TypeOfFragmentOfSourceCode = Enum(
    "TypeOfFragmentOfSourceCode",
    [
        "SOURCE_FILE",  #
        "LINE__COMMENT",
        "LINE__STATEMENT",  #
        "FIELD__LABEL",
        "FIELD__MNEMONIC",
        "FIELD__OPERANDS",
        "FIELD__COMMENTS",  #
    ],
)

# FragmentOfCode
# {
#     NodeRT node : relationships between fragment
#     Interval range : location of the fragment
#     any type : tag for processing
#     dict[any] args : any relevant supplemental data
# }


class FragmentOfSourceCode(NodeRT):
    def __init__(
        self,
        type,
        range: Interval,
        *,
        parent: NodeRT = None,
        **kwargs,
    ):
        super().__init__(parent=parent)
        self._type = type
        self._range = range
        self._args = kwargs

        # cache absolute start
        start = range.start
        currentParent = parent
        while currentParent is not None:
            start = start + currentParent.range.start
            currentParent = currentParent.parent
        self._absoluteRange = Interval(start, length=range.length)

    @property
    def type(self):
        return self._type

    @property
    def range(self) -> Interval:
        return self._range

    @property
    def args(self) -> dict:
        return self._args

    @property
    def absoluteStart(self) -> int:
        return self._absoluteRange.start

    @property
    def absoluteEnd(self) -> int:
        return self._absoluteRange.end


def prepareSourceFragment(charStream: str) -> FragmentOfSourceCode:
    return FragmentOfSourceCode(
        TypeOfFragmentOfSourceCode.SOURCE_FILE, Interval(0, length=len(charStream))
    )
