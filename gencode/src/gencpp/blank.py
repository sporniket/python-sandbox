"""
---
(c) 2024 David SPORN
---
This is part of Gencode -- whatever.

Gencode is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

Gencode is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with Gencode.
If not, see <https://www.gnu.org/licenses/>. 
---
"""

import os
import re
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter


class GeneratorOfBlankFiles:
    def __init__(self):
        pass

    def appendSubParser(self, codename: str, subparser):
        # TODO Rewrite parser as needed
        parser = subparser.add_parser(
            codename,
            help="Generate empty CPP file and its empty header file.",
        )

        # Add the arguments
        parser.add_argument(
            "--config",
            metavar="<config>",
            type=str,
            help="the project wide configuration file",
        )

        parser.add_argument(
            "--root",
            metavar="<rootdir>",
            type=str,
            default=".",
            help="the relative path of the project, defaults to the current path",
        )

        parser.add_argument(
            "params",
            metavar="<parameter...>",
            type=str,
            nargs="+",
            help="a non-empty list of specific parameters required by the template",
        )

        parser.set_defaults(func=self.run)

    def checkFolderOrMake(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            raise ValueError(f"not.directory:{path}")

    def run(self, args):
        if args.config:
            # TODO initialise default configuration and override with config file
            pass
        else:
            # TODO initialise default configuration
            pass
        # TODO get code generator : generator = codegen[args.generator]
        # TODO call generator : generator.perform(config, args.params)
        # TODO the generator should use its own argparse to display help or validate the parameters

        # That part should be put inside the generator
        # It would support a root directory, and an optionnal library name
        rootPath = "."
        if args.root:
            only_dots = re.compile(r"[.]+")
            parts = [f for f in args.root.split("/") if f and not only_dots.match(f)]
            rootPath = os.path.join(rootPath, *parts)

        self.checkFolderOrMake(os.path.join(rootPath, "include"))
        self.checkFolderOrMake(os.path.join(rootPath, "src"))

        return 0
