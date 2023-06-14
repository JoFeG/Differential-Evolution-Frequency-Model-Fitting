import numpy as np
import pandas as pd

from scipy import signal
from scipy.optimize import differential_evolution
from irace import irace

from de_run import objective_function

# COMPLETARRRRRR
def target_runner(experiment, scenario):
    
    #Latter this shoud be a aparameter!
    model = 1
    df = pd.read_csv(scenario["instances"][0])
    Ts = df["time"][1]
    event_time = Ts*(np.sum(df["event"][df["event"]==1].to_numpy())-1)    
    P0 = df["power"][0] / 1000
    event_freq = df["freq"][df["event"]==1].to_numpy()
    bounds = [(0.00001, 1000) for i in range(6)] ## CHECK
    arguments = (model, Ts, P0, event_freq)
    
    maxiter = 1000
    tol = 0.01    
    
    # Esto no es muy elegante, pero irace pasa popsize como float no como entero, no se donde esta el problema
    popsize = int(experiment["configuration"]["popsize"])
    mutation = experiment["configuration"]["mutation"]
    recombination = experiment["configuration"]["recombination"]
    
    ## Differential Evolution Run
    result = differential_evolution(
        objective_function, 
        bounds, 
        args=(arguments,),
        seed = experiment['seed'],
        tol = tol,
        popsize = popsize,      
        mutation = mutation, 
        recombination = recombination
        #**experiment["configuration"]
    )
    
    return dict(cost=result.fun)

## to try dithering in mutation parameter if needed...
parameters_table = '''
popsize       "" i (10, 50)
mutation      "" r (0, 2)
recombination "" r (0, 1)
'''

default_values = '''
popsize mutation recombination
15      0.75     0.7
'''

# OJO CON ESTE PATH ABSOLUTO DESDE LA CARPETA BASE DEL GIT
# ¿Como especificar mas de una? randomizar a mano dentro del target_runner???
instances = ["test/test.csv"]


# See https://mlopez-ibanez.github.io/irace/reference/defaultScenario.html
scenario = dict(
    instances = instances,
    maxExperiments = 500,
    debugLevel = 3,
    digits = 5,
    parallel=4, # It can run in parallel ! 
    logFile = "")

tuner = irace(scenario, parameters_table, target_runner)
tuner.set_initial_from_str(default_values)
best_confs = tuner.run()
# Pandas DataFrame
print(best_confs)