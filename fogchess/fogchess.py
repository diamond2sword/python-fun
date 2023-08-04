import ast
from typing import cast
from copy import deepcopy as DCP, copy

def main()->None:
    a: Piece= Piece([1],[3],[{"rank": [4],"file":[0]}],[],[],[],[])
    b: Piece= Piece([0,1],[],[{"rank": [1,2,3,5,6,7],"file":[0]}],[],[],[],[])
    print(a.satisfies(b))
    print(b.__dict__)

    B: Board= Board(8, 0)
    B.pieces[0][0].name= [1]
    B.pieces[1][0].name= [2]
    B.spawn([a])
    print(B)
    
    v: Variant= Variant.fromJson("game.json")

    pass




class Variant:
    @staticmethod
    def fromJson(vDictPath: str)->"Variant":
        vDictFile= open(vDictPath, "r")
        vDictStr= vDictFile.read()
        vDict= ast.literal_eval(vDictStr)
        return Variant(Piece.fromDict(vDict["pieces"]), 
                       Move.fromDict(vDict["moves"]),
                       Board.fromDict(vDict["board"]),)

    def __init__(self, 
                 pieces: list["Piece"], 
                 moves: list["Move"],
                 board: "Board",)->None:
        self.pieces= pieces
        self.moves= moves
        self.board= board
            




class Move: 
    @staticmethod
    def expand(moveA: "Move", boardA: "Board")->list["Move"]:
        resultMoves= []
        moveB= DCP(moveA)
        for file, rank, pieceA in boardA:
            if not pieceA.satisfies(moveA.oldPiece): continue
            moveB.oldPiece= DCP(pieceA)
            pieceNext= DCP(pieceA)
            boardB= DCP(boardA)
            for iteration in range(moveA.radius):
                moveC= DCP(moveB)
                moveC.oldPiece= DCP(pieceNext)
                defDict= moveC.oldPiece.getDefDict()
                moveC.defineWith(defDict)
                if not boardB.satisfies(moveC): break
                moveB.iteration= iteration+1
                resultMoves.append(DCP(moveB))
                boardB.spawn(moveC.changes) 
                pieceNext= DCP(moveC.newPiece)
        return resultMoves

    def defineWith(self, defDict: dict[str,int])->None:
        self.newPiece: "Piece"= self.oldPiece.definePieces([self.newPiece], defDict)[0]
        self.changes: list["Piece"]= self.oldPiece.definePieces(self.changes, defDict)
        self.conditions: list["Piece"]= self.oldPiece.definePieces(self.conditions, defDict)

    @staticmethod
    def fromDict(mDicts: list[dict])->list["Move"]:
        resultMoves= []
        for mDict in mDicts:
            resultMoves.append(Move(mDict["name"],
                                    mDict["radius"],
                                    mDict["iteration"],
                                    Piece.fromDict(mDict["oldPieces"])[0],
                                    Piece.fromDict(mDict["newPiece"])[0],
                                    Piece.fromDict(mDict["changes"]),
                                    Piece.fromDict(mDict["conditions"]),
                                    Move.Param.fromDict(mDict["moveParams"]),))
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
        self.name= name
        self.radius= radius
        self.iteration= iteration
        self.oldPiece= oldPiece
        self.newPiece= newPiece
        self.changes= changes
        self.conditions= conditions
        self.moveParams= moveParams

    class Param:
        @staticmethod
        def makeDefDict(moveParams: list["Move.Param"], 
                       moveParamInputs: dict[str,str],)->dict[str,int]:
            resultDict= {}
            for m in moveParams:
                resultDict.update(m.getDef(moveParamInputs))
            return resultDict 

        def getDef(self, moveParamInputs: dict[str,str])->dict[str,int]:
            resultValue= self.valueDict[moveParamInputs[self.name]]
            return {self.name: resultValue}

        @staticmethod
        def fromDict(paramDicts: list[dict])->list["Move.Param"]:
            resultParams= []
            for paramDict in paramDicts:
                resultParams.append(Move.Param(paramDict["name"],
                                               paramDict["valueDict"],))
            return resultParams

        def __init__(self,
                     name: str,
                     valueDict: dict[str,int],)->None:
            self.name= name
            self.valueDict= valueDict


        

                
