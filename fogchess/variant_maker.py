def main()->None:
    cmdDict= {0: {"desc": "change path", "call": changePath},
              1: {"desc": "add piece", "call": addPiece},
#              2: {"desc": "del piece", "call": delPiece},
#              3: {"desc": "edit piece", "call": editPiece},
#              4: {"desc": "add move", "call": addMove}, 
#              5: {"desc": "del move", "call": delMove},
#              6: {"desc": "edit move", "call": editMove},
#              7: {"desc": "edit board", "call": editBoard},
#              8: {"desc": "save variant", "call": saveVariant},
              9: {"desc": "quit", "call": None},}
    vDict: dict= {}
    runLoop(vDict, cmdDict)

def runLoop(vDict, cmdDict)->None:
    cmds= cmdDict.keys()
    cmdStr= ""
    for k in cmds:
        desc= cmdDict[k]["desc"]
        cmdStr+= f"\n{k}: {desc}"
    while True:
        print(cmdStr)
        cmd = int(input("cmd:"))
        if cmd not in cmds:
            continue
        if cmdDict[cmd]["call"] == None:
            break
        cmdDict[cmd]["call"](vDict)

def addPiece(vDict):
    resultDict= {}
    resultDict.update({
        "name": readList(param={"desc": "name",
                                "eof": 1,
                                "call": readList,
                                "param": {"desc": "int",
                                          "type": [int]}}),
        "team": readList(param={"desc": "team",
                                "eof": 1,
                                "call": readList,
                                "param": {"desc": "int",
                                          "type": [int]}}),
        "coordinates": readList(param={"desc": "list[coordinates]",
                                       "eof": 1,
                                       "call": readDict,
                                       "param": {"desc": "coordinates",
                                                 "vars": {"file": {"call": readList,
                                                                   "param": {"desc": "file",
                                                                             "eof": 2,
                                                                             "call": readStr,
                                                                             "param": {"desc": "int|str",
                                                                                       "type": [int, str]}}},
                                                          "rank": {"call": readList,
                                                                   "param": {"desc": "rank",
                                                                             "eof": 2,
                                                                             "call": readStr,
                                                                             "param": {"desc": "int|str",
                                                                                       "type": [int, str]}}}}}}),
        })

def changePath(vDict):
    try:
        vDictPath= input("vDictPath:")
        vDictFile= open(vDictPath, "r")
        vDictStr= vDictFile.read()
        vDict.update(ast.literal_eval(vDictStr))
    except:
        pass

def readList(param)->list:
    indent= INDENT * param["eof"]
    eof= f'EOF{param["eof"]}'
    willReadStr= param["call"] == readStr
    if willReadStr: print(f'{indent}{param["desc"]} end?[{eof}]')
    resultList= []
    while True:
        if not willReadStr and input(f'{indent}{param["desc"]} end?[y]:') == "y": break
        data= param["call"](param["param"])
        if willReadStr and  data == eof: break
        resultList.append(data)
    return resultList

def readStr(param):
   desc=  
        
    


INDENT= "  "
import json, ast, pprint
from copy import deepcopy as DCP
if __name__ == "__main__":
    main()
