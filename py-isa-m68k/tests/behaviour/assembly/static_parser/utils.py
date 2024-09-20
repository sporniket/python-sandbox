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

from isa_m68k.assembly.static_parser import (
    FragmentOfSourceCode,
    TypeOfFragment,
)


def thenFragmentMeetsExpectations(
    fragment: FragmentOfSourceCode,
    type: TypeOfFragment,
    start: int,
    length: int,
    *,
    parent=None,
    childRank: int = -1
):
    assert fragment.type == type
    assert fragment.range.start == start
    assert fragment.range.length == length
    assert fragment.parent is parent
    if parent is not None:
        assert fragment in parent.children
        if childRank >= 0:
            assert fragment is parent.children[childRank]
