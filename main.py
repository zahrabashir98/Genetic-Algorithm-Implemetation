import numpy as np
class Genetic(object):

    def __init__(self, f, pop_size = 100, n_variables = 1):
        self.f = f
        self.minim = -100
        self.maxim = 100
        self.pop_size = pop_size
        self.n_variables = n_variables
        self.population = self.initializePopulation()
        print(self.population)
        self.evaluatePopulation()
        print(self.evaluatePopulation())

    def initializePopulation(self):
        return [np.random.randint(self.minim, self.maxim, size=(self.n_variables)) 
                           for i in range(self.pop_size)]

    def evaluatePopulation(self):
        return [self.f(i[0]) for i in self.population]

    def nextGen(self):
  
        results = self.evaluatePopulation()
        
        # print(np.argmin(results))
        children = [self.population[np.argmin(np.absolute(results))]]
        # print(children)
        while len(children) < self.pop_size:
            # Tournament selection
            randA, randB = np.random.randint(0, self.pop_size), \
                           np.random.randint(0, self.pop_size)
            if results[randA] < results[randB]: p1 = self.population[randA]
            else: p1 = self.population[randB]

            randA, randB = np.random.randint(0, self.pop_size), \
                           np.random.randint(0, self.pop_size)  
            if results[randA] < results[randB]: p2 = self.population[randA]
            else: p2 = self.population[randB]   

            signs = []
            for i in zip(p1, p2):
                # print(i)
                if i[0] < 0 and i[1] < 0: signs.append(-1)
                elif i[0] >= 0 and i[1] >= 0: signs.append(1)
                else: signs.append(np.random.choice([-1,1]))
            # print(signs)
            # Convert values to binary
            p1 = [format(abs(i), '010b') for i in p1]
            p2 = [format(abs(i), '010b') for i in p2]

            # Recombination
            child = []
            for i, j in zip(p1, p2):
                for k, l in zip(i, j):
                    if k == l: child.append(k)
                    else: child.append(str(np.random.randint(min(k, l), 
                                                             max(k,l))))

            child = ''.join(child)
            g1 = child[0:len(child)//2] 
            g2 = child[len(child)//2:len(child)]
            children.append(np.asarray([signs[0]*int(g1, 2), 
                                        signs[0]*int(g2, 2)]))
        self.population = children

        
    def run(self):
        ix = 0
        while ix < 100:
            ix += 1
            self.nextGen()
        return self.population[0]
    
f = lambda x : 9*(x)**5 - 194*(x)**4 + 1680*(x)**3 - 7227*(x)**2 + 15501* (x) -13257
gen = Genetic(f)
# print(gen.population)
minim = gen.run()
print('Roots found      X =', minim[0])