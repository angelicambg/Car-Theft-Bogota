###########
import json
#import pandas
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.figure_factory as ff
#
folder = "D:/tesis/processing/todo/control1000_500GA"

condicion = 3
gen_cross = 42
gen_mt = 42
f = 1
if f == 1:
    corr = "Pearson"
if f == 2:
    corr = "spearman"

f_pob_ini = "/_0_pob_ini_control/_"
f_cross = "/_1_cross_control/_"
f_mt = "/_2_mt_control/_"

parameters_m = json.load(open(folder + f_pob_ini + str(condicion)+"_parameters.txt"))

fitness_m = json.load(open(folder + f_pob_ini+str(condicion)+"_p_fitness"+str(f)+".txt"))


for i in range(0, gen_cross):
    with open(folder + f_cross + str(condicion)+"_cross"+str(i)+"_parameters.txt") as file:
        parameters_cross1 = json.load(file)
    parameters_m += parameters_cross1

for i in range(0, gen_mt):
    with open(folder + f_mt + str(condicion)+"_mt"+str(i)+"_parameters.txt") as file:
        parameters_mt1 = json.load(file)
    parameters_m += parameters_mt1

for i in range(0, gen_cross):
    with open(folder + f_cross + str(condicion)+"_cross"+str(i)+"_fitness"+str(f)+".txt") as file:
        fitness_cross1 = json.load(file)
    fitness_m += fitness_cross1

for i in range(0, gen_mt):
    with open(folder + f_mt + str(condicion)+"_mt"+str(i)+"_fitness"+str(f)+".txt") as file:
        fitness_mt1 = json.load(file)
    fitness_m += fitness_mt1

min_f = min(fitness_m)
max_f = max(fitness_m)


data = [
    go.Parcoords(
        line=dict(color=fitness_m,
                  colorscale='RdBu',
                  showscale=True,
                  reversescale=True,
                  cmin=min_f,
                  cmax=max_f),
        dimensions=list([
            dict(range=[0, 1],
                 # constraintrange=[0, 1],
                 label='alpha-POL', values=[i[0] for i in parameters_m], visible=True),
            dict(range=[0, 1],
                 # constraintrange=[0, 1],
                 label='beta - Co', values=[i[1] for i in parameters_m], visible=True),
            dict(range=[0, 1],
                 # constraintrange=[0, 1],
                 label='gamma-P', values=[i[2] for i in parameters_m], visible=True),
            dict(range=[0, 1],
                 #constraintrange=[0, 1],
                 label='kappa-RV(s)', values=[i[3] for i in parameters_m], visible=True,),
            dict(range=[0, 1],
                 #constraintrange=[0, 1],
                 label='eta-Sec(s)', values=[i[4] for i in parameters_m], visible=True),
            dict(range=[0, 1],
                 #constraintrange=[0.1, 1],
                 label='r~Sec', values=[i[5] for i in parameters_m], visible=True),
            dict(range=[0, 1],
                 #constraintrange=[0.3, 1],
                 label='lambda', values=[i[6] for i in parameters_m], visible=True),
            dict(range=[min_f, max_f],
                 #constraintrange=[min_f, max_f],
                 label='fitness', values=fitness_m, tickformat=".2f", visible=True),
            dict(range=[0,1],
                 #constraintrange=[min_f, max_f],
                 label='tau~RV', values=[i[8] for i in parameters_m], visible=True)
        ])
    )
]

plotly.offline.plot(data, filename=folder+"/"+corr+"_cond_"+str(condicion) +".html")
