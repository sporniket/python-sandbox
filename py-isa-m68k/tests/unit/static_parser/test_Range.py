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

import pytest
from isa_m68k.assembly.static_parser import Range


def test_Range_has_expected_properties():
    dummy = Range()
    assert dummy.offset == 0
    assert dummy.length == 0
    assert dummy.end == 0

    dummy = Range(1, 5)
    assert dummy.offset == 1
    assert dummy.length == 5
    assert dummy.end == 6

    with pytest.raises(ValueError) as error:
        Range(-1)
    assert "invalid.must.be.positive.or.zero:offset" in error.value.args
    assert len(error.value.args) == 1

    with pytest.raises(ValueError) as error:
        Range(0, -1)
    assert "invalid.must.be.positive.or.zero:length" in error.value.args
    assert len(error.value.args) == 1

    with pytest.raises(ValueError) as error:
        Range(-1, -1)
    assert "invalid.must.be.positive.or.zero:offset" in error.value.args
    assert "invalid.must.be.positive.or.zero:length" in error.value.args
    assert len(error.value.args) == 2


def test_Range_isEmpty_works_as_expected():
    (a, b) = (Range(0, 0), Range(0, 1))
    assert a.isEmpty()
    assert not b.isEmpty()


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
    # is never before null
    assert not b.isBefore(None)


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
    # is not smaller than None
    assert not b.isSmaller(None)


def test_Range_isEndingBefore_is_an_ordering_relation():
    (a, b, c) = (Range(9, 10), Range(10, 10), Range(11, 10))
    # isEndingBefore is transitive
    assert a.isEndingBefore(b)
    assert b.isEndingBefore(c)
    assert a.isEndingBefore(c)
    # isEndingBefore is anti symetrical
    assert not b.isEndingBefore(a)
    # isEndingBefore is reflexive
    assert b.isEndingBefore(b)
    # is not ending before None
    assert not b.isEndingBefore(None)


def test_Range_isOutside_works_as_expected():
    a, b, c = Range(5, 10), Range(15, 10), Range(3, 15)
    assert a.isOutside(b)
    assert not a.isOutside(c)
    assert b.isOutside(a)
    assert not b.isOutside(c)
    assert not c.isOutside(a)
    assert not c.isOutside(b)


def test_Range_isInside_is_an_ordering_relation():
    (a, b, c) = (Range(9, 2), Range(8, 4), Range(7, 6))
    # isInside is transitive
    assert a.isInside(b)
    assert b.isInside(c)
    assert a.isInside(c)
    # isInside is anti symetrical
    assert not b.isInside(a)
    # isInside is reflexive
    assert b.isInside(b)
    # is not inside None
    assert not b.isInside(None)
    # other things
    assert not a.isInside(Range(7, 2))
    assert not a.isInside(Range(8, 2))
    assert not a.isInside(Range(10, 2))
    assert not a.isInside(Range(11, 2))
