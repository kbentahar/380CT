from random import randint, sample, choice
from itertools import chain, combinations, product
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
            r+= str(c) + "\n"
        return r

    def value(self):
        for c in self.clauses:
            x1 = self.variable_assignment[ abs(c[0])-1 ]
            x2 = self.variable_assignment[ abs(c[1])-1 ]
            x3 = self.variable_assignment[ abs(c[2])-1 ]
            # if negative then negate boolean value of the variable
            if c[0]<0: x1 = not x1
            if c[1]<0: x2 = not x2
            if c[2]<0: x3 = not x3
            # if any clause is False then the value is False
            if (x1 or x2 or x3) == False:
                return False
        # if no clause is False then value is True
        return True

    def random_instance(self, nv, nc):
        self.nv = nv
        self.variable_assignment = [False]*nv
        self.nc = nc
        self.variables = list(range(1,nv+1))
        # generate nc clauses: (... or ... or ...)
        for c in range(nc):
            x1 = choice([-1,1])*randint(1,nv)
            x2 = choice([-1,1])*randint(1,nv)
            x3 = choice([-1,1])*randint(1,nv)
            self.clauses.append( (x1,x2,x3) )

    def random_yes_instance(self, n, bitlength=10):
        pass

    ###

    def try_at_random(self):
        pass
            
    def exhaustive_search(self):
        # iterate over all the possible Boolean variable assignments
        for self.variable_assignment in product([True,False],repeat=self.nv):
            if self.value() == True:
                return True
        return False
        
instance = SAT()

with open("times.csv","w") as times:
    # test exhaustive search
    for n in range(10,50):
        t0 = time()    
        for repeats in range(100): # average 100 instances
            instance.random_instance(n,n)
            decision = instance.exhaustive_search()
        times.write( str(n)+", "+str(time()-t0)+"\n" )
    
