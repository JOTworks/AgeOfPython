from pprint import pprint
from enums import Structure
from colorama import Fore, Back, Style
class Memory: #TODO: openMemory away. we can just use used Memory for everything! None instead of ""
    def __init__(self):
        #self.openMemory = [] #list of open goals, they get deleted when in use and added when freed
        self.__usedMemory = [] #list of variable name for used goals, equals "" if open memory
        for itr in range (512):
            self.__usedMemory.append("")
        self.__usedMemory[0] = "***ZERO_INDEX***"

    def printUsedMemory(self):
        memoryString = ""
        for itr in range(len(self.__usedMemory)):
            if self.__usedMemory[itr] != "":
                if isinstance(self.__usedMemory[itr], Structure):
                   memoryString += str(itr) +" "+Fore.LIGHTBLACK_EX+str(self.__usedMemory[itr])+Fore.WHITE+"\n"
                else: 
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

    def get_type(self, varName):
        if not self.isUsed(varName):
            raise Exception(f'{varName} is not allocated')
        memLoc = self.getMemLoc(varName)
        if isinstance(self.__usedMemory[memLoc+1], Structure):
            return self.__usedMemory[memLoc+1]
        else:
            return Structure.INT
       
    def getMemLoc(self, varName):
        varNameList = varName.split(".")
        if not self.isUsed(varNameList[0]):
            raise Exception("Can't get memLoc that dosnt exist: "+varName+"\n"+self.printUsedMemory())
        memStartLoc = self.__usedMemory.index(varNameList[0]) 
        if (len(varNameList)==1):
            return memStartLoc
        if(len(varNameList)==2) and (self.__usedMemory[memStartLoc+1]==Structure.POINT):
            if varNameList[1]=='x' or varNameList[1]=='0':
                return memStartLoc
            if varNameList[1]=='y' or varNameList[1]=='1':
                return memStartLoc+1
        if(len(varNameList)==2) and (self.__usedMemory[memStartLoc+1]==Structure.STATE):
            if varNameList[1]=='local_total' or varNameList[1]=='0':
                return memStartLoc
            if varNameList[1]=='local_last' or varNameList[1]=='1':
                return memStartLoc+1
            if varNameList[1]=='remote_total' or varNameList[1]=='2':
                return memStartLoc+2
            if varNameList[1]=='remote_last' or varNameList[1]=='3':
                return memStartLoc+3
        print(self.printUsedMemory())
        raise Exception (f'didnt get MemLoc! {varName}')

    def malloc(self, varName, s_type):
        if not isinstance(varName, str):
            raise Exception("what are you doing trying to store a none string into memory???")
        if s_type == Structure.INT:
            self.mallocInt(varName)
        elif s_type == Structure.POINT:
            self.mallocPoint(varName)
        elif s_type == Structure.STATE:
            self.mallocState(varName)
        else:
            raise Exception(f'type {s_type}::{type(s_type)} is not a mallocable type')

    def mallocInt(self, varName):
        self.checkSpace()
        index = self.__usedMemory.index('')
        self.__usedMemory[index] = varName
        return index

    def mallocPoint(self, varName):
        self.checkSpace()
        for itr in range(41,len(self.__usedMemory)-1):
            if (self.__usedMemory[itr] == "") and (self.__usedMemory[itr+1] == ""):
                self.__usedMemory[itr] = varName
                self.__usedMemory[itr+1] = Structure.POINT
                return itr
        raise Exception("Malloc ERROR RAN OUT OF SPACE FOR A POINT!")
    #victory data is 3
    def mallocState(self, varName): #state and cost
        self.checkSpace()
        for itr in range(41,len(self.__usedMemory)-3):
            if (self.__usedMemory[itr] == "") and (self.__usedMemory[itr+1] == ""):
                self.__usedMemory[itr] = varName
                self.__usedMemory[itr+1] = Structure.STATE
                self.__usedMemory[itr+2] = Structure.STATE
                self.__usedMemory[itr+3] = Structure.STATE
                return itr
        raise Exception("Malloc ERROR RAN OUT OF SPACE FOR A STATE!")

    def mallocFunction(self, funcName, Returns  ):
        self.checkSpace()

    def free(self, varName):
        if not varName in self.__usedMemory:
            raise Exception ("tried to free"+varName+"but it was not in Memory!")
        index = self.__usedMemory.index(varName)
        if self.usedMemory[index+1] == Structure.POINT:
            self.usedMemory[index] = ""
            self.usedMemory[index+1] = ""
            self.freeGoal(index+1)
        elif self.usedMemory[index+1] == Structure.STATE:
            self.usedMemory[index] = ""
            self.usedMemory[index+1] = ""
            self.usedMemory[index+2] = ""
            self.usedMemory[index+3] = ""
        else:
            self.usedMemory[index] = ""