import os
from glob import glob
from time import sleep

class Bucket(object):
    def __init__(self):
        self.cont = []
    
    def __str__(self):
        return self.cont[0] if len(self.cont) > 0 else ""

    def add(self, obj):
        if len(self.cont) == 0:
            self.cont.append(obj)
        else:
            raise IndexError

    def pop(self):
        if len(self.cont) == 0:
            raise IndexError
        return self.cont.pop(0)

    def clear(self):
        self.cont = []

    def undo(self, obj=None):
        if obj == None:
            return self.pop()
        self.cont.append(obj)
    
    @property
    def type(self):
        return "BUCKET"
    
        
class Queue(object):
    def __init__(self, word=""):
        self.cont = [x for x in word]

    def __str__(self):
        items = ""
        for item in self.cont: items += item
        return items

    def add(self, obj):
        self.cont.append(obj)

    def pop(self):
        return self.cont.pop(0)

    def clear(self):
        self.cont = []

    def undo(self, obj=None):
        if obj == None:
            return self.cont.pop()
        self.cont.insert(0, obj)
    
    @property
    def type(self):
        return "QUEUE"


class Stack(object):
    def __init__(self):
        self.cont = []

    def __str__(self):
        items = ""
        for item in self.cont: items += item
        return items

    def add(self, obj):
        self.cont.append(obj)

    def pop(self):
        return self.cont.pop();

    def clear(self):
        self.cont = []

    def undo(self,obj=None):
        if obj == None:
            return self.cont.pop()
        self.cont.append(obj)
    
    @property
    def type(self):
        return "STACK"



class Task(object):
    tasks = ["AAABBN", 
             "AAANNB", 
             "BBAAAN",
             "BBNAAA",
             "NNAAAB",
             "NNBAAA",
             "ANANAB",
             "NABANA",
             "NANANANABATMAN"]

    def __init__(self, taskid, container):
        self.taskid = taskid-1
        self.moves = []   #list of str
        self.history = []
        self.history.append(self._createrow(['','BANANA','',''])) 
        self.source = Queue("BANANA")
        self.goal = Stack()
        self.container = container

    @property
    def task(self):
        return self.tasks[self.taskid]
        
        
    def add_history(self):
        self.history.append(self._createrow([
            self.moves[len(self.moves)-1],
            str(self.source), 
            str(self.goal),
            str(self.container)]))

    def check(self):
        print(str(self.goal), self.task)
        return True if str(self.goal) == self.task else False

    def move(self):
        letter = self.source.pop()
        self.goal.add(letter)
        self.moves.append("MOVE "+letter)
        self.add_history()

    def put(self):
        letter = self.source.pop()
        self.container.add(letter)
        self.moves.append("PUT "+letter)
        self.add_history()

    def get(self):
        letter = self.container.pop()
        self.goal.add(letter)
        self.moves.append("GET "+letter)
        self.add_history()

    def undo(self):
        prevmove = self.moves.pop()
        self.history.pop()
        if prevmove[0] == "P":
            self.source.undo(self.container.undo())
        elif prevmove[0] == "M":
            self.source.undo(self.goal.undo())
        elif prevmove[0] == "G":
            self.container.undo(self.goal.undo())
            

    def retry(self):
        self.moves = []
        self.history = []
        self.history.append(self._createrow(['','BANANA','',''])) 
        self.source = Queue("BANANA")
        self.goal = Stack()
        self.container.clear()

    def save(self):
        filename = "ex1_task%d.txt"%self.taskid
        used = []
        pastlines = []
        if os.path.isfile(filename):
            check = open(filename, 'r')
            used = check.readline().strip().split(',')
            pastlines = check.readlines()
            check.close()
            if self.container.type in used:
                print("You've already completed this task using this container")
                return
        if len(used) > 0 and used[0] == "NONE":
            used = []
        savefile = open(filename, "w")
        savefile.write(','.join(used+[self.container.type])+'\n\n')
        if len(pastlines) > 0:
            savefile.writelines(pastlines[1:])
            savefile.write('\n\n')

        savefile.write(self._createrow(["OPER","SOURCE", "GOAL", self.container.type])+'\n')
        for item in self.history:
            savefile.write(item+'\n')
        savefile.close()

    def Print(self):
        #for i in range(len(self.moves)):
        #    print(str(i+1)+". " + self.moves[i])
        #print ("")

        print(self._createrow(["OPER","SOURCE", "GOAL", self.container.type]))
        for move in self.history:
            print(move)
        print("")
        print("Goal:", self.task)

    def _createrow(self, columns):
        # WARNING: impressively obscure code ahead
        #          ...Read at your own risk!
        
        row = ""
        for col in columns:
            row += col
            for i in range(len(self.task)-len(col)): row += " "
            row += " | "
        return row


