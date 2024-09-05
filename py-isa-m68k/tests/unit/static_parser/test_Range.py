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

from isa_m68k.assembly.static_parser import Range


def test_Range_has_expected_properties():
    dummy = Range()
    assert dummy.offset == 0
    assert dummy.length == 0

    dummy = Range(1, 5)
    assert dummy.offset == 1
    assert dummy.length == 5


def test_Range_isBefore_is_an_ordering_relation():
    (a, b, c) = (Range(9), Range(10), Range(11))
    # isBefore is transitive
    assert a.isBefore(b)
    assert b.isBefore(c)
    assert a.isBefore(c)
    # isBefore is anti symetrical
    assert not b.isBefore(a)
    # isBefore is reflexive
    assert b.isBefore(b)


def test_Range_isSmaller_is_an_ordering_relation():
    (a, b, c) = (Range(0, 9), Range(0, 10), Range(0, 11))
    # isSmaller is transitive
    assert a.isSmaller(b)
    assert b.isSmaller(c)
    assert a.isSmaller(c)
    # isSmaller is anti symetrical
    assert not b.isSmaller(a)
    # isSmaller is reflexive
    assert b.isSmaller(b)
