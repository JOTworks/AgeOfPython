from pprint import pprint

from data import Structure
class Memory: #refactor openMemory away. we can just use used Memory for everything! refactor None instead of ""
    def __init__(self):
        #self.openMemory = [] #list of open goals, they get deleted when in use and added when freed
        self.__usedMemory = [] #list of variable name for used goals, equals "" if open memory
        for itr in range (1,256):
            self.__usedMemory.append("")

    def printUsedMemory(self):
        memoryString = ""
        for itr in range(len(self.__usedMemory)):
            if self.__usedMemory[itr] != "":
                memoryString += str(itr) +" "+self.__usedMemory[itr]+"\n"
        return memoryString
                
    def checkSpace(self):
        if not "" in self.__usedMemory:
            raise Exception("Malloc ERROR RAN OUT OF GOALS!")
    
    def isUsed(self, varName):
        varName = varName.split(".")
        if varName[0] in self.__usedMemory:
            return True
        return False
        
    def getMemLoc(self, varName):
        varNameList = varName.split(".")
        if not self.isUsed(varNameList[0]):
            raise Exception("Can't get memLoc that dosnt exist: "+varName+"\n"+self.printUsedMemory())
        memStartLoc = self.usedMemory.index(varNameList[0]) 
        if (len(varNameList)==1):
            return memStartLoc
        elif(len(varNameList)==2) and (self.usedMemory[memStartLoc+1]==Structure.POINT):
            if varNameList[1]=='x' or varNameList[1]=='0':
                return memStartLoc
            if varNameList[1]=='y' or varNameList[1]=='1':
                return memStartLoc+1

    def mallocInt(self, varName):
        self.checkSpace()
        self.usedMemory[self.openMemory[0]] = varName
        index = self.openMemory[0]
        del self.openMemory[0]
        return index

    def mallocPoint(self, varName):
        self.checkSpace()
        for itr in range(len(self.openMemory)-1):
            if self.openMemory[itr]+1 == self.openMemory[itr+1]:
                self.usedMemory[self.openMemory[itr]] = varName
                self.usedMemory[self.openMemory[itr+1]] = str("Structure.POINT")
                index = self.openMemory[itr]
                del self.openMemory[itr:itr+2]
                return index
        raise Exception("Malloc ERROR RAN OUT OF SPACE FOR A POINT!")
    #victory data is 3
    def mallocState(self, varName): #state and cost
        self.checkSpace()
        for itr in range(len(self.openMemory)-3):
            if (self.openMemory[itr] == self.openMemory[itr+1] + 1) and (self.openMemory[itr] == self.openMemory[itr+2] + 2) and (self.openMemory[itr] == self.openMemory[itr+3] + 3):
                self.usedMemory[self.openMemory[itr]] = varName
                self.usedMemory[self.openMemory[itr+1]] = Structure.State
                self.usedMemory[self.openMemory[itr+3]] = Structure.State
                self.usedMemory[self.openMemory[itr+4]] = Structure.State
                index = self.openMemory[itr]
                del self.openMemory[itr:itr+3]
                return index
        return False
        raise Exception("Malloc ERROR RAN OUT OF SPACE FOR A STATE!")

    def free(self, varName):
        if not varName in self.usedMemory:
            raise Exception ("tried to free"+varName+"but it was not in Memory!")
        index = self.usedMemory.index(varName)
        if self.usedMemory[index+1] == Structure.POINT:
            self.freeGoal(index)
            self.freeGoal(index+1)
        elif self.usedMemory[index+1] == Structure.STATE:
            self.freeGoal(index)
            self.freeGoal(index+1)
            self.freeGoal(index+2)
            self.freeGoal(index+3)
        else:
            self.freeGoal(index)

    def freeGoal(self, goal):
        self.openMemory.append(goal)
        self.usedMemory[goal] = ""