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

TypeOfNode = Enum(
    "TypeOfNode", ["SOURCE_FILE", "LINE__COMMENT", "LINE_EMPTY", "LINE_STATEMENT"]
)


class Node:
    def __init__(
        self,
        range: Range,
        *,
        tag: any = None,
        args: list = [],
        parent: "Node" = None,
        previous: "Node" = None,
        next: "Node" = None
    ):
        self._range = range
        self._tag = tag
        self._args = args
        self._parent = parent
        self._previous = previous
        self._next = next
        self._children = []
