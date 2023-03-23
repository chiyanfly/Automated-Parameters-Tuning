import os

import networkx as nx
import sys

import sys

# caution: path[0] is reserved for script path (or '' in REPL)

import GraphCons as G

# cspfile = "../testdata/test.xml"
testfilePath = sys.argv[1]
cen_resultpath = sys.argv[2]
degree_result_path = sys.argv[3]

ori_map_path = sys.argv[4]


def charge_map_csp_ori(ori_map_file):
    dic_csp_ori = {}
    for line in open(ori_map_file):
        csp_var = line.split(";")[2]
        ori_var = line.split(";")[0]
        dic_csp_ori[csp_var] = ori_var

    return dic_csp_ori


if __name__ == "__main__":
    for file in os.listdir(testfilePath):
        print(file)
        csppath = testfilePath + file
        ori_map_file = ori_map_path + file.replace("xml", "csv")
        dic_csp_ori = {}
        if os.path.exists(ori_map_file):
            dic_csp_ori = charge_map_csp_ori(ori_map_file)
        else:
            print("No Ori file")
            continue

        cen_resultfile = open(cen_resultpath + file + "_Varaible_Cons_Graph_cen.csv", "w")
        cen_resultfile.write("Source_Variable/Cons" + ",CSP_Variable/Cons," + "Betweenness centrality" + "\n")
        degree_resultfile = open(degree_result_path + file + "_Varaible_Cons_Graph_degree.csv", "w")
        degree_resultfile.write("Source_Variable/Cons" + ",CSP_Variable/Cons," + "Degree" + "\n")


        My_Graph, dic_id_objet = G.creatVN_CN_Graph(csppath)
        degreelist = list(My_Graph.degree)
        centralitylist = nx.betweenness_centrality(My_Graph)



        sortedlist_cen = sorted(centralitylist.items(), key=lambda item: item[1], reverse=True)
        # sortedlist_degree = sorted(centralitylist.items(), key=lambda item: item[1], reverse=True)

        max = len(sortedlist_cen)
        if max >= 2000:
            max = 2000

        for i in range(0, max):
            (id_den, value_cen) = sortedlist_cen[i]
            csp_var = dic_id_objet.get(id_den)
            if str(csp_var).startswith("v"):
                ori_var = dic_csp_ori.get(csp_var)
                cen_resultfile.write(ori_var + "," + csp_var + "," + str(value_cen) + "\n")
                cen_resultfile.flush()

            (id_degree, value_degree) = degreelist.__getitem__(i)
            csp_var = dic_id_objet.get(id_degree)
            if str(csp_var).startswith("v"):
                ori_var = dic_csp_ori.get(csp_var)
                degree_resultfile.write(ori_var + "," + csp_var + "," + str(value_degree) + "\n")
                degree_resultfile.flush()

        cen_resultfile.flush()
        degree_resultfile.flush()
