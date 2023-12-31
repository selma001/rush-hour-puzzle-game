class Node:

    def __init__(self, rushHourPuzzle, parent=None, action="", c=1, heuristic=1):
        self.state = rushHourPuzzle
        self.parent = parent
        self.action = action
        self.g = 0 if not self.parent else self.parent.g + c
        self.setF(heuristic)   

    # Choose one of the available heuristics
    def setF(self, heuristic):
        heuristics = {1: self.heuristic1(),
                    2: self.heuristic2(),
                    3: self.heuristic3()}
        self.f = self.g + heuristics[heuristic]

    """ First heuristic: Distance from target vehicle to the exit """
    def heuristic1(self):
        for vehicle in self.state.vehicles:
            if vehicle["id"] == 'X':
                return self.state.board_width-2-vehicle["x"]
    
    """ Second heuristic: number of vehicles that block the way to the exit """
    def heuristic2(self):
        for vehicle in self.state.vehicles:
            if vehicle["id"] == 'X':
                unique_vehicles = set(self.state.board[vehicle["y"]][vehicle["x"]:])
                if ' ' in unique_vehicles:
                    return self.heuristic1()+len(unique_vehicles)-2
                return self.heuristic1()+len(unique_vehicles)-1

    """ Third heuristic: """
    def heuristic3(self):
        blocking_vehicles = set()
        for vehicle in self.state.vehicles:
            if vehicle["id"] == "X":
                for other_vehicle in self.state.vehicles:
                    if (
                        vehicle["id"] != other_vehicle["id"]
                        and vehicle["x"] == other_vehicle["x"]
                    ):
                        if vehicle["y"] < other_vehicle["y"]:
                            blocking_vehicles.add(other_vehicle["id"])
                        else:
                            blocking_vehicles.add(other_vehicle["id"])
                            
        for vehicle in self.state.vehicles:
            if vehicle["id"] == "X":
                for other_vehicle in self.state.vehicles:
                    if (
                        vehicle["id"] != other_vehicle["id"]
                        and vehicle["y"] == other_vehicle["y"]
                    ):
                        if vehicle["x"] < other_vehicle["x"]:
                            blocking_vehicles.add(other_vehicle["id"])
                        else:
                            blocking_vehicles.add(other_vehicle["id"])
        return len(blocking_vehicles) + self.heuristic1()
    
    def getPath(self):
        states = []
        node = self
        while node != None:
            states.append(node.state)
            node = node.parent
        return states[::-1]
    
    def getSolution(self):
        actions = []
        node = self
        while node != None:
            actions.append(node.action)
            node = node.parent
        return actions[::-1]

    def __lt__(self, other):
        # Define the comparison method for sorting based on the f values
        return self.f < other.f
            



