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
        "name": readData(
            defReadDataParam(readList,
            defReadListParam("list[name]", readStr, 
            defReadStrParam("", ["int"])))),
        "team": readData(
            defReadDataParam(readList,
            defReadListParam("list[team]", readStr,
            defReadStrParam("", ["int"])))),
        "coordinates": readData(
            defReadDataParam(readList,
            defReadListParam("list[coordinates]", readDict,
            defReadDictParam("coordinates", [
                defReadDictMapping("file", readList,
                defReadListParam("list[file]", readStr,
                defReadStrParam("", ["int", "str"]))),
                defReadDictMapping("rank", readList,
                defReadListParam("list[rank]", readStr,
                defReadStrParam("", ["int", "str"])))])))),
        "whiteLightLevel": readData(
            defReadDataParam(readList,
            defReadListParam("list[whiteLightLevel]", readStr,
            defReadStrParam("", ["int"])))),
        "blackLightLevel": readData(
            defReadDataParam(readList,
            defReadListParam("list[blackLightLevel]", readStr,
            defReadStrParam("", ["int"])))),
        "recentMove": readData(
            defReadDataParam(readList,
            defReadListParam("list[recentMove]", readDict,
            defReadDictParam("recentMove", [
                defReadDictMapping("file", readList,
                defReadListParam("list[name]", readStr,
                defReadStrParam("", ["int", "str"]))),
                defReadDictMapping("rank", readList,
                defReadListParam("list[iteration]", readStr,
                defReadStrParam("", ["int", "str"])))])))),
        "hasMoved": readData(
            defRead

    })

def changePath(vDict):
    try:
        vDictPath= input("vDictPath:")
        vDictFile= open(vDictPath, "r")
        vDictStr= vDictFile.read()
        vDict.update(ast.literal_eval(vDictStr))
    except:
        pass

def defReadDataParam(call, callParam):
    return {"call": call,
            "param": callParam}

def defReadDictParam(desc, mappings):
    return {"desc": str(desc),
            "mappings": mappings}

def defReadDictMapping(key, call, callParam):
    calls= [readList, readDict, readStr]
    if call not in calls:
        raise Exception("defReadListParam: call must be in {calls}")
    return {"key": str(key),
            "call": call,
            "param": callParam}


def defReadListParam(desc, call, callParam,):
    calls= [readList, readDict, readStr]
    if call not in calls:
        raise Exception("defReadListParam: call must be in {calls}")
    return {"desc": str(desc),
            "call": call,
            "param": callParam} 

def defReadStrParam(desc, typeList):
    pTypes= ["int","str","float","bool"]
    for t in typeList:
        if t in pTypes: continue
        raise Exception(f'defReadStrParam: type \'{t}\' is not in {pTypes}')
    return {"desc": str(desc),
            "type": typeList}

def readData(param):
    return param["call"](param["param"])
    

def readDict(param, nIndent= 0)->dict:
    indent= INDENT_STR * nIndent
    resultDict={}
    print(f'{indent}readDict: {param["desc"]}')
    for mDict in param["mappings"]:
        print(f'{indent}readDict: mapping key \'{mDict["key"]}\'')
        data= mDict["call"](mDict["param"], nIndent+1)
        resultDict[mDict["key"]]= data
    return resultDict
        

def readList(param, nIndent= 0)->list:
    indent= INDENT_STR * nIndent
    resultList= []
    while True:
        if input(f'{indent}readList: {param["desc"]}, close list?[y]:') == "y": break
        data= param["call"](param["param"], nIndent+1)
        if data in resultList:
            print(f'{indent}readList: input already in the list')
            continue
        resultList.append(data)
    return resultList


def readStr(param, nIndent= 0):
    indent= INDENT_STR * nIndent
    isTypeValid= False
    while True:
        data= input(f'{indent}readStr: {param["type"]}{param["desc"]}:')
        for castType in param["type"]:
            try:
                data= eval(f'{castType}(\'{data}\')')
                isTypeValid= True
            except: pass
        if isTypeValid: break
        print(f'{indent}readStr: input type of \'{data}\' not in {param["type"]}')
    return data

 




        
    


INDENT_STR= "  "
import json, ast, pprint
from copy import deepcopy as DCP
if __name__ == "__main__":
    main()
