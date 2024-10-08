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

import filecmp
import io
import os
import shutil
import sys
import time

from contextlib import redirect_stdout
from typing import List
from unittest.mock import patch


def mockStdInput(lines):
    return io.StringIO("\n".join(lines) + "\n")


def makeTmpDirOrDie(suffix: str = None) -> str:
    newdir = os.path.join(".", f"tmp.{suffix}" if suffix != None else "tmp")
    if os.path.exists(newdir):
        if os.path.isdir(newdir):
            return newdir
        raise (ResourceWarning(f"{newdir} is not a directory"))
    os.mkdir(newdir)
    return newdir


def initializeTmpWorkspace(files: List[str]) -> str:
    tmp_dir = makeTmpDirOrDie(f"test_{time.time()}")
    for file in files:
        if file[-2:].upper() == ",A":
            file = file[:-2]
        shutil.copy(file, tmp_dir)
    return tmp_dir


def thenActualFileIsSameAsExpected(pathActual: str, pathExpected: str):
    assert os.path.exists(pathActual)
    assert filecmp.cmp(pathActual, pathExpected, shallow=False)


def verify_cli_behaviour_using_standard_input(
    cli, input_lines: List[str], baseArgs: List[str], expected: str
):
    with patch.object(sys, "argv", baseArgs):
        with patch.object(sys, "stdin", mockStdInput(input_lines)):
            with redirect_stdout(io.StringIO()) as out:
                returnCode = cli.run()
        assert returnCode == 0
        assert out.getvalue() == expected
