import unittest

class TestJourneys(unittest.TestCase):
    
    def test1(self):
        newJourney=Journey(['AB5','BC4','CD8','DC8','DE6','AD5','CE2','EB3','AE7'],'ABC')
        self.assertEqual(getDistance(newJourney.followRoute()),9)
        
    def test2(self):
        newJourney=Journey(['AB5','BC4','CD8','DC8','DE6','AD5','CE2','EB3','AE7'],'AD')
        self.assertEqual(getDistance(newJourney.followRoute()),5)
        
    def test3(self):
        newJourney=Journey(['AB5','BC4','CD8','DC8','DE6','AD5','CE2','EB3','AE7'],'ADC')
        self.assertEqual(getDistance(newJourney.followRoute()),13)
        
    def test4(self):
        newJourney=Journey(['AB5','BC4','CD8','DC8','DE6','AD5','CE2','EB3','AE7'],'AEBCD')
        self.assertEqual(getDistance(newJourney.followRoute()),22)
        
    def test5(self):
        newJourney=Journey(['AB5','BC4','CD8','DC8','DE6','AD5','CE2','EB3','AE7'],'AED')
        self.assertEqual(getDistance(newJourney.followRoute()),'NO SUCH ROUTE')
        
    def test6(self):
        newJourney=Journey(['AB5','BC4','CD8','DC8','DE6','AD5','CE2','EB3','AE7'],'CC',0,3)
        self.assertEqual(len(newJourney.filterRoutes(newJourney.getAllRoutes())),2)
        
    def test7(self):
        newJourney=Journey(['AB5','BC4','CD8','DC8','DE6','AD5','CE2','EB3','AE7'],'AC',4,4)
        self.assertEqual(len(newJourney.filterRoutes(newJourney.getAllRoutes())),3)
        
    def test8(self):
        newJourney=Journey(['AB5','BC4','CD8','DC8','DE6','AD5','CE2','EB3','AE7'],'AC')
        self.assertEqual(getShortestRoute(newJourney.getAllRoutes())[1],9)
        
    def test9(self):
        newJourney=Journey(['AB5','BC4','CD8','DC8','DE6','AD5','CE2','EB3','AE7'],'BB')
        self.assertEqual(getShortestRoute(newJourney.getAllRoutes())[1],9)
        
    def test10(self):
        newJourney=Journey(['AB5','BC4','CD8','DC8','DE6','AD5','CE2','EB3','AE7'],'CC',maxDistance=29)
        self.assertEqual(len(newJourney.getAllRoutesMaxDistance()),7)
        
    '''tests if getAllRoutesMaxDistance works if looping before the final
    station is possible'''
    def test_extra(self):
        newJourney=Journey(['AB5','BA4','BC8'],'AC',maxDistance=22)
        self.assertEqual(len(newJourney.getAllRoutesMaxDistance()),2)

