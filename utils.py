import os
from pickle import FALSE
from collections import defaultdict
import subprocess

edgeDict = defaultdict(list)

def graphList(graph):
    for edge in graph.edges():
        edgeDict[edge[0]].append(edge[1])

def writeStart(filename, graph, init):
    #if os.path.exists(filename):
        #os.remove(filename)  #create new file

    #write beginning of smv file
    with open(filename, 'w') as fw:
        fw.write("MODULE main\n\nVAR\n	nodes : ")
        lw = '{'
        for i in graph.nodes():
            lw = lw + 'q' + str(i) + ', '
        lw = lw[:-2]
        fw.write(lw)
        fw.write("};\n")
        fw.write("\n\nASSIGN")
        fw.write("			\n\n	init(nodes) := q" + str(init) + ";\n")

        fw.write("    next(nodes) := case\n")
        lw = ""
        for key in edgeDict.keys():
            lw = lw + ("        nodes = q"+str(key)+" : {")
            for node in edgeDict[key]:
                lw = lw + "q" + str(node) + ","
            lw = lw[:-1]
            fw.write(lw)
            fw.write("};\n")
            lw = ""
        fw.write("        TRUE : nodes;\n\n")
        fw.write("        esac;\n\n")
        fw.write("LTLSPEC")
        fw.write("        (G F(nodes = q4))")


# main function of writing the smv file
def writeSmv(graph, init):
    graphList(graph)
    filename_main = 'demo.smv'
    if os.path.exists(filename_main):
        os.remove(filename_main)
    with open(filename_main, 'w') as fw:
        writeStart(filename_main, graph, init)
        with open(filename_main, 'r') as fr:
            for line in fr:
                fw.write(line)


# run smv file and check the result
def runSmv():
    smv_file = f'demo.smv'
    output = subprocess.check_output(['nuXmv', smv_file], shell=True).splitlines()
    ans = False if 'false' in str(output) else True
    print(ans)
    moveList=list()
   
    if not ans:
        loop_vecs = str(b''.join(output))
        chunks = loop_vecs.split(' ')
        FLAG=False
        for i in range(len(chunks)) :
            if chunks[i] == 'Counterexample':
                FLAG=True
            if chunks[i]== 'nodes' and FLAG:
                moveList.append(chunks[i+2])
        print(moveList)