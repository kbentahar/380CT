import sys
from random import randint, randrange, sample, choice, shuffle
from itertools import chain, combinations, product
from numpy import arange
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

    def set_variable(self,variable, value):
        self.variable_assignment[ abs(variable)-1 ] = value

    def negate_variable_value(self,variable):
        self.variable_assignment[ abs(variable)-1 ] = not self.variable_assignment[ abs(variable)-1 ]

    def get_variable(self,variable):
        return self.variable_assignment[ abs(variable)-1 ]

    def get_variables(self,clause):
        x1 = self.get_variable( clause[0] )
        x2 = self.get_variable( clause[1] )
        x3 = self.get_variable( clause[2] )
        return x1,x2,x3

    def value(self, n=None):
        ''' evaluate the first n clauses of phi '''
        if n==None: n=self.nc # if n is not given then evlaute phi completely
        n_clauses_evaluated = 0
        for c in self.clauses:
            n_clauses_evaluated += 1
            x1,x2,x3 = self.get_variables( c )
            # if negative then negate boolean value of the variable
            if c[0]<0: x1 = not x1
            if c[1]<0: x2 = not x2
            if c[2]<0: x3 = not x3
            # if any clause is False then the value is False
            if (x1 or x2 or x3) == False:
                return False
            if n_clauses_evaluated == n:
                return True
        # if no clause is False then value is True
        return True

    def ratio_unsatisfied(self):
        ''' calculate ratio of satisfied clauses'''
        count = 0
        for c in self.clauses:
            x1,x2,x3 = self.get_variables( c )
            # if negative then negate boolean value of the variable
            if c[0]<0: x1 = not x1
            if c[1]<0: x2 = not x2
            if c[2]<0: x3 = not x3
            if (x1 or x2 or x3) == False:
                count += 1
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
        def clause_value(c): # helper function
            x1,x2,x3 = self.get_variables( c )
            # if negative then negate boolean value of the variable
            if c[0]<0: x1 = not x1
            if c[1]<0: x2 = not x2
            if c[2]<0: x3 = not x3
            return (x1 or x2 or x3)
        # start by randomly choosing a satisfying configuration, then build formula
        self.nv = nv
        self.variables = list(range(1,nv+1))
        self.variable_assignment = [choice([True,False]) for nv in range(self.nv)]
        # choose satisfying clauses
        self.nc = nc
        self.clauses = []

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

    def dynamic(self):
        ''' TODO '''
        possible_assignments = []
        for c in self.clauses:
            # only time 'x or y or z = False' is when x=y=z=False
            for tf in product([True,False],repeat=3):
                pass
        
    def greedy(self):
        '''
        Find the variable that appears most often and assign it accordingly to maximize ...
        '''
        literals_occurance = [[i,0] for i in range(-self.nv,self.nv+1)]
        for c in self.clauses:
            for v in c:
                literals_occurance[ v+self.nv ][1] += 1
        literals_occurance.sort( key=lambda a:a[1] )
        for v in literals_occurance:
            self.set_variable( v[0] , v[0]>0 )
        return self.ratio_unsatisfied()

    def greedy_randomized(self, block_size=2):
        '''
        Find the variable that appears most often and assign it accordingly to maximize ...
        Same as greedy() but randomizes the order of 'literals_occurance' a bit
        '''
        literals_occurance = [[i,0] for i in range(-self.nv,self.nv+1)]
        for c in self.clauses:
            for v in c:
                literals_occurance[ v+self.nv ][1] += 1
        literals_occurance.sort( key=lambda a:a[1] )
        for i in range(0,len(literals_occurance), block_size): # randomize list block by block
            tmp = literals_occurance[i:i+block_size]
            shuffle( tmp )
            literals_occurance[i:i+block_size] = tmp
        for v in literals_occurance:
            self.set_variable( v[0] , v[0]>0 )
        return self.ratio_unsatisfied()

    def GRASP(self):
        ''' GRASP meta-heuristic '''
        best = 1 # i.e. start with the worst solution that satisfies no clauses
        for i in range(100):
            candidate = self.greedy_randomized( choice([2,3,4]) ) # random block_size from {2,3,4}
            # local search: flip variable assignment and see if things improve
            for v in self.variables:
                self.negate_variable_value(v)          # try changing variable v
                if self.ratio_unsatisfied() > candidate: # undo if worse
                    self.negate_variable_value(v)
            if candidate < best:
                best = candidate
        return best


instance = SAT()

def time_GRASP():
    with open("times_grasp.csv","w") as times:
        # test greedy search
        max_repeats = 200
        nv = 20
        for rho in arange(0.5,7,0.1):  # rho = nc/nv
            nc = int(rho*nv)
            q  = 0        # to measure 'quality' of solution of greedy
            #qr = 0        # to measure 'quality' of solution of greedy_randomized
            qg = 0        # to measure 'quality' of solution of GRASP
            for repeat in range(max_repeats):
                instance.random_yes_instance(nv, nc)
                q  += instance.greedy()
                #qr += instance.greedy_randomized(3)
                qg += instance.GRASP()
            print      ( str(rho)+"\t"+str(q/max_repeats)+"\t"+str(qg/max_repeats) )
            times.write( str(rho)+"\t"+str(q/max_repeats)+"\t"+str(qg/max_repeats) )
            times.flush()

def time_Greedy():
    with open("times_greedy.csv","w") as times:
        # test greedy search
        max_repeats = 1000
        nv = 20
        for rho in arange(0.5,7,0.1):  # rho = nc/nv
            nc = int(rho*nv)
            q  = 0        # to measure 'quality' of solution
            for repeat in range(max_repeats):
                instance.random_yes_instance(nv, nc)
                q += instance.greedy()
            print      ( str(rho)+"\t"+str(q/max_repeats) )
            times.write( str(rho)+"\t"+str(q/max_repeats)+"\n" )
            times.flush()

def time_Exhaustive():
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

            #if t1-t0 > 60: # if it takes too long then stop testing
            #    break

time_Exhaustive()
#time_Greedy()
#time_GRASP()