class Journey():
    
    def __init__(self, graph, stations, minStops=0, maxStops=0, maxDistance=0):
        self.graph=graph
        self.stations=stations
        self.minStops=minStops
        self.maxStops=maxStops
        self.maxDistance=maxDistance
          
    '''If no maxStops, it checks if all routes in routes go from stations[0] to stations[-1]
    If there is a maxStops, it checks if the maximum is reached
    I assume you can always travel to another station from any station'''
    def checkIfDone(self,routes):
        if self.maxStops==0:
            for route in routes:
                if route[-1][1]!=self.stations[-1]:
                    return False
            return True
        else:
            for route in routes:
                if len(route)==self.maxStops:
                    return True
            return False
    
    '''removes routes that end in the wrong station'''
    def removeInvalidRoutes(self,routes):
        newRoutes=[]
        for route in routes:
            if route[-1][1]==self.stations[-1]:
                newRoutes.append(route)
        return newRoutes

    '''returns all routes in graph that go from stations[0] to stations[-1]
    If maxStops=0, it returns all possibilities wihout using the same road twice.
    If maxStops>0, is does allow re-using roads, and returns all options with this
    maximum'''
    def getAllRoutes(self):
        routes=[]
        for route in self.graph:
            if route[0]==self.stations[0]:
                routes.append([route])
        while not self.checkIfDone(routes):
            newRoutes=[]
            for route1 in routes:
                if route1[-1][1]==self.stations[-1]:
                    newRoutes.append(route1.copy())
                if (self.maxStops>0 and len(route1)<self.maxStops) or route1[-1][1]!=self.stations[-1]:
                    for route2 in self.graph:
                        if route1[-1][1]==route2[0]:
                            roadUsed=False
                            for road in route1:
                                if road==route2:
                                    roadUsed=True
                            if not roadUsed or self.maxStops>0:
                                newRoutes.append(route1.copy())
                                newRoutes[-1].append(route2)
            routes=newRoutes.copy()
        if self.maxStops>0:
            return self.removeInvalidRoutes(routes)
        else:
            return routes
    
    '''returns all routes with a maximum distance.
    Allows re-using roads'''
    def getAllRoutesMaxDistance(self):
        routes=[]
        finishedRoutes=[]
        for route in self.graph:
            if route[0]==self.stations[0]:
                routes.append([route])
        while len(routes)>0:
            newRoutes=[]
            for route1 in routes:
                    for route2 in self.graph:
                        if route1[-1][1]==route2[0]:
                            tempRoute=route1.copy()
                            tempRoute.append(route2)
                            if getDistance(tempRoute)<=self.maxDistance:
                                newRoutes.append(route1.copy())
                                newRoutes[-1].append(route2)
            for newRoute in newRoutes:
                if newRoute[-1][1]==self.stations[-1]:
                    finishedRoutes.append(newRoute)
            routes=newRoutes.copy()
        return finishedRoutes
    
    '''returns the route that follows stations.
    stations is a string of letters that represent the stations, e.g. ABC'''
    def followRoute(self):
        route=[]
        for i in range(len(self.stations)-1):
            for road in self.graph:
                found=False
                if road[:2]==self.stations[i:i+2]:
                    found=True
                    route.append(road)
                    break
            if found==False:
                return 'NO SUCH ROUTE'
        return route
    
    '''filters out routes that have too little or many stops,
    so it returns the routes that have the minimum and
    maximum number of stops
    minStops is the minimum number of stops
    maxStops is the maximimum number of stops'''
    def filterRoutes(self,routes):
        validRoutes=[]
        for route in routes:
            if len(route)<=self.maxStops and len(route)>=self.minStops:
                validRoutes.append(route)
        return validRoutes
    
'''prints the results of the 10 problems'''
def printResults(graph):
    newJourney=Journey(graph,'ABC')
    print(getDistance(newJourney.followRoute()))
    newJourney=Journey(graph,'AD')
    print(getDistance(newJourney.followRoute()))
    newJourney=Journey(graph,'ADC')
    print(getDistance(newJourney.followRoute()))
    newJourney=Journey(graph,'AEBCD')
    print(getDistance(newJourney.followRoute()))
    newJourney=Journey(graph,'AED')
    print(getDistance(newJourney.followRoute()))
    newJourney=Journey(graph,'CC',0,3)
    print(len(newJourney.filterRoutes(newJourney.getAllRoutes())))
    newJourney=Journey(graph,'AC',4,4)
    print(len(newJourney.filterRoutes(newJourney.getAllRoutes())))
    newJourney=Journey(graph,'AC')
    print(getShortestRoute(newJourney.getAllRoutes())[1])
    newJourney=Journey(graph,'BB')
    print(getShortestRoute(newJourney.getAllRoutes())[1])
    newJourney=Journey(graph,'CC',maxDistance=29)
    print(len(newJourney.getAllRoutesMaxDistance()))
    
'''returns the distance of the route.
route is a list of strings of the connected stations and their length, e.g.
['AB5','BC4','CD8']
'''
def getDistance(route):
    if route=='NO SUCH ROUTE':
        return'NO SUCH ROUTE'
    distance=0
    for road in route:
        distance+=int(road[2])
    return distance

'''returns the shortest route
routes is a list of lists of strings, which represent two connected stations
and ther lengths. Example: [['AB5','BC4','CD8'],['AG6','GE1','ED8']]'''
def getShortestRoute(routes):
    shortestDistance=getDistance(routes[0])
    for route in routes:
        distance=getDistance(route)
        if distance<=shortestDistance:
            shortestRoute=route
            shortestDistance=distance
    return shortestRoute, shortestDistance

if __name__ == "__main__":
    graph=['AB5','BC4','CD8','DC8','DE6','AD5','CE2','EB3','AE7']
    printResults(graph)
    unittest.main()