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

from enum import Enum
from typing import List
from ..py_models import Interval, NodeRT


MARKERS__COMMENT = ["*", ";"]
MARKERS__STRING = ['"', "'"]
MARKERS__LABEL = [":"]
WHITESPACES = [" ", "\t"]

########################[Source code --> fragments (line of code)]########################

TypeOfFragmentOfSourceCode = Enum(
    "TypeOfFragmentOfSourceCode",
    [
        "SOURCE_FILE",  #
        "LINE__COMMENT",
        "LINE__STATEMENT",  #
        "FIELD__LABEL",
        "FIELD__MNEMONIC",
        "FIELD__OPERANDS",
        "FIELD__COMMENTS",
    ],
)

# FragmentOfCode
# {
#     NodeRT node : relationships between fragment
#     Interval range : location of the fragment
#     any type : tag for processing
#     dict[any] args : any relevant supplemental data
# }


class FragmentOfSourceCode(NodeRT):
    def __init__(
        self,
        type: TypeOfFragmentOfSourceCode,
        range: Interval,
        *,
        parent: NodeRT = None,
        **kwargs,
    ):
        super().__init__(parent=parent)
        self._type = type
        self._range = range
        self._args = kwargs

    @property
    def type(self) -> TypeOfFragmentOfSourceCode:
        return self._type

    @property
    def range(self) -> Interval:
        return self._range

    @property
    def args(self) -> dict:
        return self._args


class FragmenterOfSourceFile:
    def __init__(self):
        pass

    def fragment(self, charStream: str) -> list[FragmentOfSourceCode]:
        sizeOfStream = len(charStream)
        rootFragment = FragmentOfSourceCode(
            TypeOfFragmentOfSourceCode.SOURCE_FILE, Interval(0, length=sizeOfStream)
        )
        result = []
        mark = 0

        def processLine(line):
            sizeOfLine = len(line)
            if sizeOfLine > 0:
                range = Interval(mark, length=sizeOfLine)
                firstChar = charStream[mark]
                fragment = FragmentOfSourceCode(
                    (
                        TypeOfFragmentOfSourceCode.LINE__COMMENT
                        if firstChar in MARKERS__COMMENT
                        else TypeOfFragmentOfSourceCode.LINE__STATEMENT
                    ),
                    range,
                    parent=rootFragment,
                )
                result.append(fragment)

        def process(i, c):
            nonlocal mark
            if c in ["\n"]:
                # end of line
                processLine(charStream[mark:i].rstrip())
                mark = i + 1

        for i, c in enumerate(charStream):
            process(i, c)
        if mark < sizeOfStream - 1:
            processLine(charStream[mark:].rstrip())
        return result


########################[Statement (Fragment of Source code) --> fragments (fields of statement)]########################


# state machine states for parsing a statement line
ACCUMULATE_LABEL = 0  # when first character is not whitespace --> WAIT_MNEMONIC
WAIT_LABEL_OR_MNEMONIC = 1  # when first character is not whitespace, until not whitespace --> ACCUMULATE_LABEL_OR_MNEMONIC
ACCUMULATE_LABEL_OR_MNEMONIC = (
    2  # until ':' --> WAIT_MNEMONIC ; or until whitespace --> WAIT_OPERANDS_OR_COMMENT
)
WAIT_MNEMONIC = 4  # until not whitespace --> ACCUMULATE_MNEMONIC
ACCUMULATE_MNEMONIC = 5  # until whitespace --> WAIT_OPERANDS_OR_COMMENT
WAIT_OPERANDS_OR_COMMENT = 6  # until not whitespace --> ACCUMULATE_OPERANDS
ACCUMULATE_OPERANDS = 7  # should understand string litterals ; until whitespace --> WAIT_COMMENT_OR_COMMENT_BODY
WAIT_COMMENT_OR_COMMENT_BODY = (
    8  # wait for comment marker or body --> ACCUMULATE_COMMENT
)
WAIT_COMMENT_BODY = 9  # until not whitespace --> ACCUMULATE_COMMENT
ACCUMULATE_COMMENT = 10  # until end of line
INSIDE_STRING_LITTERAL = 11  # temporary state that waits for end of the string.


