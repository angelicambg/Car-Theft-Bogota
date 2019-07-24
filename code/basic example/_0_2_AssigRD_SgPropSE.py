#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:08:48 2019
asignacion de carros aleatorioa y Sg inicializado con el SE
@author: Angelica
"""

import random as rd
from scipy import stats
import numpy as np
import csv

# import info neighborhoods
with open('D:/tesis/Model_neighbors/lexicografico_menos/X4_SE_ini.csv', newline='') as f:  # generacion por mz
    reader = csv.reader(f, delimiter=';')
    grid_info = list(reader)

grid_info = [[int(i),    # 0_i: Id nb (SCaCodigo)
              int(j)*2,    # 1_j: N_cars (n_cars)
              int(k),    # 2_k: CAI
              float(l),  # 3_l: comer_mas_lin
              float(m),  # 4_m: parking_lin
              int(n),    # 5_n:t_autos_red2
              o,         # 6_o: nb_of_nb
              0,         # 7_0: robos pasados (incializacion en cero)
              float(p)   # 8_p: SE incializacion en cero o con el estrato
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
np.histogram(gain, bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])


# making the spots according to the number of blocks
spots_nb = []
for id_nb in range(0, len(grid_info)):
    for rep in range(0, grid_info[id_nb][1]):
        spots_nb.append(grid_info[id_nb][0])


# shuffle the nb to paste to the list of cars

rd.seed(50)
spots_nb_id = rd.sample(spots_nb, len(spots_nb))

car_info = {}

for id_car in range(0, N_cars):
    car_info[id_car+1] = {"gain": gain[id_car], "id_grid": spots_nb_id[id_car]}

with open("D:/tesis/Model_neighbors/lexicografico_menos/lexico_rd_grid_2.txt", "w") as file:
    file.write(str(grid_info))

with open("D:/tesis/Model_neighbors/lexicografico_menos/lexico_rd_cars_2.txt", "w") as file:
    file.write(str(car_info))


