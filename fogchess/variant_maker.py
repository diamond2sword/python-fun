def main()->None:
    cmdDict= [{"desc": "add piece", "call": addPiece},
              {"desc": "del piece", "call": delPiece},
#              {"desc": "edit piece", "call": editPiece},
#              {"desc": "add move", "call": addMove}, 
#              {"desc": "del move", "call": delMove},
#              {"desc": "edit move", "call": editMove},
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

def delPiece(vDict): pass
    

def addPiece(vDict):
    piece= readData(getPieceReadDataParam())
    if piece not in vDict["pieces"]:
        vDict["pieces"].append(piece)

def quitVariantMaker(vDict):
    vDictPath= vDict["vDictPath"]
    if vDict["vDictPath"] == "": vDictPath= input("vDictPath[optional]:")
    if vDictPath == "": quit()
    vDict["vDictPath"]= vDictPath
    try:
        oldVDict= loadJsonToDict(vDictPath)
        if oldVDict == vDict: quit()
        mustSave= "y" == input(f'overwrite \'{vDictPath}\'?[y]:')
        if not mustSave: quit()
        try: saveVariant(vDict, vDictPath)
        except Exception as e:  
            mustCancel= input(f'{e}\nfailed to save, cancel quitting?[y]:')
            if mustCancel: return
    except Exception as e: print(e) 
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
    dictA= {"pieces": [],
            "moves": [],
            "board": {},
            "vDictPath": ""}
    dictA.update(DCP(vDict))
    vDict.update(dictA)
    print("successfully initialized, initializing creates missing mappings of dict")

def loadJsonToDict(jsonPath):
    jsonFile= open(jsonPath, "r")
    jsonDict= json.load(jsonFile)
    return jsonDict


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
import json, ast, pprint, shutil, os
from copy import deepcopy as DCP
if __name__ == "__main__":
    main()
