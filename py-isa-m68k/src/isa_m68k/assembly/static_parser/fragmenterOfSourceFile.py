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
from ...py_models import Interval

from .fragment import TypeOfFragmentOfSourceCode, FragmentOfSourceCode
from .setOfChars import MARKERS__COMMENT


class FragmenterOfSourceFile:
    def __init__(self):
        pass

    def fragment(
        self, rootFragment: FragmentOfSourceCode, charStream: str
    ) -> list[FragmentOfSourceCode]:
        sizeOfStream = len(charStream)
        result = []
        mark = 0

        def processLine(line):
            sizeOfLine = len(line)
            if sizeOfLine > 0:
                range = Interval(mark, length=sizeOfLine)
                firstChar = charStream[mark]
                fragment = FragmentOfSourceCode(
                    (
                        TypeOfFragmentOfSourceCode.LINE__COMMENT
                        if firstChar in MARKERS__COMMENT
                        else TypeOfFragmentOfSourceCode.LINE__STATEMENT
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
