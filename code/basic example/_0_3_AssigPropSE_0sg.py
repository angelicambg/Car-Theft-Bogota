#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:08:48 2019
asignacion de gain de carros por SE y Sg inicializado con cero
@author: Angelica
"""

import random as rd
from scipy import stats
import numpy as np
import csv

# import info neighborhoods
with open('D:/tesis/Model_neighbors/lexicografico_menos/X4_0_ini.csv', newline='') as f:  # generacion por mz
    reader = csv.reader(f, delimiter=';')
    grid_info = list(reader)

grid_info = [[int(i),       # 0_i: Id nb (SCaCodigo)
              int(j)*2,    # 1_j: N_cars (n_cars)
              int(k),       # 2_k: CAI
              float(l),     # 3_l: comer_mas_lin
              float(m),     # 4_m: parking_lin
              int(n),       # 5_n:t_autos_red2
              o,            # 6_o: nb_of_nb
              0,            # 7_0: robos pasados (incializacion en cero)
              float(p)      # 8_p: SE incializacion en cero o con el estrato
              ] for i, j, k, l, m, n, o, p in grid_info]

for i in range(0, len(grid_info)):
    grid_info[i][6] = [int(s) for s in grid_info[i][6].split(',')]


#target
sum([i[5] for i in grid_info])

lower = 0.2
upper = 0.8
mu = 0.5
sigma = 0.09
N_cars = sum([i[1] for i in grid_info])# creating cars according to the number of blocks per nb

gain = stats.truncnorm.rvs(
          (lower-mu)/sigma, (upper-mu)/sigma, loc=mu, scale=sigma, size=N_cars, random_state=10)
#np.histogram(gain, bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])

deci = [33, 67, 100]
deciles = [np.percentile(gain, i) for i in deci]

gain_1 = []
gain_2 = []
gain_3 = []
for i in gain:
    if i <= deciles[0]:
        gain_1.append(i)
    elif i <= deciles[1]:
        gain_2.append(i)
    else:
        gain_3.append(i)

# ordering by SE
from operator import itemgetter
grid_info_order = sorted(grid_info, key=itemgetter(4))

# making the spots according to the number of blocks
spots_nb = []
for id_nb in range(0, len(grid_info_order)):
    for rep in range(0, grid_info_order[id_nb][1]):
        spots_nb.append(grid_info_order[id_nb][0])
len(gain_1)+len(gain_2)+len(gain_3)
spots_nb_1 = spots_nb[:len(gain_1)]#505
spots_nb_2 = spots_nb[len(gain_1):(len(gain_1)+len(gain_2))]#403
spots_nb_3 = spots_nb[(len(gain_1)+len(gain_2)):]#76

rd.seed(20)
spots_nb_id_1 = rd.sample(spots_nb_1, len(spots_nb_1))
rd.seed(20)
spots_nb_id_2 = rd.sample(spots_nb_2, len(spots_nb_2))
rd.seed(30)
spots_nb_id_3 = rd.sample(spots_nb_3, len(spots_nb_3))

gain_paste = gain_1+gain_2+gain_3
spots_nb_paste = spots_nb_id_1 + spots_nb_id_2 + spots_nb_id_3

car_info = {}
for id_car in range(0, N_cars):
    car_info[id_car+1] = {"gain": gain_paste[id_car], "id_grid": spots_nb_paste[id_car]}


with open("D:/tesis/Model_neighbors/lexicografico_menos/lexico_rd_grid_3.txt", "w") as file:
    file.write(str(grid_info))


with open("D:/tesis/Model_neighbors/lexicografico_menos/lexico_rd_cars_3.txt", "w") as file:
    file.write(str(car_info))