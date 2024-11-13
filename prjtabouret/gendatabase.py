#!/usr/bin/env python3

import json
import sys

def initStructRoot(x):
    for n in ["GAL16V8_Registered","GAL16V8_Complex","GAL16V8_Simple"]:
        x[n] = {}
        for s in [
            "pins",
            # "specials",
            # "blocks",
            "macrocells",
            "switches","globals"
        ]:
            x[n][s] = None

def initGlobals(x, modeName, modeValue):
    x["globals"] = {
        "__doc__":[f"# Global configuration fuses setting for '{modeName}'"],
        "mode":{ # AC1 fuse
            "fuses":[2192, 2193], # SYN, AC0
            "values":{
                #"registered":2,
                f"{modeName}":modeValue,
                #"simple":1
            }
        }
    }

def initArray(x):
    x["array"] = {
        "__doc__":[
            "# Entries of the AND Array",
            "",
            "The AND Array (64 lines of 32 columns) has 16 entries that are injected into it, as well as the inverted value of each entries.",
            "",
            "Each entry value (normal and inverted) is connected to a column of the AND Array, and is fed by a pad or the feedback of the macrocells.",
        ]
    }
    def makeEntry(x, name:str, offsetNormal:int, source:str):
        x[name] = {
            "offsetNormal":offsetNormal,
            "offsetInverted":offsetNormal+1,
            "source":source
        }
    
    for specs in [
        ["E1", 0, ]
    ]:
        # HERE TODO
        pass

def initMacroCells(x):
    x["macrocells"] = {
        "__doc__":[
            "# Description of each macrocell",
            "",
            "* **pad name** : for most pins, where the inputs and output pins physically connect to the dye ; for pins 1 and 11, it will designate a named net that will be either the 'normal' input, either the special net like 'clock' or 'output enable'.",
            "* **pterm ranges** : for each of the 8 product terms that are inputs of a given macro cell, the range of 32 fuses that control each term.",
            "* **pterm disable** : for each of the 8 product terms that are inputs of a given macro cell, the fuse that disable said product term.",
            "* **configuration fuse** : each cell has a local configuration fuse to change its behaviour.",
            "* **polarity** : fuse to setup whether the output is active high or low, in other word, normal or inverted output."
        ]
    }
    for i in range(0,8):
        ptermsOffset = 256 * i
        ptdOffset=2128 + 8*i

        x["macrocells"][f"MC{i+1}"] = {
            "pad":f"M{i+1}",
            "pterm_ranges":{f"PT{j+1}":[ptermsOffset+32*j,ptermsOffset+32*(j+1)] for j in range(0,8)},
            "pterm_disables":{f"PTD{j+1}":ptdOffset+j for j in range(0,8)},
            "configuration":{
                "fuses":[2120+i],
                "values":{
                    "registered":0,
                    "combinatorial":1
                }
            },
            "polarity":{
                "fuses":[2048+i],
                "values":{
                    "active low":0,
                    "active high":1
                }
            }
        }

def initPins(x,*, pin1:str="I1", pin11:str = "I10"):
    x["pins"] = {
        "__doc__":[
            "# Mapping of physical pin index to a pad name",
            "",
            "VCC and GND are dropped as the play no role in the logic."
        ]
    }
    for pkg in ["DIP20","PLCC20"]:
        # DIP and PLCC have in fact the same mapping
        # Each physical pin is wired to a given pad
        # Pin 1 and 11 have specific setups
        x["pins"][pkg] = {1:pin1}
        x["pins"][pkg].update({j:f"I{j}" for j in range(2,10)})
        x["pins"][pkg].update({11:pin11}) 
        x["pins"][pkg].update({12+j:f"M{8-j}" for j in range(0,8)})


if __name__ == '__main__':
    targetFileName="database"
    print(f"generate {targetFileName}.json ...")
    print()

    # 1.
    result = {
        "__doc__":[
            "# Database for the GAL16v8 PLD",
            "",
            "Each item describe a global configuration of the device, namely the 'registered' mode, the 'complex' mode and the 'simple' mode."
        ]
    }
    initStructRoot(result)    

    # 2.
    for specs in [["GAL16V8_Registered","registered",2],["GAL16V8_Complex","complex",3],["GAL16V8_Simple","simple",1]]:
        initGlobals(result[specs[0]],specs[1],specs[2])

    # 3.
    for specs in [["GAL16V8_Registered"],["GAL16V8_Complex"],["GAL16V8_Simple"]]:
        initArray(result[specs[0]])

    # 4.
    for specs in [["GAL16V8_Registered"],["GAL16V8_Complex"],["GAL16V8_Simple"]]:
        initMacroCells(result[specs[0]])

    # 7
    for specs in [["GAL16V8_Registered","CLK","OE"],["GAL16V8_Complex"],["GAL16V8_Simple"]]:
        if len(specs)>1:
            initPins(result[specs[0]],pin1=specs[1],pin11=specs[2])
        else:
            initPins(result[specs[0]])

    # save to file
    with open(f"./{targetFileName}.json", encoding="utf-8", mode="w") as f:
        json.dump(result, f, indent=4)

    # end.
    print("DONE.")
