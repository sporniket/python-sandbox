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
from ...py_models import Interval


from .fragment import TypeOfFragmentOfSourceCode, FragmentOfSourceCode
from .specialChars import MARKER__SUFFIX_OF_OPERATION_CODE


class FragmenterOfMnemonicField:
    def __init__(self):
        pass

    def fragment(
        self, mnemonic: FragmentOfSourceCode, charStream: str
    ) -> list[FragmentOfSourceCode]:
        if mnemonic.type != TypeOfFragmentOfSourceCode.FIELD__MNEMONIC:
            raise ValueError(f"invalid.fragment.not.a.mnemonic.field:{mnemonic.type}")
        extract = charStream[mnemonic.absoluteStart : mnemonic.absoluteEnd]
        sizeOfExtract = len(extract)
        indexSeparator = extract.rfind(MARKER__SUFFIX_OF_OPERATION_CODE)
        if indexSeparator > -1:
            # there is a separator
            afterSeparator = indexSeparator + 1
            if indexSeparator > 0:
                FragmentOfSourceCode(
                    TypeOfFragmentOfSourceCode.MNEMONIC__RADIX,
                    Interval(0, end=indexSeparator),
                    parent=mnemonic,
                )
            if sizeOfExtract > afterSeparator:
                FragmentOfSourceCode(
                    TypeOfFragmentOfSourceCode.MNEMONIC__SUFFIX,
                    Interval(afterSeparator, end=sizeOfExtract),
                    parent=mnemonic,
                )
        else:
            if sizeOfExtract > 0:
                FragmentOfSourceCode(
                    TypeOfFragmentOfSourceCode.MNEMONIC__RADIX,
                    Interval(0, end=sizeOfExtract),
                    parent=mnemonic,
                )

        return mnemonic.children
