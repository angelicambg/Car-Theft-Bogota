import _1_0_functions_lexico
import plotly
import numpy as np
import plotly.figure_factory as ff
import random as rd

directory = "D:/tesis/Model_neighbors/lexicografico_menos/"

def delta_graf(grid, salida):
    z = [[grid[i] for i in grid][x:x + 6] for x in range(0, len([grid[i] for i in grid]), 6)]
    z_text = np.around(z, decimals=2)
    x = ['A', 'B', 'C', 'D', 'E', 'F']
    y = ['I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
    colorscale = [[0.0, 'rgb(0, 0, 51)'], [.2, 'rgb(0, 0, 102)'],
                  [.4, 'rgb(0, 102, 204)'], [.6, 'rgb(51, 153, 255)'],
                  [.8, 'rgb(153, 204, 255)'], [1.0, 'rgb(255,255,255)']]
    fig = ff.create_annotated_heatmap(z, zmin=0, zmax=1, x=x, y=y, xgap=3, ygap=3, annotation_text=z_text,
                                      colorscale=colorscale, reversescale=True,
                                      font_colors=['#3c3636', '#efecee'])
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 11
    fig.layout.xaxis.showgrid = False
    fig.layout.yaxis.showgrid = False
    fig.layout.xaxis.zeroline = False
    fig.layout.yaxis.zeroline = False
    return plotly.offline.plot(fig, filename=salida)


def count_graf(grid, salida):
    newlist = [grid[i] for i in grid]
    newlist2 = []
    for i in range(0, len(newlist)):
        if newlist[i] == 0:
            newlist2.append(0.0)
        elif newlist[i] > 0 and newlist[i] <= 3:
            newlist2.append(0.2)
        elif newlist[i] > 3 and newlist[i] <= 6:
            newlist2.append(0.4)
        elif newlist[i] > 6 and newlist[i] <= 9:
            newlist2.append(0.6)
        elif newlist[i] > 9 and newlist[i] <= 12:
            newlist2.append(0.8)
        elif newlist[i] > 12:
            newlist2.append(1.0)

    z = [newlist2[x:x + 6] for x in range(0, len([grid[i] for i in grid]), 6)]
    z1 = [[grid[i] for i in grid][x:x + 6] for x in range(0, len([grid[i] for i in grid]), 6)]
    z_text = np.around(z1, decimals=2)
    x = ['A', 'B', 'C', 'D', 'E', 'F']
    y = ['I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']

    colorscale = [[0.0, 'rgb(0, 0, 51)'], [.2, 'rgb(0, 0, 102)'],
                  [.4, 'rgb(0, 102, 204)'], [.6, 'rgb(51, 153, 255)'],
                  [.8, 'rgb(153, 204, 255)'], [1.0, 'rgb(255,255,255)']]

    fig = ff.create_annotated_heatmap(z, zmin=0, zmax=1, x=x, y=y, xgap=3, ygap=3, annotation_text=z_text,
                                      colorscale=colorscale, reversescale=True,
                                      font_colors=['#3c3636', '#efecee'])
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 11
    fig.layout.xaxis.showgrid = False
    fig.layout.yaxis.showgrid = False
    fig.layout.xaxis.zeroline = False
    fig.layout.yaxis.zeroline = False
    return plotly.offline.plot(fig, filename=salida)



rd.seed(123)
par1, car_stolen_1, list_grid_1, trials_1, list_grid10_1, list_grid100_1, list_grid200_1, trials10_1, trials100_1, \
        trials200_1, delta_0_1, delta10_1, delta100_1, delta200_1, \
        delta_fin_1, list_grid0_1, car_stolen10_1, car_stolen100_1, \
        car_stolen200_1 = _1_0_functions_lexico.cal_pop_fitness([1, 1, 1, 1, 1, 1, 1, 3, 1])

count_graf({i: list_grid10_1[i]["pt"] for i in list_grid10_1}, directory + "robos01_10.html")
count_graf({i: list_grid100_1[i]["pt"] for i in list_grid100_1}, directory + "robos01_100.html")
count_graf({i: list_grid200_1[i]["pt"] for i in list_grid200_1}, directory + "robos01_200.html")
count_graf({i: list_grid_1[i]["pt"] for i in list_grid_1}, directory + "robos01.html")

delta_graf(delta_0_1, directory + "Grid_01.html")
delta_graf(delta10_1, directory + "Grid_01_10.html")
delta_graf(delta100_1, directory + "Grid_01_100.html")
delta_graf(delta200_1, directory + "Grid_01_200.html")
delta_graf(delta_fin_1, directory + "Grid_01_300.html")

