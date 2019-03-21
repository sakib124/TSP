import random
import matplotlib.pyplot as plt
import math
import numpy as np


class City:
    def __init__(self, x=None, y=None):
        self.x = None
        self.y = None
        if x is not None:
            self.x = x
        else:
            self.x = int(random.random() * 200)
        if y is not None:
            self.y = y
        else:
            self.y = int(random.random() * 200)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distance(self, city):
        xDis = abs(self.getX() - city.getX())
        yDis = abs(self.getY() - city.getY())
        distance = math.sqrt((xDis * xDis) + (yDis * yDis))
        return distance

    def __repr__(self):
        return str(self.getX()) + ", " + str(self.getY())


class RouteManager:
    destCities = []

    def addCity(self, city):
        self.destCities.append(city)

    def getCity(self, index):
        return self.destCities[index]

    def numCities(self):
        return len(self.destCities)


class Route:
    def __init__(self, routemanager, route=None):
        self.routemanager = routemanager
        self.route = []
        self.fitness = 0.0
        self.distance = 0
        if route is not None:
            self.route = route
        else:
            for i in range(0, self.routemanager.numCities()):
                self.route.append(None)

    def __len__(self):
        return len(self.route)

    def __getitem__(self, index):
        return self.route[index]

    def __setitem__(self, key, value):
        self.route[key] = value

    def __repr__(self):
        bracketPoints = "["
        for i in range(0, self.routeSize()):
            bracketPoints += str(self.getCity(i)) + "],["
        return bracketPoints

    def generateIndividual(self):
        for cityIndex in range(0, self.routemanager.numCities()):
            self.setCity(cityIndex, self.routemanager.getCity(cityIndex))
        random.shuffle(self.route)

    def getCity(self, routePositon):
        return self.route[routePositon]

    def setCity(self, routePositon, city):
        self.route[routePositon] = city
        self.fitness = 0.0
        self.distance = 0

    def getFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.getDistance())
        return self.fitness

    def getDistance(self):
        if self.distance == 0:
            routeDist = 0
            for cityIndex in range(0, self.routeSize()):
                fromCity = self.getCity(cityIndex)
                destCity = None
                if cityIndex + 1 < self.routeSize():
                    destCity = self.getCity(cityIndex + 1)
                else:
                    destCity = self.getCity(0)
                routeDist += fromCity.distance(destCity)
            self.distance = routeDist
        return self.distance

    def routeSize(self):
        return len(self.route)

    def containsCity(self, city):
        return city in self.route


class Population:
    def __init__(self, routemanager, popSize, initialise):
        self.routes = []
        for i in range(0, popSize):
            self.routes.append(None)

        if initialise:
            for i in range(0, popSize):
                newRoute = Route(routemanager)
                newRoute.generateIndividual()
                self.saveRoute(i, newRoute)

    def __setitem__(self, key, value):
        self.routes[key] = value

    def __getitem__(self, index):
        return self.routes[index]

    def saveRoute(self, index, route):
        self.routes[index] = route

    def getRoute(self, index):
        return self.routes[index]

    def getFittest(self):
        fittest = self.routes[0]
        for i in range(0, self.popSize()):
            if fittest.getFitness() <= self.getRoute(i).getFitness():
                fittest = self.getRoute(i)
        return fittest

    def popSize(self):
        return len(self.routes)


