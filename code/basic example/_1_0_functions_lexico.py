#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:19:45 2019

@author: alvaro
"""
import random as rd
import numpy as np
import copy
from scipy import stats

dir = "D:/tesis/Model_neighbors/lexicografico_menos/"


def cal_pop_fitness(chromosome):
    # 1 mz random,
    # 2 se_mz y gain correlated
    # 3 predios random
    # 4 se_predios y gain correlated
    if chromosome[7] == 1:
        with open(dir + "lexico_rd_grid.txt", "r") as file:
            grid_info = eval(file.readline())
        list_grid = {}
        for i in range(0, len(grid_info)):
            list_grid[grid_info[i][0]] = {"CAI": grid_info[i][2],
                                          "commerce": grid_info[i][3],
                                          "parking": grid_info[i][4],
                                          "target": grid_info[i][5],
                                          "nb": grid_info[i][6],
                                          "pt": grid_info[i][7],
                                          "sg": grid_info[i][8]}
        with open(dir + "lexico_rd_cars.txt", "r") as file:
            car_info = eval(file.readline())
        list_car = car_info.copy()
    elif chromosome[7] == 2:
        with open(dir + "lexico_rd_grid_2.txt", "r") as file:
            grid_info = eval(file.readline())

        list_grid = {}
        for i in range(0, len(grid_info)):
            list_grid[grid_info[i][0]] = {"CAI": grid_info[i][2],
                                          "commerce": grid_info[i][3],
                                          "parking": grid_info[i][4],
                                          "target": grid_info[i][5],
                                          "nb": grid_info[i][6],
                                          "pt": grid_info[i][7],
                                          "sg": grid_info[i][8]}
        with open(dir + "lexico_rd_cars_2.txt", "r") as file:
            car_info = eval(file.readline())
        list_car = car_info.copy()
    elif chromosome[7] == 3:
        with open(dir + "lexico_rd_grid_3.txt", "r") as file:
            grid_info = eval(file.readline())

        list_grid = {}
        for i in range(0, len(grid_info)):
            list_grid[grid_info[i][0]] = {"CAI": grid_info[i][2],
                                          "commerce": grid_info[i][3],
                                          "parking": grid_info[i][4],
                                          "target": grid_info[i][5],
                                          "nb": grid_info[i][6],
                                          "pt": grid_info[i][7],
                                          "sg": grid_info[i][8]}
        with open(dir + "lexico_rd_cars_3.txt", "r") as file:
            car_info = eval(file.readline())
        list_car = car_info.copy()
    elif chromosome[7] == 4:
        with open(dir + "lexico_rd_grid_4.txt", "r") as file:
            grid_info = eval(file.readline())

        list_grid = {}
        for i in range(0, len(grid_info)):
            list_grid[grid_info[i][0]] = {"CAI": grid_info[i][2],
                                          "commerce": grid_info[i][3],
                                          "parking": grid_info[i][4],
                                          "target": grid_info[i][5],
                                          "nb": grid_info[i][6],
                                          "pt": grid_info[i][7],
                                          "sg": grid_info[i][8]}
        with open(dir + "lexico_rd_cars_4.txt", "r") as file:
            car_info = eval(file.readline())
        list_car = car_info.copy()
        # Calculating the fitness value of each solution in the current population.
        # The fitness function calculates the correlation for the ABM
    """
    Global parameters
    """
    alpha = chromosome[0]       # CAI parameter
    beta = chromosome[1]        # commer parameter
    gamma = chromosome[2]       # parking parameter
    kappa = chromosome[3]       # efectividad en robos parameter
    eta = chromosome[4]         # sg survelillance parameter incializada con SE
    t = chromosome[5]           # saltos en que se va incremento surveillance parameter
    p_lambda = chromosome[6]    # decaimitento probabilidad parameter
    spread_nb = chromosome[8]   # Peso de como se riega el spread
    target2 = 0
    trials = 0
    trials10 = 0
    trials100 = 0
    trials200 = 0

    """
    selecting some cars to calculate probability
    """
    car_stolen = {}
    list_grid0 = copy.deepcopy(list_grid)
    list_grid10 = {}
    list_grid100 = {}
    list_grid200 = {}
    car_stolen_10 = {}
    car_stolen_100 = {}
    car_stolen_200 = {}
    # car_try = {}
    delta_0 = delta_func(list_grid, chromosome)
    while target2 < 300:
        sample_cars = rd.sample(list_car.keys(), 1)[0]
        "id de la grilla sobre la cual se va a intentar el robo"
        grid_trial = list_car[sample_cars]["id_grid"]
        trials += 1
        "calculando el valor de la variable de robos pasados usando el contador de pt"
        max_thefts = max([list_grid[i]["pt"] for i in list_grid])
        if max_thefts == 0:
            max_t = 1
        else:
            max_t = max_thefts
        pt_own = list_grid[grid_trial]["pt"] / max_t
        pt_nb = 0
        for nb in list_grid[grid_trial]["nb"]:
            pt_nb += list_grid[nb]["pt"] / (max_t * len(list_grid[grid_trial]["nb"]))
        "calculando delta dados los robos pasados"
        if (alpha + beta + gamma + kappa + eta) > 0:
            delta = ((alpha * list_grid[grid_trial]["CAI"]) +
                     (beta * (1 - list_grid[grid_trial]["commerce"])) +
                     (gamma * list_grid[grid_trial]["parking"]) +
                     (kappa * (1 - ((spread_nb * pt_own) + ((1-spread_nb) * pt_nb)))) +
                     (eta * list_grid[grid_trial]["sg"])
                     ) / (alpha + beta + gamma + kappa + eta)
        else:
            delta = 0
        probability = (1 + np.exp(-(list_car[sample_cars]["gain"] - delta) / p_lambda)) ** (-1)
        theft = rd.random() < probability
        if theft:
            target2 += 1
            car_stolen[sample_cars] = list_car.pop(sample_cars)
            list_grid[grid_trial]["pt"] += 1
            list_grid[grid_trial]["sg"] += t
            if list_grid[grid_trial]["sg"] > 1:
                list_grid[grid_trial]["sg"] = 1
        if target2 == 10:
            list_grid10 = copy.deepcopy(list_grid)
            trials10 = trials
            delta10 = delta_func(list_grid, chromosome)
            car_stolen_10 = copy.deepcopy(car_stolen)
        if target2 == 100:
            list_grid100 = copy.deepcopy(list_grid)
            trials100 = trials
            delta100 = delta_func(list_grid, chromosome)
            car_stolen_100 = copy.deepcopy(car_stolen)
        if target2 == 200:
            list_grid200 = copy.deepcopy(list_grid)
            trials200 = trials
            delta200 = delta_func(list_grid, chromosome)
            car_stolen_200 = copy.deepcopy(car_stolen)
    # cor_per = stats.pearsonr([list_grid[i]["target"] for i in list_grid], [list_grid[i]["pt"] for i in list_grid])[0]
    # cor_spe = stats.spearmanr([list_grid[i]["target"] for i in list_grid], [list_grid[i]["pt"] for i in list_grid])[0]
    delta_fin = delta_func(list_grid, chromosome)
    return chromosome, car_stolen, list_grid, trials, list_grid10, list_grid100, list_grid200, trials10, trials100, \
        trials200, delta_0, delta10, delta100, delta200, delta_fin, list_grid0, \
        car_stolen_10, car_stolen_100, car_stolen_200


def delta_func(list_grid, chromosome):
    delta_nb = {}
    alpha = chromosome[0]       # CAI parameter
    beta = chromosome[1]        # commer parameter
    gamma = chromosome[2]       # parking parameter
    kappa = chromosome[3]       # efectividad en robos parameter
    eta = chromosome[4]         # sg survelillance parameter incializada con SE
    spread_nb = chromosome[8]   # Peso de como se riega el spread
    max_thefts = max([list_grid[i]["pt"] for i in list_grid])
    if max_thefts == 0:
        max_t = 1
    else:
        max_t = max_thefts
    for l in list_grid:
        pt_own = list_grid[l]["pt"] / max_t
        pt_nb = 0
        for nb in list_grid[l]["nb"]:
            pt_nb += list_grid[nb]["pt"] / (max_t * len(list_grid[l]["nb"]))
        "calculando delta dados los robos pasados"
        delta_nb[l] = ((alpha * list_grid[l]["CAI"]) +
                       (beta * (1 - list_grid[l]["commerce"])) +
                       (gamma * list_grid[l]["parking"]) +
                       (kappa * (1 - ((spread_nb * pt_own) + ((1 - spread_nb) * pt_nb)))) +
                       (eta * list_grid[l]["sg"])
                       ) / (alpha + beta + gamma + kappa + eta)
    return delta_nb
