# this doc takes a CSP instance as input and generate its constraints graph
from xml.dom import minidom
import re
import sys
import networkx as nx


def chargeVaraible(cspfile):
    mycsp = minidom.parse(cspfile)
    List_var = mycsp.getElementsByTagName('var')
    variablelist = []
    for var in List_var:
        varid = var.attributes['id'].value
        variablelist.append(varid)
    return variablelist


"""
the following is to construct the graph with two kinds of nodes:
    variable node
    constraint node
    vn and vn no connection directly
    vn connnect to cn, if consraint contains this variable
"""


def creatVN_CN_Graph(cspFile):
    variableList = chargeVaraible(cspFile)
    constraintlist = []
    G = nx.Graph()

    mycsp = minidom.parse(cspFile)
    List_extensions = mycsp.getElementsByTagName('extension')
    List_intension = mycsp.getElementsByTagName('intension')
    i = 0
    for exc in List_extensions:
        variables = str(exc.getElementsByTagName('list')[0].firstChild.data).replace("\n", " ").strip()
        variables = ",".join(variables.split())
        constraintlist.append("ex" + str(i) + ":" + variables)
        i = i + 1
    for inte in List_intension:
        constraintlist.append("in" + str(i) + ":" + str(inte.firstChild.data))
        i = i + 1

    nodeid = 1
    dic_id_objet = {}
    dic_objet_id = {}
    for var in variableList:
        G.add_node(nodeid)
        dic_id_objet[nodeid] = var
        dic_objet_id[var] = nodeid
        nodeid = nodeid + 1
    for cons in constraintlist:
        G.add_node(nodeid)
        dic_id_objet[nodeid] = cons
        dic_objet_id[cons] = nodeid
        nodeid = nodeid + 1

    for cons in constraintlist:
        for v in set(re.findall("v\d+", cons)):
            varid = dic_objet_id[v]
            consid = dic_objet_id[cons]
            G.add_edge(varid, consid)
    # print("dealing with "+cspFile,nx.info(G))
    return G,dic_id_objet


"""
try a second graph only containing the variable node, 

vn and vn connects when they are in the same constraint 
"""


def creatVN_Graph(cspFile):
    variableList = chargeVaraible(cspFile)
    constraintlist = []
    G = nx.Graph()

    mycsp = minidom.parse(cspFile)
    List_extensions = mycsp.getElementsByTagName('extension')
    List_intension = mycsp.getElementsByTagName('intension')
    i = 0
    for exc in List_extensions:
        variables = str(exc.getElementsByTagName('list')[0].firstChild.data).replace("\n", " ").strip()
        variables = ",".join(variables.split())
        constraintlist.append("ex" + str(i) + ":" + variables)
        i = i + 1
    for inte in List_intension:
        constraintlist.append("in" + str(i) + ":" + str(inte.firstChild.data))
        i = i + 1

    nodeid = 1
    dic_id_variable = {}
    dic_variable_id = {}
    for var in variableList:
        G.add_node(nodeid)
        dic_id_variable[nodeid] = var
        dic_variable_id[var] = nodeid
        nodeid = nodeid + 1

    for cons in constraintlist:

        vars = list(set(re.findall("v\d+", cons)))

        list_binary = []

        for i in range(0, len(vars) - 1):
            for j in range(i + 1, len(vars)):
                list_binary.append((vars[i], vars[j]))

        for (a,b) in list_binary:
            G.add_edge(dic_variable_id[a],dic_variable_id[b])
    # print(G.edges)
    # print(nx.info(G))
    # print(dic_id_variable)
    return G,dic_id_variable
#
# My_Graph = creatVN_Graph(cspfile)
#
# pos = nx.spring_layout(My_Graph)
# nx.draw(My_Graph, pos, node_size=5, alpha=0.8)
# plt.show()
# comms = community_louvain.best_partition(My_Graph)
#
# for l in  nx.algorithms.community.louvain_partitions(My_Graph):
#     print(l)
#
# unique_coms = np.unique(list(comms.values()))
# print(len(comms.items()))
# cmap = {
#     0: 'maroon',
#     1: 'teal',
#     2: 'black',
#     3: 'orange',
#     4: 'green',
#     5: 'yellow'
# }
#
# node_cmap = [cmap[v] for _, v in comms.items()]
#
# pos = nx.spring_layout(My_Graph)
# nx.draw(My_Graph, pos, node_size=10, node_color=node_cmap)
# plt.show()
