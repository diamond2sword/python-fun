def main()->None:
    cmdDict= [{"desc": "add piece", "call": addPiece},
              {"desc": "del piece", "call": delPiece},
              {"desc": "add move", "call": addMove}, 
              {"desc": "del move", "call": delMove},
              {"desc": "edit move", "call": editMove},
#              {"desc": "edit board", "call": editBoard},
              {"desc": "init variant", "call": initVariant},
              {"desc": "load variant", "call": loadVariant},
              {"desc": "save variant", "call": saveVariant},

              {"desc": "quit", "call": quitVariantMaker},]
    vDict= {}
    initVariant(vDict)
    runLoop(vDict, cmdDict)

def runLoop(vDict, cmdDict)->None:
    cmdIndexes= [i for i in range(len(cmdDict))]
    cmdStr= ""
    for i in range(len(cmdDict)):
        desc= cmdDict[i]["desc"]
        cmdStr+= f'\n{i}: {desc}'
    while True:
        print(cmdStr)
        #try:
        cmdIndex = int(input("cmd:"))
        if cmdIndex not in cmdIndexes:
            continue
        cmdDict[cmdIndex]["call"](vDict)
        #except Exception as e: print(f'runLoop: {e}')

def editMove(vDict):
    moveBNames= [moveB["name"] for moveB in vDict["moves"]]
    print(f'moves= {moveBNames}')
    if len(moveBNames) == 0: return
    moveAName= readStr(defReadStrParam("edit move", ["int"]))
    if moveAName not in moveBNames: return
    for i in range(len(vDict["moves"])):
        if vDict["moves"][i]["name"] != moveAName: continue
        break
    vDict["moves"][i]= readData(getMoveReadDataParam(),
                                isEditing=True,
                                dataA=vDict["moves"][i],
                                mustPrettyPrint=True)
    

    

    
def delMove(vDict):
    moveBNames= [moveB["name"] for moveB in vDict["moves"]]
    print(f'moves= {moveBNames}')
    if len(moveBNames) == 0: return
    moveAName= readStr(defReadStrParam("delete move", ["int"]))
    if moveAName not in moveBNames: return
    for i in range(len(vDict["moves"])):
        if vDict["moves"][i]["name"] != moveAName: continue
        del vDict["moves"][i]
        break
    print("move successfully removed")


def addMove(vDict):
    moveA= readData(getMoveReadDataParam())
    moveBNames= [moveB["name"] for moveB in vDict["moves"]]  
    if moveA["name"] in moveBNames:
        mustChangeName= "y" == input(f'the name \'{moveA["name"]}\' already used: {moveBNames}\nautomatically change name?[y]:')
        if not mustChangeName: return
        name= -1
        while True:
            name+= 1
            if name in moveBNames: continue
            moveA["name"]= name
            break
        print(f'changed the move\'s name to \'{name}\'')
    pprint.pprint(moveA)
    mustAdd= "y" == input("confirm addition?[y]:")
    if not mustAdd: return
    vDict["moves"].append(moveA)
    print("move successfully added")

def delPiece(vDict):
    print(f'pieces= {vDict["pieces"]}')
    if len(vDict["pieces"]) == 0: return
    piece= readStr(defReadStrParam("delete piece", ["int"]))
    if piece not in vDict["pieces"]: return
    vDict["pieces"].remove(piece)
    print("piece successfully removed")

def addPiece(vDict):
    print(f'pieces= {vDict["pieces"]}')
    piece= readStr(defReadStrParam("add piece", ["int"]))
    if piece in vDict["pieces"]: return
    vDict["pieces"].append(piece)
    print("piece successfully added")

def quitVariantMaker(vDict):
    vDictPath= vDict["vDictPath"]
    mustSave= False
    if vDict != EMPTY_VARIANT_DICT():
        mustSave= "y" == input("save changes?[y]:")
    inputDesc= "required" if mustSave else "optional"
    if vDict["vDictPath"] == "": 
        vDictPath= input(f'vDictPath[{inputDesc}]:')
    if vDictPath == "": quit()
    vDict["vDictPath"]= vDictPath
    if not mustSave: quit()
    try:
        oldVDict= loadJsonToDict(vDictPath)
        if oldVDict == vDict: quit()
        mustOverwrite= "y" == input(f'overwrite \'{vDictPath}\'?[y]:')
    except Exception as e: print(e)
    try: saveVariant(vDict, vDictPath)
    except Exception as e:
        mustCancel= input(f'{e}\nfailed to save, cancel quitting?[y]:')
        if mustCancel: return
    quit()


