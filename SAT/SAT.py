import sys
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

    def ratio_satisfied(self):
        ''' calculate ratio of satisfied clauses'''
        count = self.nc
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
                count -= 1
        # if no clause is False then value is True
        return count/self.nc

    def random_instance(self, nv, nc):
        self.nv = nv
        self.variables = list(range(1,nv+1))
        self.variable_assignment = [False]*nv
        self.nc = nc
        # generate nc clauses: (... or ... or ...)
        self.clauses = []
        for c in range(nc):
            x1 = choice([-1,1])*randint(1,nv)
            x2 = choice([-1,1])*randint(1,nv)
            x3 = choice([-1,1])*randint(1,nv)
            self.clauses.append( (x1,x2,x3) )

    def random_yes_instance(self, nv, nc):
        # start by randomly choosing a satisfying configuration, then build formula
        self.nv = nv
        self.variables = list(range(1,nv+1))
        self.variable_assignment = [choice([True,False]) for nv in range(self.nv)]
        # choose satisfying clauses
        self.nc = nc
        self.clauses = []

        def clause_value(c): # helper function
            x1 = self.variable_assignment[ abs(c[0])-1 ]
            x2 = self.variable_assignment[ abs(c[1])-1 ]
            x3 = self.variable_assignment[ abs(c[2])-1 ]
            # if negative then negate boolean value of the variable
            if c[0]<0: x1 = not x1
            if c[1]<0: x2 = not x2
            if c[2]<0: x3 = not x3
            return (x1 or x2 or x3)

        for nc in range(self.nc):
            c = sample(self.variables,3)
            c[0] *= choice([-1,1])
            c[1] *= choice([-1,1])
            c[2] *= choice([-1,1])
            while clause_value(c) == False: # alter c until it becomes satisfying
                c[ choice([0,1,2]) ] *= -1  # by flipping terminals (negating)
            self.clauses.append(c)

    def try_at_random(self):
        pass

    def exhaustive_search(self):
        # iterate over all the possible Boolean variable assignments
        for self.variable_assignment in product([True,False],repeat=self.nv):
            if self.value() == True:
                return True
        return False

    def greedy(self):
        '''
        Find the variable that appears most often and assign it accordingly to maximize ...
        '''
        variables_occurance = [[i,0] for i in range(-self.nv,self.nv+1)]
        for c in self.clauses:
            for v in c:
                variables_occurance[ v+self.nv ][1] += 1
        variables_occurance.sort( key=lambda a:a[1] )
        for v in variables_occurance:
            self.variable_assignment[ abs(v[0])-1 ] = (v[0]>0)
        return self.ratio_satisfied()



instance = SAT()

with open("times_greedy.csv","w") as times:
    # test greedy search
    max_repeats = 1000
    rho = 10  # ratio: nc/nv
    for nv in range(10,400,10):
        nc = rho*nv
        q  = 0        # to measure 'quality' of solution
        for repeat in range(max_repeats):
            instance.random_yes_instance(nv, nc)
            q += instance.greedy()
        print      ( str(nv)+"\t"+str(q/max_repeats) )
        times.write( str(nv)+"\t"+str(q/max_repeats)+"\n" )
        times.flush()

sys.exit()

with open("times_exhaustive.csv","w") as times:
    # test exhaustive search
    max_repeats = 100
    for n in range(10,50):
        t0 = time()
        for repeats in range(max_repeats): # e.g. average over 100 instances
            instance.random_instance(n,n)
            decision = instance.exhaustive_search()
        t1 = time()

        # record average time
        print      ( str(n)+"\t"+str((t1-t0)/max_repeats) )
        times.write( str(n)+"\t"+str((t1-t0)/max_repeats)+"\n" )

        if t1-t0 > 60: # if it takes too long then stop testing
            break
