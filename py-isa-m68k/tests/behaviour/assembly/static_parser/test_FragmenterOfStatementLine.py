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
    FragmenterOfStatementLine,
    FragmentOfSourceCode,
    TypeOfFragmentOfSourceCode,
)
from py_models import Interval


from .utils import thenFragmentMeetsExpectations


def test__FragmenterOfStatementLine_fragment__fragments_line_into_fields():
    sourceFile = """** 
* A minimal program for Atari ST.
*
* Just a call to Pterm0() to terminate immediately.
* 

                move.w  #0,-(sp) ; GEMDOS function code 0 = Pterm0()
                trap    #1      ; Call GEMDOS"""
    statementFragment = FragmentOfSourceCode(
        TypeOfFragmentOfSourceCode.LINE__STATEMENT,
        range=Interval(96, length=68),
        parent=FragmentOfSourceCode(
            TypeOfFragmentOfSourceCode.SOURCE_FILE, range=Interval(0, length=210)
        ),
    )
    fragments = FragmenterOfStatementLine().fragment(statementFragment, sourceFile)

    assert len(fragments) == 3
    ### verify all about mnemonic
    thenFragmentMeetsExpectations(
        fragments[0],
        TypeOfFragmentOfSourceCode.FIELD__MNEMONIC,
        16,
        6,
        parent=statementFragment,
        childRank=0,
    )
    assert len(fragments[0].children) == 0

    ### verify all about operands
    thenFragmentMeetsExpectations(
        fragments[1],
        TypeOfFragmentOfSourceCode.FIELD__OPERANDS,
        24,
        8,
        parent=statementFragment,
        childRank=1,
    )
    assert len(fragments[1].children) == 0

    ### verify all about comments
    thenFragmentMeetsExpectations(
        fragments[2],
        TypeOfFragmentOfSourceCode.FIELD__COMMENTS,
        35,
        33,
        parent=statementFragment,
        childRank=2,
    )
