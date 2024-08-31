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

import os
import shutil
import time
import sys
import io
from typing import List, Union, Optional

from unittest.mock import patch
from contextlib import redirect_stdout, redirect_stderr

from isa_m68k.assembly import AssemblyCli

from .utils import (
    initializeTmpWorkspace,
    thenActualFileIsSameAsExpected,
)


ARGS = ["prog"]
SOURCE_DATA_FILES = os.path.join(".", "tests", "data")
EXPECTED_DATA_FILES = os.path.join(".", "tests", "data.expected")


def test_that_it_compile_a_minimal_source_into_machine_language():
    # Prepare files
    setupFileNames = ["justquit.s"]
    tmp_dir = initializeTmpWorkspace(
        [os.path.join(SOURCE_DATA_FILES, f) for f in setupFileNames]
    )
    sourceFileNames = setupFileNames[:-1]
    sourceFiles = [os.path.join(tmp_dir, f) for f in sourceFileNames]
    outputFileNames = ["a.out", "a.json"]

    # execute
    with patch.object(sys, "argv", ARGS + sourceFiles):
        with redirect_stdout(io.StringIO()) as out:
            with redirect_stderr(io.StringIO()) as err:
                returnCode = AssemblyCli().run()

    # verify
    assert returnCode == 0
    for f in outputFileNames:
        thenActualFileIsSameAsExpected(
            os.path.join(tmp_dir, f), os.path.join(EXPECTED_DATA_FILES, f)
        )
