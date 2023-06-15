#Carl imports
from explore_param_space import *
from file_process import *
from models import *
from run_simulation import label

#Third-party imports
import numpy as np
import matplotlib.pyplot as mpl
from pathlib import Path
from uuid import uuid4

#Define important paths
cwd = Path(__file__).resolve().parents[1]
data_path = Path(cwd,"data","LHCU_20")
save_path = Path(cwd,"models")

#Define parameter space boundaries
#Same order as OptVars in run_simulation.py
R = [(-20,20),(100,2000),(-20,20),(100,2000),(0,10000)]

#Create an initial sampling of the parameter space (k points, Latin Hypercube method)
k = 4
S = LHCuSample(R,k)

#Label them by running simulations, and keep in a variable the folder in which the results are saved
res_path = label(S)

#Load the results and format them for model training
X_T,Y_T = load_FE(res_path)

#Define model HyperParameters
HP = HyperParameters(layers=[64,64],
                     loss='mae',
                     dropout_rate=0.5,
                     interpolation=1000)

#Build model
model = RecModel(X_T,Y_T,HP)

#train model
model.train(n_epochs=10, verbose=1)

model.save(Path(save_path,"model_RL_base"))

label_fn = lambda X: load_FE(label(X))

for i in range(1):
    model_bis = improve_random(model,label_fn,R,k=4)
    model_bis.save(Path(save_path,f"model_RL_improved_{str(i).zfill(3)}"))
    model = model_bis