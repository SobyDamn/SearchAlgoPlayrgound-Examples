from SearchAlgoPlayground import PlayGround
from SearchAlgoUtlis import *

PATH_NODE_COLOR = (242, 163, 124) #Color for node in path
HIGHLIGHT_COLOR = (145, 190, 230) #color to highlight node
PG:PlayGround = PlayGround.fromfilename("Graph1.json")
PG.setTitle("A* Algorithm")
"""
node_values dictionary will contain node label as key and their g values and h values
g value - actual cost from start not
h value - heuristic cost
structure of each element is
{nodeLabel:{
    g_value:Value,
    h_value:Value
}}
"""
node_values = {} #All nodes with Node class object label as key

#Parent dictionary, contains child node label as key and it's parent as value
parent_dict = {}

def h(N):
    """
    Returns heuristic distance from goal node
    """
    if N.get_label() in node_values:
        return node_values[N.get_label()]["h_value"]
    else:
        return float('inf') #If the node is not in world return large value

def g(N):
    """
    Return actual cost from start node
    """
    return node_values[N.get_label()]["g_value"]

def sort(OPEN:list):
    """
    Returns node with lowest f value
    f_value = g_value+h_value
    """
    OPEN.sort() #Sort first by alphabetical order
    return sorted(OPEN,key = lambda node: node_values[node.get_label()]["h_value"] + node_values[node.get_label()]["g_value"]) #sort by f value

def manhattan_dist(N,G):
    """
    Returns manhattan distance between two nodes
    """
    #Node class attribute id returns the location of the node in 2D grid
    (x1,y1) = N.id
    (x2,y2) = G.id
    return abs(x2-x1)*10 + abs(y2-y1)*10 #return manhattan distance, each block is 10 unit

def A_star():
    S = PG.getStartNode() #start node from the playground
    G = PG.getGoalNode() #goal node from the playground
    #initialising g_values as infinite for all the nodes, calculate h_value of the node as well
    OPEN = [S] #OPEN list with starting node
    parent_dict[S.get_label()] = None #Parent of start node as None
    CLOSED = []
    nodes = PG.getAllNodes()
    for node in nodes:
        #Storing nodes with their label as key and corresponding g_value and h_value
        node_values[node.get_label()] = {}
        node_values[node.get_label()]["h_value"] = manhattan_dist(node,G)
        node_values[node.get_label()]["g_value"] = float('inf') #g_value as infinite
    #Set start node g_value as 0, as it will be picked first
    node_values[S.get_label()]["g_value"] = 0

    def PropagateMovement(M):
        """
        Method to change the path if a better node is found
        """
        for X in PG.MoveGen(M):
            k = PG.get_edge(M,X).get_weight()
            if g(M)+k<g(X):
                parent_dict[X.get_label()] = M
                node_values[X.get_label()]["g_value"] = g(M) + k
                if X in CLOSED:
                    PropagateMovement(X)

    while len(OPEN)!=0:
        #Sort the OPEN list according to their f values
        OPEN = sort(OPEN)
        #Take first node with the least f value
        N = OPEN[0]
        CLOSED.append(N) #Add N to closed

        PG.showInfoText("Picking {} with g({}) = {},h({}) = {}".format(N.get_label(),N.get_label(),g(N),N.get_label(),h(N)))
        print("Picking {} with g({}) = {},h({}) = {}".format(N.get_label(),N.get_label(),g(N),N.get_label(),h(N)))
        OPEN = OPEN[1:] #Pop first element
        N.set_color(HIGHLIGHT_COLOR) #Set color of the picked node
        #Delaying program helps to add visuals to the playground frames
        PG.delay(600) ##Delays the program so everything doesn't happen in single frame
        if N==G:
            #Path found
            print("Path Cost :",g(N))
            PG.showInfoText("Path Cost : {}".format(g(N)))
            ReconstructPath(N) #Reconstruct the path
            return
        else:
            for M in PG.MoveGen(N):
                k = PG.get_edge(N,M).get_weight()
                if g(N) + k <g(M):
                    #Update parent
                    parent_dict[M.get_label()] = N
                    node_values[M.get_label()]["g_value"] = g(N) + k
                    #node_values[M.get_label()]["f_value"] = g(M) + h(M)
                    if M in OPEN:
                        continue
                    if M in CLOSED:
                        PropagateMovement(M)
                    else:
                        OPEN = OPEN + [M]
    PG.showInfoText("No Path Found!")
    print("No Path Found!")
    return

    
def ReconstructPath(G):
    """
    Creates path from parent_dict
    """
    path = [G] #First node
    #Doing backtracking to start node
    #Start node will have parent value as None
    while G is not None:
        G = parent_dict[G.get_label()]
        if G is not None:
            path.append(G)
    #Traverse the path array in reverse and highlight the edges and nodes
    for i in range(len(path)-1,0,-1):
        nodeS = path[i]
        nodeE = path[i-1]
        edge = PG.get_edge(nodeS,nodeE) #get edge between the node
        nodeS.set_color(PATH_NODE_COLOR) #set color for node
        edge.set_color(PATH_NODE_COLOR) #set color for edge
        PG.delay(500)
    PG.delay(500)
    path[0].set_color(PATH_NODE_COLOR) #set color for last node
    

PG.onStart(A_star) #Set function when start button is clicked

#NOTE: Running playground draws the frames
PG.run() #Run the playground