from SearchAlgoPlayground import PlayGround
from SearchAlgoUtlis import *
from SearchAlgoPlayground.config import CYAN,YELLOW,PURPLE
from SearchAlgoPlayground import config,UI
config["BACKGROUND_COLOR"] = PURPLE
PG:PlayGround = PlayGround()
def dfs():
    ALGORITHM_TITLE = "Depth First Search Algorithm"
    PG.setTitle(ALGORITHM_TITLE)
    S = PG.getStartNode()
    G = PG.getGoalNode()
    OPEN = [(S,None)] #Starting with S and it's parent as None
    CLOSED = [] #Empty

    #Till we have node to suspect keep looking
    while OPEN:
        nodePair = OPEN[0]
        (N,_) = nodePair
        if N==G:
            nodes = ReconstructPath(nodePair,CLOSED)
            highlightPath(nodes)
            return
        else:
            N.set_color(CYAN)
            PG.delay(1000)
            CLOSED = [nodePair] + CLOSED
            neighbours = PG.MoveGen(N)
            newNodes = RemoveSeen(neighbours,OPEN,CLOSED)
            for node in newNodes:
                node.set_color(YELLOW)
                PG.delay(200)
            newPairs = MakePairs(newNodes,N)
            OPEN = newPairs + OPEN[1:]
            PG.delay(10)
            N.set_color(YELLOW)
    return []


def highlightPath(nodes):
    for i in range(len(nodes)-1,0,-1):
        nodeS = nodes[i]
        nodeE = nodes[i-1]
        edge = PG.get_edge(nodeS,nodeE)
        nodeS.set_color(PURPLE)
        edge.set_color(PURPLE)
        PG.delay(1000)
    nodes[0].set_color(PURPLE)

PG.onStart(dfs)
PG.run()