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

from isa_m68k.py_models import NodeRT


def test__NodeRT__has_expected_properties():
    parent, olderSibling, youngerSibling, child1, child2 = (
        NodeRT(),
        NodeRT(),
        NodeRT(),
        NodeRT(),
        NodeRT(),
    )
    a = NodeRT(
        parent=parent,
        previous=olderSibling,
        next=youngerSibling,
        children=[child1, child2],
    )

    assert a.parent is parent
    assert a.previous is olderSibling
    assert a.next is youngerSibling
    assert len(a.children) == 2
    assert a.children[0] == child1
    assert a.children[1] == child2

    # side effects -- referenced nodes are relinked according to specified relations.
    assert a in parent.children
    assert a is olderSibling.next
    assert a is youngerSibling.previous
    assert a is child1.parent
    assert a is child2.parent
    assert parent is olderSibling.parent
    assert parent is youngerSibling.parent