def saveVariant(vDict, vDictPath="", mustMakeBackup=True):
    def main(vDict, vDictPath):
        if vDictPath == "": vDictPath= vDict["vDictPath"]
        inputDesc= "required" if vDictPath == "" else "optional"
        vDictPath= input(f'vDictPath[{inputDesc}]:')
        if vDictPath == "": return
        vDict["vDictPath"]= vDictPath
        if not os.path.isfile(vDictPath): open(vDictPath,"x")
        try: loadDictToJson(vDictPath)
        except: save(vDict, vDictPath)
        try:
            if mustMakeBackup: backup(vDictPath)
            save(vDict, vDictPath)
        except Exception as e: print(f'saveVariant: failed to save vDict to \'{vDictPath}\'\n{e}')  

    def save(vDict, vDictPath):
        vDictFile= open(vDictPath, "w")
        json.dump(vDict, vDictFile, indent=4, sort_keys=True) 
        print(f'successfully saved vDict to \'{vDictPath}\'') 

    def backup(vDictPath):
        fileName= os.path.basename(vDictPath)
        backupDir= f'.variant-backup/{fileName}'
        os.makedirs(backupDir, exist_ok=True)
        backupList= os.listdir(backupDir)
        backupList.sort(key=int)
        lastBackupName= None if len(backupList) == 0 else int(backupList[-1])
        backupName= 0 if lastBackupName is None else lastBackupName + 1
        backupPath= f'{backupDir}/{backupName}'
        if not os.path.isfile(vDictPath): return
        oldVarDict= loadJsonToDict(vDictPath)
        if lastBackupName is not None:
            lastBackupDict= loadJsonToDict(f'{backupDir}/{lastBackupName}')
            if oldVarDict == lastBackupDict: return
        shutil.copyfile(vDictPath, backupPath)
        print(f'successfully made backup of vDict to \'{backupPath}\'')

    return main(vDict, vDictPath)

def loadVariant(vDict, vDictPath=""):
    inputDesc= "required" if vDictPath == "" else "optional"
    vDictPath= input(f'vDictPath[{inputDesc}]:')
    try:
        vDict.update(loadJsonToDict(vDictPath))
        vDict["vDictPath"]= vDictPath
        print(f'successfully loaded \'{vDictPath}\'')
    except Exception as e: print(f'{e}\nloadVariant: failed to load \'{vDictPath}\'')
    print(f'vDictPath=\'{vDict["vDictPath"]}\'')

def initVariant(vDict):
    dictA= EMPTY_VARIANT_DICT()
    dictA.update(DCP(vDict))
    vDict.update(dictA)
    print("successfully initialized, initializing creates missing mappings of dict")

def loadJsonToDict(jsonPath):
    jsonFile= open(jsonPath, "r")
    jsonDict= json.load(jsonFile)
    return jsonDict

def getMoveReadDataParam():
    def main():
        return defReadDataParam(readDict,
               defReadDictParam("move", [
                   defReadDictMapping("name", readStr,
                       defReadStrParam("", ["int"])),
                   defReadDictMapping("radius", readStr,
                       defReadStrParam("", ["int"])),
                   defReadDictMapping("iteration", readStr,
                       defReadStrParam("", ["int"])),
                   defReadDictMapping("oldPiece", readData, getPieceReadDataParam()),
                   defReadDictMapping("newPiece", readData, getPieceReadDataParam()),
                   defReadDictMapping("changes", readList,
                       defReadListParam("list[pieces]", readData, getPieceReadDataParam())),
                   defReadDictMapping("conditions", readList,
                       defReadListParam("list[pieces]", readData, getPieceReadDataParam())),
                   defReadDictMapping("moveParams", readList,
                       defReadListParam("list[moveParam]", readData, getMoveParamReadDataParam()))]))

    def getMoveParamReadDataParam():
        return defReadDataParam(readDict,
               defReadDictParam("moveParam", [
                   defReadDictMapping("name", readStr,
                       defReadStrParam("", ["str"])),
                   defReadDictMapping("valueDict", readList,
                       defReadListParam("list[mapping]", readDict,
                       defReadDictParam("mapping", [
                           defReadDictMapping("key", readStr,
                              defReadStrParam("", ["str"])),
                           defReadDictMapping("value", readStr,
                              defReadStrParam("", ["int"]))])))]))

    return main()
                   

