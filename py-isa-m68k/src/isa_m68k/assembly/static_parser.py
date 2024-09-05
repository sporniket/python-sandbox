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

TypeOfNode = Enum(
    "TypeOfNode", ["SOURCE_FILE", "LINE__COMMENT", "LINE_EMPTY", "LINE_STATEMENT"]
)


class Range:
    def __init__(self, offset: int = 0, length: int = 0):
        # sanity checks
        errors = []
        if offset < 0:
            errors += ["invalid.must.be.positive.or.zero:offset"]
        if length < 0:
            errors += ["invalid.must.be.positive.or.zero:length"]
        if len(errors) > 0:
            listBody = ",".join(errors)
            raise ValueError(*errors)
        self._offset = offset
        self._length = length

    @property
    def offset(self) -> int:
        return self._offset

    @property
    def length(self) -> int:
        return self._length

    # ========[ predicates ] ========
    def isEmpty(self) -> bool:
        return self._length == 0

    def isBefore(self, x: "Range") -> bool:
        return (x is not None) and self._isBefore(x)

    def isEndingBefore(self, x: "Range") -> bool:
        return (x is not None) and (self.offset + self.length <= x.offset + x.length)

    def isSmaller(self, x: "Range") -> bool:
        return x is not None and self._isSmaller(x)

    def isOutside(self, x: "Range") -> bool:
        return (x is None) or x._isBeginningAfter(self) or self._isBeginningAfter(x)

    def isInside(self, x: "Range") -> bool:
        return (x is not None) and x._isBefore(self) and self._isEndingBefore(x)

    # ========[ predicates internal ] ========
    def _isBefore(self, x: "Range") -> bool:
        return self.offset <= x.offset

    def _isEndingBefore(self, x: "Range") -> bool:
        return self.offset + self.length <= x.offset + x.length

    def _isBeginningAfter(self, x: "Range") -> bool:
        return self.offset >= x.offset + x.length

    def _isSmaller(self, x: "Range") -> bool:
        return self.length <= x.length
