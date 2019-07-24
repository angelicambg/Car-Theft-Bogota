###########
import json
#import pandas
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.figure_factory as ff
#
folder = "D:/tesis/processing/todo/grid_control/"

condicion = 1
#gen_cross = 99
#gen_mt = 99
f = 1
if f == 1:
    corr = "Pearson"
if f == 2:
    corr = "spearman"

parameters_m = []
fitness_m = []


for i in range(0, 149):
    with open(folder + "_" + str(condicion)+"_parameters_grid"+str(i)+".txt") as file:
        parameters_chunk = json.load(file)
    parameters_m += parameters_chunk

for i in range(0, 149):
    with open(folder + "_" + str(condicion)+"_p_fitness"+str(f)+"_grid"+str(i)+".txt") as file:
        fitness_chunk = json.load(file)
    fitness_m += fitness_chunk


min_f = min(fitness_m)
max_f = max(fitness_m)


data = [
    go.Parcoords(
        line=dict(color=fitness_m,
                  colorscale='YlGnBu',
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
                 label='kappa - RV(s)', values=[i[3] for i in parameters_m], visible=True,),
            dict(range=[0, 1],
                 #constraintrange=[0, 1],
                 label='eta-Sec(s)', values=[i[4] for i in parameters_m], visible=True),
            dict(range=[0.1, 1],
                 #constraintrange=[0.1, 1],
                 label='r~Sec', values=[i[5] for i in parameters_m], visible=True),
            dict(range=[0.3, 1],
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

plotly.offline.plot(data, filename=folder+"_grid_control.html")