class FragmenterOfStatementLine:
    def __init__(self):
        pass

    def fragment(
        self, statementLine: FragmentOfSourceCode, charStream: str
    ) -> list[FragmentOfSourceCode]:
        if statementLine.type != TypeOfFragmentOfSourceCode.LINE__STATEMENT:
            raise ValueError("invalid.fragment.not.a.statement.line")
        stringMarker = '"'
        lastMark = 0
        escapeStringMarker = False
        for i, c in enumerate(charStream):
            if i == 0:
                if c not in WHITESPACES:
                    self._state = ACCUMULATE_LABEL
                else:
                    self._state = WAIT_LABEL_OR_MNEMONIC
                continue
            else:
                if self._state == ACCUMULATE_LABEL:
                    if c in MARKERS__COMMENT:
                        FragmentOfSourceCode(
                            TypeOfFragmentOfSourceCode.FIELD__LABEL,
                            Interval(lastMark, end=i),
                            parent=statementLine,
                        )
                        lastMark = i
                        self._state = WAIT_COMMENT_BODY
                        continue
                    elif c in WHITESPACES or c in MARKERS__LABEL:
                        FragmentOfSourceCode(
                            TypeOfFragmentOfSourceCode.FIELD__LABEL,
                            Interval(lastMark, end=i),
                            parent=statementLine,
                        )
                        lastMark = i
                        self._state = WAIT_MNEMONIC
                        continue
                    else:
                        continue
                elif self._state == WAIT_LABEL_OR_MNEMONIC:
                    lastMark = i
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    elif c not in WHITESPACES:
                        self._state = ACCUMULATE_LABEL_OR_MNEMONIC
                        continue
                elif self._state == ACCUMULATE_LABEL_OR_MNEMONIC:
                    if c in MARKERS__COMMENT:
                        FragmentOfSourceCode(
                            TypeOfFragmentOfSourceCode.FIELD__MNEMONIC,
                            Interval(lastMark, end=i),
                            parent=statementLine,
                        )
                        lastMark = i
                        self._state = WAIT_COMMENT_BODY
                        continue
                    if c in MARKERS__LABEL:
                        FragmentOfSourceCode(
                            TypeOfFragmentOfSourceCode.FIELD__LABEL,
                            Interval(lastMark, end=i),
                            parent=statementLine,
                        )
                        lastMark = i
                        self._state = WAIT_MNEMONIC
                        continue
                    elif c in WHITESPACES:
                        FragmentOfSourceCode(
                            TypeOfFragmentOfSourceCode.FIELD__MNEMONIC,
                            Interval(lastMark, end=i),
                            parent=statementLine,
                        )
                        lastMark = i
                        self._state = WAIT_OPERANDS_OR_COMMENT
                        continue
                    else:
                        continue
                elif self._state == WAIT_MNEMONIC:
                    lastMark = i
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    if c not in WHITESPACES:
                        self._state = ACCUMULATE_MNEMONIC
                        continue
                elif self._state == ACCUMULATE_MNEMONIC:
                    if c in MARKERS__COMMENT:
                        FragmentOfSourceCode(
                            TypeOfFragmentOfSourceCode.FIELD__MNEMONIC,
                            Interval(lastMark, end=i),
                            parent=statementLine,
                        )
                        lastMark = i
                        self._state = WAIT_COMMENT_BODY
                        continue
                    if c in WHITESPACES:
                        FragmentOfSourceCode(
                            TypeOfFragmentOfSourceCode.FIELD__MNEMONIC,
                            Interval(lastMark, end=i),
                            parent=statementLine,
                        )
                        lastMark = i
                        self._state = WAIT_OPERANDS_OR_COMMENT
                        continue
                    else:
                        continue
                elif self._state == WAIT_OPERANDS_OR_COMMENT:
                    lastMark = i
                    if c not in WHITESPACES:
                        if c in MARKERS__COMMENT:
                            self._state = WAIT_COMMENT_BODY
                            continue
                        else:
                            if c in MARKERS__STRING:
                                self._state = INSIDE_STRING_LITTERAL
                            else:
                                self._state = ACCUMULATE_OPERANDS
                            continue
                elif self._state == ACCUMULATE_OPERANDS:
                    if c in MARKERS__COMMENT:
                        FragmentOfSourceCode(
                            TypeOfFragmentOfSourceCode.FIELD__OPERANDS,
                            Interval(lastMark, end=i),
                            parent=statementLine,
                        )
                        lastMark = i
                        self._state = WAIT_COMMENT_BODY
                        continue
                    if c in MARKERS__STRING:
                        escapeStringMarker = False
                        self._state == INSIDE_STRING_LITTERAL
                        continue
                    elif c in WHITESPACES:
                        FragmentOfSourceCode(
                            TypeOfFragmentOfSourceCode.FIELD__OPERANDS,
                            Interval(lastMark, end=i),
                            parent=statementLine,
                        )
                        lastMark = i
                        self._state = WAIT_COMMENT_OR_COMMENT_BODY
                        continue
                    else:
                        continue
                elif self._state == WAIT_COMMENT_OR_COMMENT_BODY:
                    lastMark = i
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    elif c not in WHITESPACES:
                        self._state = ACCUMULATE_COMMENT
                        continue
                    else:
                        continue
                elif self._state == WAIT_COMMENT_BODY:
                    lastMark = i
                    if c not in WHITESPACES:
                        self._state = ACCUMULATE_COMMENT
                        continue
                elif self._state == ACCUMULATE_COMMENT:
                    continue
                elif self._state == INSIDE_STRING_LITTERAL:
                    if c == stringMarker:
                        self._state = ACCUMULATE_OPERANDS
                    continue
                else:
                    raise ValueError(
                        f"Unknown state '{self._state}' at position {i}, character '{c}' while parsing line of code : {line}"
                    )
        # When finished while still accumulating, create the last fragment
        if self._state == ACCUMULATE_LABEL:
            FragmentOfSourceCode(
                TypeOfFragmentOfSourceCode.FIELD__LABEL,
                Interval(lastMark, end=len(charStream)),
                parent=statementLine,
            )
        elif self._state == ACCUMULATE_LABEL_OR_MNEMONIC:
            FragmentOfSourceCode(
                TypeOfFragmentOfSourceCode.FIELD__LABEL,
                Interval(lastMark, end=len(charStream)),
                parent=statementLine,
            )
        elif self._state == ACCUMULATE_MNEMONIC:
            FragmentOfSourceCode(
                TypeOfFragmentOfSourceCode.FIELD__MNEMONIC,
                Interval(lastMark, end=len(charStream)),
                parent=statementLine,
            )
        elif self._state == ACCUMULATE_OPERANDS:
            FragmentOfSourceCode(
                TypeOfFragmentOfSourceCode.FIELD__OPERANDS,
                Interval(lastMark, end=len(charStream)),
                parent=statementLine,
            )
        elif self._state == ACCUMULATE_COMMENT:
            FragmentOfSourceCode(
                TypeOfFragmentOfSourceCode.FIELD__COMMENTS,
                Interval(lastMark, end=len(charStream)),
                parent=statementLine,
            )
        elif self._state == INSIDE_STRING_LITTERAL:
            FragmentOfSourceCode(
                TypeOfFragmentOfSourceCode.FIELD__OPERANDS,
                Interval(lastMark, end=len(charStream)),
                parent=statementLine,
            )
            raise ValueError("invalid.string.litteral.still.open")

        return statementLine.children