class GeneticAlgorithm:
    def __init__(self, routemanager):
        self.routemanager = routemanager
        self.mutationRate = 0.015
        self.tournamentSize = 5
        self.elitism = True

    def evolvePopulation(self, pop):
        newPop = Population(self.routemanager, pop.popSize(), False)
        elitismOffset = 0
        if self.elitism:
            newPop.saveRoute(0, pop.getFittest())
            elitismOffset = 1

        for i in range(elitismOffset, newPop.popSize()):
            parent1 = self.tournamentSelection(pop)
            parent2 = self.tournamentSelection(pop)
            child = self.crossover(parent1, parent2)
            newPop.saveRoute(i, child)

        for i in range(elitismOffset, newPop.popSize()):
            self.mutate(newPop.getRoute(i))

        return newPop

    def crossover(self, parent1, parent2):
        child = Route(self.routemanager)

        startPosition = int(random.random() * parent1.routeSize())
        endPosition = int(random.random() * parent1.routeSize())

        for i in range(0, child.routeSize()):
            if startPosition < endPosition and i > startPosition and i < endPosition:
                child.setCity(i, parent1.getCity(i))
            elif startPosition > endPosition:
                if not (i < startPosition and i > endPosition):
                    child.setCity(i, parent1.getCity(i))

        for i in range(0, parent2.routeSize()):
            if not child.containsCity(parent2.getCity(i)):
                for ii in range(0, child.routeSize()):
                    if child.getCity(ii) == None:
                        child.setCity(ii, parent2.getCity(i))
                        break

        return child

    def mutate(self, route):
        for routePosition1 in range(0, route.routeSize()):
            if random.random() < self.mutationRate:
                routePosition2 = int(route.routeSize() * random.random())

                city1 = route.getCity(routePosition1)
                city2 = route.getCity(routePosition2)

                route.setCity(routePosition2, city1)
                route.setCity(routePosition1, city2)

    def tournamentSelection(self, pop):
        tournament = Population(self.routemanager, self.tournamentSize, False)
        for i in range(0, self.tournamentSize):
            randomId = int(random.random() * pop.popSize())
            tournament.saveRoute(i, pop.getRoute(randomId))
        fittest = tournament.getFittest()
        return fittest


if __name__ == '__main__':

    routemanager = RouteManager()

    # create and add cities to specified coordinates
    city = City(60, 200)
    routemanager.addCity(city)
    city2 = City(180, 200)
    routemanager.addCity(city2)
    city3 = City(80, 180)
    routemanager.addCity(city3)
    city4 = City(140, 180)
    routemanager.addCity(city4)
    city5 = City(20, 160)
    routemanager.addCity(city5)
    city6 = City(100, 160)
    routemanager.addCity(city6)
    city7 = City(200, 160)
    routemanager.addCity(city7)
    city8 = City(140, 140)
    routemanager.addCity(city8)
    city9 = City(40, 120)
    routemanager.addCity(city9)
    city10 = City(100, 120)
    routemanager.addCity(city10)
    city11 = City(180, 100)
    routemanager.addCity(city11)
    city12 = City(60, 80)
    routemanager.addCity(city12)
    city13 = City(120, 80)
    routemanager.addCity(city13)
    city14 = City(180, 60)
    routemanager.addCity(city14)
    city15 = City(20, 40)
    routemanager.addCity(city15)
    city16 = City(100, 40)
    routemanager.addCity(city16)
    city17 = City(200, 40)
    routemanager.addCity(city17)
    city18 = City(20, 20)
    routemanager.addCity(city18)
    city19 = City(60, 20)
    routemanager.addCity(city19)
    city20 = City(160, 20)
    routemanager.addCity(city20)

    # initialize population
    pop = Population(routemanager, 50, True);
    print "Initial distance: " + str(pop.getFittest().getDistance())

    # evolve population for 100 generations
    ga = GeneticAlgorithm(routemanager)
    pop = ga.evolvePopulation(pop)
    for i in range(0, 100):
        pop = ga.evolvePopulation(pop)

    # Print final distance and solution of best order of cities to reach
    print "Final distance: " + str(pop.getFittest().getDistance())
    print ""
    print "Solution:"
    s = str(pop.getFittest())
    print s[:-2]

    # create and plot graph from solution array that was printed
    data = np.array([
        eval(s[:-2])
    ])
    x, y = data.T
    plt.scatter(x, y)
    plt.plot(x, y)
    plt.show()

