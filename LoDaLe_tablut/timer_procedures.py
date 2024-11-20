import time
import numpy as np

class TimerProc:
    def __init__(self, name, descr):
        self.name = name
        self.descr = descr
        self.state = dict()
        self.ongoing = dict()

    def start(self, procedure_name:str):
        if procedure_name in self.ongoing:
            raise Exception(f"{procedure_name} has already an active timer")
        self.ongoing[procedure_name] = time.time()
    
    def end(self, procedure_name:str)->str:
        current_t = time.time()
        if procedure_name not in self.ongoing:
            raise Exception(f"{procedure_name} has not an active timer yet")
        delta = current_t - self.ongoing[procedure_name]
        del self.ongoing[procedure_name]
        if procedure_name not in self.state:
            self.state[procedure_name] = list()
        self.state[procedure_name].append(delta)
        return str(delta)
        
    def __str__(self):
        result = f"{self.name} timer - {self.descr}\nProcedure:\t\tAverage execution time (sec):\n"
        for key in self.state:
            result += key + "\t\t" + str(np.array(self.state[key]).mean()) + "\n"
        return result