def Clear():
    '''
    Clears the terminal screen. However, 
    since WingIDE does not support any method of clearing
    the terminal, I will simply print a couple of newlines
    '''
    print("\n"*25)
#def SaveAll():
#    savefiles = glob("ex1_task*.txt")
#
#    data = {}
#    used = {}
#    for filename in savefiles:
#        if filename[8].isnumeric and int(filename[8]) < 10:
#            file = open(filename, 'r')
#            used[int(filename[8])] = file.readline()
#            data[int(filename[8])] = file.readlines()
#            file.close()
#    keys = list(data.keys())
#    keys.sort()
#    #write the data to file
#    file = open("ex1.txt", 'w')
#    for key in keys:
#        file.write('%d: %s - Solved using %s\n'%(key+1, Task.tasks[key],used[key]))
#        file.writelines(data[key])
#        file.write("\n\n")
#    file.close()
#    print("Saved to ex1.txt!")


def SaveAll():
    savefiles = glob("ex1_task*.txt")
    
    data ={}
    for filename in savefiles:
        if filename[8].isnumeric and int(filename[8]) < 10:
            file = open(filename, 'r')
            data[int(filename[8])] = file.readlines()
            file.close()
    keys = list(data.keys())
    keys.sort()
    #write the data to file
    file = open("ex1.txt", 'w')
    for key in keys:
        file.write('%d: %s\n'%(key+1, Task.tasks[key]))
        file.write("Can be solved with: ")
        file.writelines(data[key])
        file.write("\n\n")
    file.close()
    print("Saved to ex1.txt!")
        


def Container(id):
    choices = [Bucket, Queue, Stack]
    inp = -1
    while True:
        print ("Now choose which container you wish to use [%s]:"%Task.tasks[id])
        print ("1) Bucket")
        print ("2) Queue")
        print ("3) Stack")
        inp = input("Number from 1 to 3: ")
        if inp.isnumeric() and int(inp) > 0 and int(inp) < 4:
            break
        print("invalid input")
    return choices[int(inp)-1]()

def Menu():
    inp = -1
    while True:
        print("Task ID (1-9)")
        print("10) Combine all saved tasks into ex1.txt")
        print("11) exit")
        inp = input(">> ")
        
        if inp.isnumeric() and int(inp) > 0 and int(inp) < 12:
            break #Brian is gonna hate this...
        
        print("invalid input")
    
    if int(inp) == 10:
        SaveAll()
    inp = int(inp)
    return Task(inp, Container(inp)) if inp < 10 else inp


def Help():
    helpstr = '''
    Here are a list of commands:
    imp     - Mark the task as impossible and try a different one
    move    - Add the next letter of source to the end of goal
    put     - Put the next letter from source word into the container
    get     - Remove a letter from the container and add to end of goal
    undo    - Undo the previous move/put/get
    save    - Saves your instructions to a file
    retry   - Restarts from beginning
    menu    - Choose a new task to complete
    exit    - Exits this program
    help    - Displays this help
    '''
    print(helpstr)
    input("Press enter to continue...")
    
def Start():
    task = Menu()
    if type(task) == int:
        return
    choices = {
        "move": task.move,
        "put": task.put,
        "get": task.get,
        "undo": task.undo,
        "help": Help
    }

    Help()
    print("Good Luck!\n\n")
    
    done = False
    while not done:
        task.Print()
        inp = input(">> ").lower().strip()
        if inp == "menu":
            # Too lazy to do it properly, lets just recurse
            Start() 
            done = True
        elif inp == "exit":
            done = True
        elif inp == "imp":
            done = True 
            print("Giving up...")
            taskfile = open("ex1_task%d.txt"%task.taskid, 'w')
            taskfile.write("NONE\nimpossible\n")
            taskfile.close()
            Clear()
            Start()
        elif inp == "retry":
            task.retry()
        elif inp in choices:
            try:
                choices[inp]()
            except:
                print("Can't do that")
                sleep(1)
            if task.check():
                print("SUCCESS - saving")
                task.save()
                done = True
                sleep(1)
                Start()
        # clear screen
        Clear() 

def main():
    print("Welcome to CSCA48's Exercise 1 aide program")
    print("This program will aide you by automatically sorting the")
    print("letters based on your commands (no need for pencil/paper")
    print("This program can also write all the moves you did to a text file")
    print("First, select the task number in the exercise (1 - 9):")
    Start()


if __name__ == "__main__":
    main()

