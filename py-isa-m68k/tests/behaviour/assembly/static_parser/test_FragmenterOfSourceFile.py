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
    FragmenterOfSourceFile,
    FragmentOfSourceCode,
    TypeOfFragmentOfSourceCode,
)

from .utils import thenFragmentMeetsExpectations


def test__FragmenterOfSourceFile_fragment__ignores_empty_lines():
    fragments = FragmenterOfSourceFile().fragment(
        """** 
* A minimal program for Atari ST.
*
* Just a call to Pterm0() to terminate immediately.
* 

                move.w  #0,-(sp) ; GEMDOS function code 0 = Pterm0()
                trap    #1      ; Call GEMDOS"""
    )

    assert len(fragments) == 7

    root = fragments[0].parent
    assert root is not None
    assert root.type == TypeOfFragmentOfSourceCode.SOURCE_FILE

    thenFragmentMeetsExpectations(
        fragments[0],
        TypeOfFragmentOfSourceCode.LINE__COMMENT,
        0,
        2,
        parent=root,
        childRank=0,
    )
    thenFragmentMeetsExpectations(
        fragments[1],
        TypeOfFragmentOfSourceCode.LINE__COMMENT,
        4,
        33,
        parent=root,
        childRank=1,
    )
    thenFragmentMeetsExpectations(
        fragments[2],
        TypeOfFragmentOfSourceCode.LINE__COMMENT,
        38,
        1,
        parent=root,
        childRank=2,
    )
    thenFragmentMeetsExpectations(
        fragments[3],
        TypeOfFragmentOfSourceCode.LINE__COMMENT,
        40,
        51,
        parent=root,
        childRank=3,
    )
    thenFragmentMeetsExpectations(
        fragments[4],
        TypeOfFragmentOfSourceCode.LINE__COMMENT,
        92,
        1,
        parent=root,
        childRank=4,
    )
    thenFragmentMeetsExpectations(
        fragments[5],
        TypeOfFragmentOfSourceCode.LINE__STATEMENT,
        96,
        68,
        parent=root,
        childRank=5,
    )
    thenFragmentMeetsExpectations(
        fragments[6],
        TypeOfFragmentOfSourceCode.LINE__STATEMENT,
        165,
        45,
        parent=root,
        childRank=6,
    )
