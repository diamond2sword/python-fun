from typing import TypedDict, cast

def main()->None:
    a: Piece= Piece([1],[3],[{"rank": [4],"file":[0]}],[],[],[],[])
    b: Piece= Piece([0,1],[],[{"rank": [1,2,3,5,6,7],"file":[0]}],[],[],[],[])
    print(a.satisfies(b))
    print(b.varDict)

    B: Board= Board(8, 0)
    B.pieces[0][0].varDict["name"]= [1]
    B.pieces[1][0].varDict["name"]= [2]
    B.spawn(a)
    print(B)
    pass




class Move:
    class Renderer:
        @staticmethod
        def expand(moveA: "Move", boardA: "Board")->list["Move"]:
            resultMoves= []
            moveB: Move= moveA
            for rank,file,pieceA in boardA:
                if not pieceA.satisfies(moveA.varDict["oldPiece"]): continue
                moveB.varDict["oldPiece"]= pieceA
                boardB= boardA
                for iteration in range(moveA.varDict["radius"]):
                    if not boardB.satisfies(moveA):
                        break
                    moveB.varDict["iteration"]= iteration+1
                    resultMoves.append(moveB)
                    for pieceC in moveA.varDict["changes"]:
                        boardB.spawn(pieceC)

                         
            return resultMoves

    def __init__(self,
                 name: int,
                 radius: int,
                 iteration: int,
                 oldPiece: "Piece",
                 newPiece: "Piece",
                 changes: list["Piece"],
                 conditions: list["Piece"],
                 moveParams: list["Move.Param"],)->None:
        self.varDict: Move.VarDict= {"name": name,
                                     "radius": radius,
                                     "iteration": iteration,
                                     "oldPiece": oldPiece,
                                     "newPiece": newPiece,
                                     "changes": changes,
                                     "conditions": conditions,
                                     "moveParams": moveParams,}
        if iteration != 0:
            self.defDict: dict[str,int]= {"x": int(oldPiece.varDict["coordinates"][0]["file"][0]),
                                          "y": int(oldPiece.varDict["coordinates"][0]["rank"][0]),}
            

   
    class VarDict(TypedDict):
        name: int
        radius: int
        iteration: int
        oldPiece: "Piece"
        newPiece: "Piece"
        changes: list["Piece"]
        conditions: list["Piece"]
        moveParams: list["Move.Param"]

    class Param:
        @staticmethod
        def getDefDict(moveParams: list["Move.Param"], 
                       moveParamInputs: dict[str,str],)->dict[str,int]:
            resultDict= {}
            for m in moveParams:
                resultDict.update(m.getDef(moveParamInputs))
            return resultDict 

        def getDef(self, moveParamInputs: dict[str,str])->dict[str,int]:
            resultValue= self.valueDict[moveParamInputs[self.name]]
            return {self.name: resultValue}

        def __init__(self,
                     name: str,
                     valueDict: dict[str,int],)->None:
            self.name= name
            self.valueDict= valueDict


        

                
class Board:
    def spawn(self, piece: "Piece")->None:
        c= piece.varDict["coordinates"][0]
        self.pieces[int(c["file"][0])][int(c["rank"][0])]= piece

    def satisfies(self, move: Move)->bool: 
        for pieceB in move.varDict["conditions"]:
            c= pieceB.varDict["coordinates"][0]
            pieceA= self.pieces[int(c["file"][0])][int(c["rank"][0])]
            if pieceA.satisfies(pieceB):
                continue
            return False
        return True

    def __str__(self)->str:
        text: str=""
        for i in range(self.width):
            for j in range(self.width):
                text+= str(self.pieces[j][self.width-1-i].varDict["name"])
                text+= ","
            text+= "\n"
        return text


    def __init__(self, width: int, team: int)->None:
        self.width= width
        self.team= team
        self.pieces: dict[int,dict[int,Piece]]= {}
        for i in range(self.width):
            self.pieces[i]= {}
            for j in range(self.width):
                self.pieces[i][j]= Piece.EMPTY()
                self.pieces[i][j].varDict["coordinates"]= [{"rank": [j],
                                                            "file": [i],}]

    def __iter__(self)->"Board":
        self.iterN: int= 0
        self.iterMax: int= self.width*self.width
        return self

    def __next__(self)->tuple[int,int,"Piece"]:
        if self.iterN == self.iterMax:
            raise StopIteration
        self.iterN+= 1
        file= self.iterN % self.width
        rank= self.iterN // self.width
        return (file, rank, self.pieces[file][rank])







class Piece:
    def satisfies(self, other: "Piece")->bool:
        for k in self.varDict.keys():
            if other.varDict[k] == []: #type: ignore[literal-required]
                continue
            if self.varDict[k][0] in other.varDict[k]: #type: ignore[literal-required]
                continue
            return False
        return True

    @staticmethod
    def EMPTY()->"Piece":
        return Piece([],
                     [],
                     [],
                     [],
                     [],
                     [],
                     [],)

    def __init__(self, 
                 name: list[int|str], 
                 team: list[int], 
                 coordinates: list[dict[str,list[int|str]]], 
                 whiteLightLevel: list[int], 
                 blackLightLevel: list[int], 
                 recentMove: list[dict[str,list[int]]], 
                 hasMoved: list[bool],)->None:
        self.varDict: Piece.VarDict= {"name": name,
                                      "team": team,
                                      "coordinates": [],
                                      "whiteLightLevel": whiteLightLevel,
                                      "blackLightLevel": blackLightLevel,
                                      "recentMove": [],
                                      "hasMoved": hasMoved,}
        for cDict in coordinates:
            for r in cDict["rank"]:
                for f in cDict["file"]:
                    self.varDict["coordinates"].append({"rank": [r],
                                                        "file": [f]})
        for rDict in recentMove:
            for n in rDict["name"]:
                for i in rDict["iteration"]:
                    self.varDict["recentMove"].append({"name": [n],
                                                       "iteration": [i]})

    class VarDict(TypedDict):
        name: list[int|str]
        team: list[int]
        coordinates: list[dict[str,list[int|str]]]
        whiteLightLevel: list[int]
        blackLightLevel: list[int] 
        recentMove: list[dict[str,list[int]]]
        hasMoved: list[bool]




if __name__ == "__main__":
    main()
