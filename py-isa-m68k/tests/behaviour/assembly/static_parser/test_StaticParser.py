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

from isa_m68k.assembly.static_parser import StaticParser, FragmentOfCode, TypeOfFragment


def thenFragmentHasExpectedRange(fragment: FragmentOfCode, start, length):
    assert fragment.range.start == start
    assert fragment.range.length == length


def test__StaticParser_parseSource__ignores_empty_lines():
    fragments = StaticParser().parseSource(
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
    assert root.type == TypeOfFragment.SOURCE_FILE
    assert root is not None
    for i, f in enumerate(fragments):
        assert root is f.parent
        assert root.children[i] is f

    assert fragments[0].type == TypeOfFragment.LINE__COMMENT
    assert fragments[1].type == TypeOfFragment.LINE__COMMENT
    assert fragments[2].type == TypeOfFragment.LINE__COMMENT
    assert fragments[3].type == TypeOfFragment.LINE__COMMENT
    assert fragments[4].type == TypeOfFragment.LINE__COMMENT
    assert fragments[5].type == TypeOfFragment.LINE__STATEMENT
    assert fragments[6].type == TypeOfFragment.LINE__STATEMENT

    thenFragmentHasExpectedRange(fragments[0], 0, 2)
    thenFragmentHasExpectedRange(fragments[1], 4, 33)
    thenFragmentHasExpectedRange(fragments[2], 38, 1)
    thenFragmentHasExpectedRange(fragments[3], 40, 51)
    thenFragmentHasExpectedRange(fragments[4], 92, 1)
    thenFragmentHasExpectedRange(fragments[5], 96, 68)
    thenFragmentHasExpectedRange(fragments[6], 165, 45)
