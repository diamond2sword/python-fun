import typing
from copy import deepcopy, copy

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
    pass




class Move:
    class Renderer:
        @staticmethod
        def expand(moveA: "Move", boardA: "Board")->list["Move"]:
            resultMoves= []
            moveB: Move= deepcopy(moveA)
            for rank, file, pieceA in boardA:
                if not pieceA.satisfies(moveA.oldPiece): continue
                moveB.oldPiece= pieceA
                boardB= deepcopy(boardA)
                for iteration in range(moveA.radius):
                    if not boardB.satisfies(moveA):
                        break
                    moveB.iteration= iteration+1
                    resultMoves.append(deepcopy(moveB))
                    boardB.spawn(moveA.changes) 
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
        if iteration != 0:
            self.defDict: dict[str,int]= {"x": int(oldPiece.coordinates[0]["file"][0]),
                                          "y": int(oldPiece.coordinates[0]["rank"][0]),}
            

   

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
    def spawn(self, changes: list["Piece"])->None:
        for piece in changes:
            c= piece.coordinates[0]
            self.pieces[int(c["file"][0])][int(c["rank"][0])]= deepcopy(piece)

    def satisfies(self, move: Move)->bool: 
        for pieceB in move.conditions:
            c= pieceB.coordinates[0]
            pieceA= self.pieces[int(c["file"][0])][int(c["rank"][0])]
            if pieceA.satisfies(pieceB):
                continue
            return False
        return True

    def __str__(self)->str:
        text: str=""
        for i in range(self.width):
            for j in range(self.width):
                text+= str(self.pieces[j][self.width-1-i].name)
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
                self.pieces[i][j].coordinates= [{"rank": [j],
                                                 "file": [i],}]

    def __iter__(self)->"Board":
        self.iterN: int= 0
        self.iterMax: int= self.width*self.width
        return self

    def __next__(self)->tuple[int,int,"Piece"]:
        if self.iterN == self.iterMax:
            raise StopIteration
        self.iterN+= 1
        file: int= self.iterN % self.width
        rank: int= self.iterN // self.width
        return (file, rank, self.pieces[file][rank])







class Piece:
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
        self.coordinates= []
        self.whiteLightLevel= whiteLightLevel
        self.blackLightLevel= blackLightLevel
        self.recentMove= []
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
