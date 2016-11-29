from random import randint, sample
from itertools import chain, combinations
from time import time

class SAT():
    def __init__(self):
        self.variables = []
        self.clauses   = []
        self.nv        = 0
        self.nc        = 0
        self.variable_assignment = []
        
    def __repr__(self):
        r = "SAT instance with "+str(self.nv)+" variables and "+str(self.nc)+" clauses: \n"
        for c in self.clauses:
            # TODO: negative variables
            r+= "(x"+str(c[0]) + " + x"+str(c[1]) + " + x"+str(c[2]) + ")\n"
        return r

    def value(self):
        r = True
        for c in self.clauses:
            x1 = self.variable_assignment[ c[0] ]
            x2 = self.variable_assignment[ c[1] ]
            x3 = self.variable_assignment[ c[2] ]
            r = r and (x1 or x2 or x3)
        return r

    def random_instance(self, nv, nc):
        self.nv = nv
        self.variable_assignment = [False]*nv
        self.nc = nc
        self.variables = list(range(1,nv+1))
        for c in range(nc):
            # TODO negate some variables
            x1 = randint(1,nv)
            x2 = randint(1,nv)
            x3 = randint(1,nv)
            self.clauses.append( (x1,x2,x3) )

    def random_yes_instance(self, n, bitlength=10):
        pass

    ###

    def try_at_random(self):
        pass
            
    def exhaustive_search(self):
        pass

        
instance = SAT()
instance.random_instance(4,7)
print( instance )

decision = instance.exhaustive_search()
print(decision)

#instance.try_at_random()
