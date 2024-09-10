"""
A model for 'rooted tree' type of graphs.

* Navigation through the graph is bi-directionnal.
* A node has a parent, except for a root node.
* A node has children, except for a leaf node. The list of children is **ordered**
* Nodes having the same parent are siblings, and a node is directly linked to the previous and next sibling in the list of children.
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

from typing import Optional


class NodeRT:
    """Node of a Rooted Tree"""

    def __init__(
        self,
        *,
        parent: "NodeRT" = None,
        previous: "NodeRT" = None,
        next: "NodeRT" = None,
        children: list["NodeRT"] = []
    ):
        if parent:
            self._parent = parent
        if previous:
            self._previous = previous
        if next:
            self._next = next
        if children:
            self._children = [x for x in children]

    # ========[ properties ]========
    @property
    def parent(self) -> Optional["NodeRT"]:
        return self._parent

    @property
    def children(self) -> list["NodeRT"]:
        return self._children

    @property
    def previous(self) -> Optional["NodeRT"]:
        return self._previous

    @property
    def next(self) -> Optional["NodeRT"]:
        return self._next

    # ========[ predicates ]========
    # -- self predicates
    def isRoot(self) -> bool:
        return False if self.parent else True

    def isLeaf(self) -> bool:
        return False if self.children else True

    def isFirstChild(self) -> bool:
        return False if self.previous else True

    def isLastChild(self) -> bool:
        return False if self.next else True

    # -- relations
    def isAncestorOrSelfOf(self, x: "NodeRT") -> bool:
        """Strict ordering relation"""
        current = x
        while current.parent:
            if current.parent is self:
                return True
            current = current.parent
        return False

    def isDescendantOf(self, x: "NodeRT") -> bool:
        """Strict ordering relation"""
        current = self
        while current.parent:
            if current.parent is x:
                return True
            current = current.parent
        return False

    def isSiblingOf(self, x: "NodeRT") -> bool:
        return x.parent is self.parent

    def isOlderSiblingOf(self, x: "NodeRT") -> bool:
        """Strict ordering relation"""
        if not self.isSiblingOf(x):
            return False
        current = self
        while current.next:
            if current.next is x:
                return True
            current = current.next
        return False

    def isYoungerSiblingOf(self, x: "NodeRT") -> bool:
        """Strict ordering relation"""
        if not self.isSiblingOf(x):
            return False
        current = self
        while current.previous:
            if current.previous is x:
                return True
            current = current.previous
        return False

    # ========[ graph management ]========
    # TODO : attach/detach child

    # ========[ others ]========
