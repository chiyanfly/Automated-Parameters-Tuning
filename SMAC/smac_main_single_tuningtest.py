import os
import sys
from numpy import generic
from ConfigSpace import ConfigurationSpace
import webtool as wt
from params import Params_c
import centralitytool as ct
import time
import itertools
from smac.facade.smac_ac_facade import SMAC4AC
from smac.facade.smac_bb_facade import SMAC4BB
from smac.scenario.scenario import Scenario


targetfile= sys.argv[1]
targetfile= targetfile+".xml"


centralityFile =""
all_centrality_candidatures, valuelist = ct.dealcentralityresult("")
print(targetfile, "centrality  variable found\n", all_centrality_candidatures, valuelist)
compile_file = ""
timeout = 600000 # 10 mins
queueId = ""
compile_id = ""



def generateobjetPartitionnmentParams():
    if (len(all_centrality_candidatures) != 0):
        params_space = []
        for i  in range(0,len(all_centrality_candidatures)+1):
            for subset in itertools.combinations(all_centrality_candidatures,i):
                for r in itertools.permutations(subset):
                    params_space.append(tuple(r))
        return params_space
    else:
        return []

def generateConfigurationSpace():
    # unity (M)
    Surfacemin=1
    
    Surfacemax=300
    
    list_surface_values = []
    list_objet_partition = generateobjetPartitionnmentParams()
    print(generateobjetPartitionnmentParams())
    print(len(list_objet_partition))
    for i in range(SurfaceMinValue, SurfaceMaxValue):
        list_surface_values.append(i * 1000000)
    list_surface_values.append(100000)
    list_surface_values.append(200000)
    list_surface_values.append(300000)
    list_surface_values.append(400000)
    list_surface_values.append(500000)
    list_surface_values.append(600000)
    list_surface_values.append(700000)
    list_surface_values.append(800000)
    list_surface_values.append(900000)

    cs = ConfigurationSpace({
        "surface": list_surface_values,
        
        "objetsPartitionnement": list_objet_partition
    })
    return cs

def call_obj(config,seed=0):
    surface= config["surface"]
 
    objetsPartitionnement = config["objetsPartitionnement"]
    print("RUN AGAIN SMAC", compile_file, "\n", surface,
          objetsPartitionnement)



if __name__ == "__main__":
    # run a first attmp with default params and get the Queueid the compileID

    # # Define your hyperparameters
    configspace = generateConfigurationSpace()
    # Provide meta data for the optimization
    scenario = Scenario({
        "run_obj": "quality",  # Optimize quality (alternatively runtime)
        "runcount-limit": 60,  # Max number of function evaluations (the more the better)
        "cs": configspace,
    })
    smac = SMAC4BB(scenario=scenario, tae_runner=call_obj)
    print(smac.optimize())

