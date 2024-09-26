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
            help="the project wide configuration",
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

            return 0
