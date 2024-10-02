"""
---
(c) 2024 David SPORN
---
This is part of Gencode

Gencode is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

Gencode is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with Gencode.
If not, see <https://www.gnu.org/licenses/>. 
---
"""

from enum import Enum
import re

Whatever = "whatever"

IdentifierPartType = Enum("IdentifierPartType", ["SEPARATOR", "REGULAR"])

RegularPartPattern = re.compile("^[0-9A-Za-z]+$")


class IdentifierPart:
    def __init__(self, value: str = None):
        match = RegularPartPattern.match("" if value is None else value)
        if match:
            self._type = IdentifierPartType.REGULAR
            self._value = value
        else:
            self._type = IdentifierPartType.SEPARATOR
            self._value = "_"

    @property
    def isSeparator(self):
        return self._type is IdentifierPartType.SEPARATOR

    @property
    def isRegular(self):
        return self._type is IdentifierPartType.REGULAR

    @property
    def lowered(self):
        return self._value if self.isSeparator else self._value.lower()

    @property
    def capitalized(self):
        return self._value if self.isSeparator else self._value.capitalize()

    @property
    def allcaps(self):
        return self._value if self.isSeparator else self._value.upper()
