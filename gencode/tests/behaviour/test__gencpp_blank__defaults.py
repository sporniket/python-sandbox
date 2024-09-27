"""
---
(c) 2024 David SPORN
---
This is part of $$$

$$$ is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

$$$ is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with $$$.
If not, see <https://www.gnu.org/licenses/>. 
---
"""

import io
import os
import sys


from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from .utils import initializeTmpWorkspace

from gencpp import GenCppCli

ARGS = ["prog"]
SOURCE_DATA_FILES = os.path.join(".", "tests", "data")
EXPECTED_DATA_FILES = os.path.join(".", "tests", "data.expected")


def thenItHasExpectedFolders(folders: list[str]):
    for f in folders:
        assert os.path.exists(f)
        assert os.path.isdir(f)


def test_that_it_create_files_in_main_directory():
    # Prepare files
    setupFileNames = []
    tmp_dir = initializeTmpWorkspace(
        [os.path.join(SOURCE_DATA_FILES, f) for f in setupFileNames]
    )
    # sourceFileNames = setupFileNames[:-1]
    # sourceFiles = [os.path.join(tmp_dir, f) for f in sourceFileNames]
    # outputFileNames = ["a.out", "a.json"]

    # execute
    with patch.object(sys, "argv", ARGS + ["--root", tmp_dir, "blank", "whatever"]):
        with redirect_stdout(io.StringIO()) as out:
            with redirect_stderr(io.StringIO()) as err:
                returnCode = GenCppCli().run()

    # verify
    assert out.getvalue() == ""
    assert err.getvalue() == ""
    assert returnCode == 0
    thenItHasExpectedFolders(
        [
            os.path.join(tmp_dir, "include"),
            os.path.join(tmp_dir, "src"),
        ]
    )
    # assert that the *.hpp file is created at tmp/include and contains expected content
    # assert that the *.cpp file is created at tmp/src and contains expected content
    # for f in outputFileNames:
    #    thenActualFileIsSameAsExpected(
    #        os.path.join(tmp_dir, f), os.path.join(EXPECTED_DATA_FILES, f)
    #    )
