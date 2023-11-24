from node import Node
from queue import Queue, PriorityQueue
from rushHourPuzzle import RushHourPuzzle

class Search:

    @staticmethod
    def breadthFirst(initial_state):
        
        initial_node = Node(initial_state)   
        # Check if the start element is the goal
        if initial_node.state.isGoal():
            return initial_node, 0

        # Create the OPEN FIFO queue and the CLOSED list
        open = Queue() # A FIFO queue
        open.put(initial_node)
        closed = list()
       
        step = 0
        while True:
            print (f'*** Step {step} ***')
            # Check if the OPEN queue is empty => goal not found 
            if open.empty():
                return None, step            
            # Get the first element of the OPEN queue
            current = open.get()            
            # Put the current node in the CLOSED list
            closed.append(current)
            step +=1 
            # Generate the successors of the current node
            for (action, successor) in current.state.successorFunction():                
                child = Node(successor, current, action)
                # Check if the child is not in the OPEN queue and the CLOSED list
                if (child.state.board not in [node.state.board for node in closed] and \
                    child.state.board not in [node.state.board for node in list(open.queue)]):
                    # Check if the child is the goal
                    if child.state.isGoal():
                        print ("Goal reached")
                        return child, step 
                    # Put the child in the OPEN queue 
                    open.put(child)     


    # # Informed search : A star algorithm

    @staticmethod
    def AStar(initial_state, h):
        open = PriorityQueue()
        closed = list()
        initial_node = Node(initial_state) 
        initial_node.setF(h)
        if initial_node.state.isGoal():
            return initial_node, 0
        
        open.put((initial_node.f, initial_node))
        step = 0
        while (True):
            print (f'*** Step {step} ***')
            _, current = open.get()
            if current.state.isGoal():
                return current, step
            closed.append(current)
            step+=1
            print(current.f)

            for(action, successor) in current.state.successorFunction():
                child = Node(successor, current, action)
                child.setF(h)

                # Check if the child state is already in the closed list
                in_closed = any(node.state.board == child.state.board for node in closed)
                if in_closed and child.f >= current.f:
                    continue

                # Check if the child state is already in the open priority queue
                in_open = any(node[1].state.board == child.state.board for node in open.queue)
                if not in_open or child.f < current.f:
                    open.put((child.f, child))

        return None, step

def main():

    initial_state = RushHourPuzzle('1.csv')
    RushHourPuzzle.printRushHourBoard(initial_state.board)   
    # goal_node, step = Search.breadthFirst(initial_state)
    goal_node, step = Search.AStar(initial_state, 3)
    print(f"Path cost: {goal_node.f}")
    print(f"Number of steps: {step}")
    print("Moves: {}".format(" ".join(map(str, goal_node.getSolution()))))

if __name__ == "__main__":
    main()
