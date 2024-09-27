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


class GenCppCli:
    @staticmethod
    def createArgParser() -> ArgumentParser:
        # TODO Rewrite parser as needed
        parser = ArgumentParser(
            prog="python3 -m gencode.gencpp",
            description="Generate CPP code files tree or snippet.",
            epilog="""---
(c) 2024 David SPORN
---
This is part of Gencode -- Sporniket's generator of code.

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
""",
            formatter_class=RawDescriptionHelpFormatter,
            allow_abbrev=False,
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
            "generator",
            metavar="<generator>",
            type=str,
            nargs=1,
            help="the name of the generator",
        )

        parser.add_argument(
            "params",
            metavar="<parameter>",
            type=str,
            nargs="*",
            help="a non-empty list of specific parameters required by the template",
        )

        return parser

    def __init__(self):
        pass

    def checkFolderOrMake(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            raise ValueError(f"not.directory:{path}")

    def run(self):
        try:
            args = GenCppCli.createArgParser().parse_args()
            # TODO other things that may throw a value error
        except ValueError as e:
            print(e, file=sys.stderr)
            return 1
        else:
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
                parts = [
                    f for f in args.root.split("/") if f and not only_dots.match(f)
                ]
                rootPath = os.path.join(rootPath, *parts)

            self.checkFolderOrMake(os.path.join(rootPath, "include"))
            self.checkFolderOrMake(os.path.join(rootPath, "src"))

            return 0