def getPieceReadDataParam():
    def main():
        return defReadDataParam(readDict,
               defReadDictParam("piece", [
                   *defReadDictStrListMappings({"name": ["int"],
                                               "team": ["int"],
                                               "whiteLightLevel": ["int"],
                                               "blackLightLevel": ["int"],
                                               "hasMoved":["bool"]}),
                   defReadDictMapping("coordinates", readList,
                       defReadListParam("list[coordinates]", readDict,
                       defReadDictParam("coordinates", [
                           *defReadDictStrListMappings({"file": ["int", "str"],
                                                        "rank": ["int", "str"]})]))),
                   defReadDictMapping("recentMove", readList,
                       defReadListParam("list[recentMove]", readDict,
                       defReadDictParam("recentMove", [
                           *defReadDictStrListMappings({"name": ["int", "str"],
                                                        "iteration": ["str"]})])))]))

    def defReadDictStrListMappings(keyTypeDict):
        resultList= []
        for key, typeList in keyTypeDict.items():
             resultList.append(defReadDictMapping(key, readList,
                               defReadListParam(f'list[{key}]', readStr,
                               defReadStrParam("", typeList))))
        return resultList

    return main()

def defReadDataParam(call, callParam):
    return {"call": call,
            "param": callParam}

def defReadDictParam(desc, mappings):
    return {"desc": str(desc),
            "mappings": mappings}

def defReadDictMapping(key, call, callParam):
    calls= [readList, readDict, readStr, readData]
    if call not in calls:
        raise Exception("defReadListParam: call must be in {calls}")
    return {"key": str(key),
            "call": call,
            "param": callParam}


def defReadListParam(desc, call, callParam,):
    calls= [readList, readDict, readStr, readData]
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


def readData(param, nIndent= 0, isEditing=False, dataA=None, mustPrettyPrint=False):
    return param["call"](param["param"], nIndent, isEditing, dataA, mustPrettyPrint)


def readDict(param, nIndent= 0, isEditing=False, dictA=None, mustPrettyPrint=False)->dict:
    indent= INDENT_STR * nIndent
    resultDict={}
    print(f'{indent}readDict: {param["desc"]}')
    if isEditing:
        if mustPrettyPrint: pprint.pprint(dictA)
        mustEdit= "y" == input(f'{indent}readDict: dictA={dictA}, edit?[y]:')
        if not mustEdit: return dictA
        resultDict.update(dictA)
        for mDict in param["mappings"]:
            k= mDict["key"]
            mustEditMapping= "y" == input(f'{indent}readDict: dictA["{k}"]={dictA[k]}, edit?[y]:')
            if not mustEditMapping: continue
            data= mDict["call"](mDict["param"], nIndent+1, isEditing, dictA[k], mustPrettyPrint)
            resultDict.update({mDict["key"]: data})
        return resultDict
    for mDict in param["mappings"]:
        print(f'{indent}readDict: mapping key \'{mDict["key"]}\'')
        data= mDict["call"](mDict["param"], nIndent+1)
        resultDict.update({mDict["key"]: data})
    return resultDict


def readList(param, nIndent= 0, isEditing=False, listA=None, mustPrettyPrint=False)->list:
    indent= INDENT_STR * nIndent
    resultList= []
    if isEditing:
        mustEdit= "y" == input(f'{indent}readList: listA={listA}, edit?[y]:')
        if not mustEdit: return listA
        for i in range(len(listA)):
            mustEditElement= input(f'{indent}readList: listA[{i}]={listA[i]}, edit?[y]:')
            if not mustEditElement: break
            while True:
                data= param["call"](param["param"], nIndent+1, isEditing, listA[i], mustPrettyPrint)
                if data in resultList:
                    print(f'{indent}readList: input already in the list')
                    continue
                resultList.append(data)
    while True:
        mustClose= "y" == input(f'{indent}readList: {param["desc"]}, close list?[y]:') 
        if mustClose: break
        data= param["call"](param["param"], nIndent+1)
        if data in resultList:
            print(f'{indent}readList: input already in the list')
            continue
        resultList.append(data)
    return resultList


def readStr(param, nIndent=0, isEditing=False, dataA=None, mustPrettyPrint=False):
    indent= INDENT_STR * nIndent
    isTypeValid= False
    if isEditing:
        mustEdit= "y" == input(f'{indent}readStr: dataA={dataA}, edit?[y]:')
        if not mustEdit: return dataA
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



 




        
    

def EMPTY_VARIANT_DICT(): return {"pieces": [],
                                  "moves": [],
                                  "board": {},
                                  "vDictPath": ""}
INDENT_STR= "  "                 
import json, ast, pprint, shutil, os
from copy import deepcopy as DCP
if __name__ == "__main__":
    main()
