from SearchAlgoPlayground import config,UI



from SearchAlgoPlayground import PlayGround
from SearchAlgoUtlis import *
from SearchAlgoPlayground.config import CYAN,YELLOW,PURPLE


"""
Using config file to change configuration of playground
Using rgb color value (r,g,b)
"""
#changing background color
config["BACKGROUND_COLOR"] = (135, 139, 145)

config["NODE_COLOR"] = (201, 205, 212) #changing node color

config["GRID_COLOR"] = (201, 205, 212) #changing grid color
config["NODE_BORDER_COLOR"] = (55, 63, 64) #changing node border color, this will also change the edge color



PG:PlayGround = PlayGround()


def dfs():
    ALGORITHM_TITLE = "Depth First Search Algorithm"
    PG.setTitle(ALGORITHM_TITLE) #set title of the window
    S = PG.getStartNode() #start node from playground
    G = PG.getGoalNode() #goal node from playground
    #in dfs OPEN is a stack
    OPEN = [(S,None)] #Starting with S and it's parent as None
    CLOSED = [] #Closed contains node that are already visited

    #Till we have node to inspect keep looking
    while OPEN:
        nodePair = OPEN[0] #pop the first pair
        (N,_) = nodePair
        #Display info text
        print("Picking Node: {}".format(N.get_label())) #display node label
        PG.showInfoText("Picking Node: {}".format(N.get_label()))
        #check if node N is goal node or not
        if N==G:
            pathNodes = ReconstructPath(nodePair,CLOSED) #construct the path
            highlightPath(pathNodes) #Once the path is found we highlight the path

            #display some info texts
            print("Path Constructed")
            PG.showInfoText("Path Constructed")
            return
        else:
            N.set_color(CYAN)
            PG.delay(100) #Delay the speed about 100 milliseconds
            CLOSED = [nodePair] + CLOSED #add node to closed
            neighbours = PG.MoveGen(N) #get all the neighbours of N
            newNodes = RemoveSeen(neighbours,OPEN,CLOSED) #remove already visited nodes from neighbours
            for node in newNodes:
                node.set_color(YELLOW)
                PG.delay(200)
            newPairs = MakePairs(newNodes,N)
            OPEN = newPairs + OPEN[1:] #Add on top i.e. it follows stack data structure
            PG.delay(10) #delay 
    #display some info texts
    print("No path found between Start and Goal Nodes")
    PG.showInfoText("No path found between Start and Goal Nodes")
    return []


def highlightPath(pathNodes):
    #highlight the nodes in the path and highlight the edge between them as well
    #We traverse the list in reverse as ReconstructPath() will generate the path from goal to start node
    for i in range(len(pathNodes)-1,0,-1):
        """
        Select nodes in pair of two and highlight them including the edge between the pair
        """
        nodeS = pathNodes[i] #starting node of edge
        nodeE = pathNodes[i-1] #ending node of the edge
        edge = PG.get_edge(nodeS,nodeE) #get the edge from playground between the two node
        nodeS.set_color(PURPLE) #set the color of the node
        edge.set_color(PURPLE)#set the color of the node
        PG.delay(100) #slow down the program as well as frames that means slowing down the animation
    pathNodes[0].set_color(PURPLE) #set the color of the last node

PG.onStart(dfs) #set onstart method
PG.run()