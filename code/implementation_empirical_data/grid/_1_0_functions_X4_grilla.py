#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:19:45 2019

@author: alvaro
"""
import random as rd
import numpy as np
from scipy import stats
import pickle

dir = ""


def cal_pop_fitness(chromosome):
    """
    chromosome is a vector with 8 values:

    alpha -> POL parameter
    beta  -> Co parameter
    gamma ->P parameter
    kappa -> RV(s) parameter
    eta   -> Sec(s) parameter
    t     -> increasing rate over Sec
    lambda
    scenario   -> 1 allocation of cars randomly according to blocks distribution
                  2 allocation of cars correlated to SE according to blocks distribution
                  3 allocation of cars randomly according to dwellings distribution
                  4 allocation of cars correlated to SE according to dwellings distribution
    spread_nb -> Tau parameter, weight inside RV


    """
    if chromosome[7] == 1:
        with open(dir + "_0_1_rd_mz_grid.txt", "r") as file:
            grid_info = eval(file.readline())

        target = sum([i[5] for i in grid_info])

        list_grid = {}
        for i in range(0, len(grid_info)):
            list_grid[grid_info[i][0]] = {"CAI": grid_info[i][2],
                                          "commerce": grid_info[i][3],
                                          "parking": grid_info[i][4],
                                          "target": grid_info[i][5],
                                          "nb": grid_info[i][6],
                                          "pt": grid_info[i][7],
                                          "sg": grid_info[i][8]}
        with open(dir + "_0_1_rd_mz_cars.txt", "r") as file:
            car_info = eval(file.readline())
        list_car = car_info.copy()
    elif chromosome[7] == 2:
        with open(dir + "_0_2_mz_gain_grid.txt", "r") as file:
            grid_info = eval(file.readline())

        target = sum([i[5] for i in grid_info])

        list_grid = {}
        for i in range(0, len(grid_info)):
            list_grid[grid_info[i][0]] = {"CAI": grid_info[i][2],
                                          "commerce": grid_info[i][3],
                                          "parking": grid_info[i][4],
                                          "target": grid_info[i][5],
                                          "nb": grid_info[i][6],
                                          "pt": grid_info[i][7],
                                          "sg": grid_info[i][8]}
        with open(dir + "_0_2_mz_gain_cars.txt", "r") as file:
            car_info = eval(file.readline())
        list_car = car_info.copy()
    elif chromosome[7] == 3:
        with open(dir + "_0_3_dw_rd_grid.txt", "r") as file:
            grid_info = eval(file.readline())

        target = sum([i[5] for i in grid_info])

        list_grid = {}
        for i in range(0, len(grid_info)):
            list_grid[grid_info[i][0]] = {"CAI": grid_info[i][2],
                                          "commerce": grid_info[i][3],
                                          "parking": grid_info[i][4],
                                          "target": grid_info[i][5],
                                          "nb": grid_info[i][6],
                                          "pt": grid_info[i][7],
                                          "sg": grid_info[i][8]}
        with open(dir + "_0_3_dw_rd_cars.txt", "r") as file:
            car_info = eval(file.readline())
        list_car = car_info.copy()
    elif chromosome[7] == 4:
        with open(dir + "_0_4_dw_gain_grid.txt", "r") as file:
            grid_info = eval(file.readline())

        target = sum([i[5] for i in grid_info])

        list_grid = {}
        for i in range(0, len(grid_info)):
            list_grid[grid_info[i][0]] = {"CAI": grid_info[i][2],
                                          "commerce": grid_info[i][3],
                                          "parking": grid_info[i][4],
                                          "target": grid_info[i][5],
                                          "nb": grid_info[i][6],
                                          "pt": grid_info[i][7],
                                          "sg": grid_info[i][8]}
        with open(dir + "_0_4_dw_gain_cars.txt", "r") as file:
            car_info = eval(file.readline())
        list_car = car_info.copy()
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

    """
    selecting some cars to calculate probability
    """
    car_stolen = {}

    while target2 < target:
        sample_cars = rd.sample(list_car.keys(), 1)[0]
        grid_trial = list_car[sample_cars]["id_grid"]
        trials += 1
        max_thefts = max([list_grid[i]["pt"] for i in list_grid])
        if max_thefts == 0:
            max_t = 1
        else:
            max_t = max_thefts
        pt_own = list_grid[grid_trial]["pt"] / max_t
        pt_nb = 0
        for nb in list_grid[grid_trial]["nb"]:
            pt_nb += list_grid[nb]["pt"] / (max_t * len(list_grid[grid_trial]["nb"]))
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

    cor_per = stats.pearsonr([list_grid[i]["target"] for i in list_grid], [list_grid[i]["pt"] for i in list_grid])[0]
    cor_spe = stats.spearmanr([list_grid[i]["target"] for i in list_grid], [list_grid[i]["pt"] for i in list_grid])[0]

    return [chromosome, car_stolen, list_grid, cor_per, cor_spe, trials]
