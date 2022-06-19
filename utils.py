from networkx import DiGraph
import utils
#given a graph, we can ask about it questions
#enter graph through txt file
graph = DiGraph()
f = open("graph.txt", "r")

flag_edge = 0
flag_node = 0
#read the graph from txt file and create the graph
for i in f.readlines():
    if "edges:" in i:
        flag_edge = 1
        flag_node = 0
        continue
    if "nodes:" in i:
        flag_edge = 0
        flag_node = 1
        continue

    if flag_edge == 1:
        str_tmp = i.split(',')
        graph.add_edge(int(str_tmp[0]),int(str_tmp[1]))
    
    if flag_node == 1:
        str_tmp = i.split(',')
        for j in str_tmp:
            graph.add_node(int(j))

init = [1,2]

utils.writeSmv(graph, init)
utils.runSmv()
