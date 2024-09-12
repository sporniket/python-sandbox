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
    # -- Does not resolves parenting when binding siblings
    assert olderSibling.parent is None
    assert youngerSibling.parent is None
    assert olderSibling not in parent.children
    assert youngerSibling not in parent.children

    # Predicates
    assert not a.isRoot()
    assert parent.isRoot()
    assert not a.isLeaf()
    assert child1.isLeaf()
    assert not a.isFirstChild()
    assert not a.isLastChild()
    # -- child order has not been setup for child1/child2
    assert child1.isFirstChild()
    assert child1.isLastChild()


def test__NodeRT_isAncestorOf__is_a_strict_ordering_relation():
    a = NodeRT()
    b = NodeRT(parent=a)
    c = NodeRT(parent=b)

    assert a.isAncestorOf(b)
    assert b.isAncestorOf(c)
    # Anti-Reflexive
    assert not a.isAncestorOf(a)
    # Anti-symetric
    assert not b.isAncestorOf(a)
    # Transitive
    assert a.isAncestorOf(c)


def test__NodeRT_isDescendantOf__is_a_strict_ordering_relation():
    a = NodeRT()
    b = NodeRT(parent=a)
    c = NodeRT(parent=b)

    assert c.isDescendantOf(b)
    assert b.isDescendantOf(a)
    # Anti-Reflexive
    assert not a.isDescendantOf(a)
    # Anti-symetric
    assert not a.isDescendantOf(b)
    # Transitive
    assert c.isDescendantOf(a)
