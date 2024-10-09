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

from gencode_lib import Identifier

import jinja2

TEMPLATE_SOURCES = {
    "licence": """// no licence -- project '{{LABEL_PROJECT}}'""",
    "source_header": """{{LICENCE}}
#ifndef {{CODE_GUARD}}
#define {{CODE_GUARD}}
// ================[ CODE BEGINS ]================

// ...your code...

// ================[ END OF CODE ]================
#endif""",
    "source_main": """{{LICENCE}}
#include "{{NAME_HEADER}}.hpp"

// ...your code...

""",
}


class GeneratorOfBlankFiles:
    def __init__(self):
        env = jinja2.Environment()
        templates = {}
        for key in TEMPLATE_SOURCES:
            templates[key] = env.from_string(TEMPLATE_SOURCES[key])
        self._templates = templates

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

    def computeLicence(
        self, projectLabel: str = "???", projectLicence: str = None
    ) -> str:
        return self._templates["licence"].render({"LABEL_PROJECT": projectLabel})

    def computeHeaderFileBody(self, args, config):
        return self._templates["source_header"].render(
            {
                "CODE_GUARD": Identifier(f"{args.params[0]}.hpp").allcaps,
                "LICENCE": self.computeLicence(),
            }
        )

    def computeProgramFileBody(self, args, config):
        return self._templates["source_main"].render(
            {"NAME_HEADER": args.params[0], "LICENCE": self.computeLicence()}
        )

    def generateHeaderFile(self, rootPath, args, config):
        target = os.path.join(rootPath, "include", args.params[0] + ".hpp")
        try:
            with open(target, "x") as out:
                source = self.computeHeaderFileBody(args, config)
                out.write(source)
        except FileExistsError:
            print(f"error.file.exists:{target}")

    def generateProgramFile(self, rootPath, args, config):
        target = os.path.join(rootPath, "src", args.params[0] + ".cpp")
        try:
            with open(target, "x") as out:
                source = self.computeProgramFileBody(args, config)
                out.write(source)
        except FileExistsError:
            print(f"error.file.exists:{target}")

    def run(self, args):
        if args.config:
            # TODO initialise default configuration and override with config file
            pass
        else:
            # TODO initialise default configuration
            pass

        rootPath = "."
        if args.root:
            only_dots = re.compile(r"[.]+")
            parts = [f for f in args.root.split("/") if f and not only_dots.match(f)]
            rootPath = os.path.join(rootPath, *parts)

        self.checkFolderOrMake(os.path.join(rootPath, "include"))
        self.checkFolderOrMake(os.path.join(rootPath, "src"))

        self.generateHeaderFile(rootPath, args, None)
        self.generateProgramFile(rootPath, args, None)

        return 0
