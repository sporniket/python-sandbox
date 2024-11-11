#!/usr/bin/env python3

import json
import sys

def initStructRoot(x):
    for n in ["GAL16V8_Registered","GAL16V8_Complex","GAL16V8_Simple"]:
        x[n] = {}
        for s in [
            "pins","specials",
            # "blocks",
            "macrocells",
            "switches","globals"
        ]:
            x[n][s] = None

def initGlobals(x, modeName, modeValue):
    x["globals"] = {
        "mode":{ # AC1 fuse
            "fuses":[2192, 2193], # SYN, AC0
            "values":{
                #"registered":2,
                f"{modeName}":modeValue,
                #"simple":1
            }
        }
    }

def initSwitches(x):
    def makeUimBody(i):
        offset = 32 * i
        return {
            #"block": "A",
            "mux": {
                "fuses": [f+offset for f in range(0,32)]
            }
        }
    x["switches"] = {f"UIM{i}":makeUimBody(i) for i in range(0,64)}

def initMacroCells(x):
    x["macrocells"] = {}
    for i in range(0,8):
        ptermsOffset = 256 * i
        ptdOffset=2128 + 8*i

        x["macrocells"][f"MC{i+1}"] = {
            # "block":"A",
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

def initSpecials(x):
    x["GAL16V8_Registered"]["specials"]={
      "CLK":"C1",
      "OE":"E1"
    }
    x["GAL16V8_Complex"]["specials"]={
    }
    x["GAL16V8_Simple"]["specials"]={
    }

if __name__ == '__main__':
    targetFileName="database"
    print(f"generate {targetFileName}.json ...")
    print()

    # 1.
    result = {}
    initStructRoot(result)    

    # 2.
    for specs in [["GAL16V8_Registered","registered",2],["GAL16V8_Complex","complex",3],["GAL16V8_Simple","simple",1]]:
        initGlobals(result[specs[0]],specs[1],specs[2])

    # 3.
    for specs in [["GAL16V8_Registered"],["GAL16V8_Complex"],["GAL16V8_Simple"]]:
        initSwitches(result[specs[0]])

    # 4.
    for specs in [["GAL16V8_Registered"],["GAL16V8_Complex"],["GAL16V8_Simple"]]:
        initMacroCells(result[specs[0]])

    # 5
    initSpecials(result)

    # save to file
    with open(f"./{targetFileName}.json", encoding="utf-8", mode="w") as f:
        json.dump(result, f, indent=4)

    # end.
    print("DONE.")