class Board:
    def spawn(self, changes: list["Piece"])->None:
        changes= DCP(changes)
        for piece in changes:
            c= piece.coordinates[0]
            self.pieces[int(c["file"][0])][int(c["rank"][0])]= piece

    def satisfies(self, move: Move)->bool: 
        for pieceB in move.conditions:
            c= pieceB.coordinates[0]
            pieceA= self.pieces[cast(int, c["file"][0])][cast(int, c["rank"][0])]
            if pieceA.satisfies(pieceB):
                continue
            return False
        return True

    def __str__(self)->str:
        text= ""
        for i in range(self.width):
            for j in range(self.width):
                text+= str(self.pieces[j][self.width-1-i].name)
                text+= ","
            text+= "\n"
        return text

    @staticmethod
    def fromDict(bDict: dict)->"Board":
        return Board(bDict["width"],
                     bDict["team"],)

    def __init__(self, width: int, team: int)->None:
        self.width= width
        self.team= team
        self.pieces: dict[int,dict[int,Piece]]= {}
        for i in range(self.width):
            self.pieces[i]= {}
            for j in range(self.width):
                self.pieces[i][j]= Piece.EMPTY()
                self.pieces[i][j].coordinates= [{"rank": [j],
                                                 "file": [i],}]

    def __iter__(self)->"Board":
        self.iterN= 0
        self.iterMax= self.width*self.width
        return self

    def __next__(self)->tuple[int,int,"Piece"]:
        if self.iterN == self.iterMax:
            raise StopIteration
        self.iterN+= 1
        file= self.iterN % self.width
        rank= self.iterN // self.width
        return (file, rank, self.pieces[file][rank])







class Piece:
    def definePieces(self, 
                     pieces: list["Piece"],
                     defDict: dict[str,int])->list["Piece"]:
        pieces= DCP(pieces)
        resultPieces= []
        for p in pieces:
            p.name= self.defineVals(p.name, defDict)
            for i in range(len(p.coordinates)):
                p.coordinates[i]["rank"]= self.defineVals(p.coordinates[i]["rank"], defDict)
                p.coordinates[i]["file"]= self.defineVals(p.coordinates[i]["file"], defDict)
            resultPieces.append(p)
        return resultPieces
        
    def defineVals(self, 
                   values: list[int|str], 
                   defDict: dict[str,int],)->list[int|str]:
        resultValues= []
        for v in values:
            v= cast(int|str, eval(str(v), defDict))
            resultValues.append(v)
        return resultValues

    def getDefDict(self)->dict[str,int]:
        return {"x": cast(int, self.coordinates[0]["rank"][0]),
                "y": cast(int, self.coordinates[0]["file"][0]),}

    def satisfies(self, other: "Piece")->bool:
        for k in self.__dict__.keys():
            if other.__dict__[k] == []:
                continue
            if self.__dict__[k][0] in other.__dict__[k]:
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
    @staticmethod
    def fromDict(pDicts: list[dict])->list["Piece"]:
        resultPieces= []
        for pDict in pDicts:
            resultPieces.append(Piece(pDict["name"],
                                      pDict["team"],
                                      pDict["coordinates"],
                                      pDict["whiteLightLevel"],
                                      pDict["blackLightLevel"],
                                      pDict["recentMove"],
                                      pDict["hasMoved"],))
        return resultPieces

    def __init__(self, 
                 name: list[int|str], 
                 team: list[int], 
                 coordinates: list[dict[str,list[int|str]]], 
                 whiteLightLevel: list[int], 
                 blackLightLevel: list[int], 
                 recentMove: list[dict[str,list[int]]], 
                 hasMoved: list[bool],)->None:
        self.name= name
        self.team= team
        self.coordinates: list[dict[str,list[int|str]]]= []
        self.whiteLightLevel= whiteLightLevel
        self.blackLightLevel= blackLightLevel
        self.recentMove: list[dict[str,list[int|str]]]= []
        self.hasMoved= hasMoved
      
        for cDict in coordinates:
            for r in cDict["rank"]:
                for f in cDict["file"]:
                    self.coordinates.append({"rank": [r],
                                             "file": [f]})
        for rDict in recentMove:
            for n in rDict["name"]:
                for i in rDict["iteration"]:
                    self.recentMove.append({"name": [n],
                                            "iteration": [i]})




if __name__ == "__main__":
    main()
