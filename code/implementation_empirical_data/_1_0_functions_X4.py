import random as rd
import numpy as np
from scipy import stats

dir = "D:/tesis/Model_neighbors/X4_ABM/"


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
    alpha = chromosome[0]
    beta = chromosome[1]
    gamma = chromosome[2]
    kappa = chromosome[3]
    eta = chromosome[4]
    t = chromosome[5]
    p_lambda = chromosome[6]
    spread_nb = chromosome[8]
    target2 = 0
    trials = 0

    """
    selecting cars to calculate probability
    """
    car_stolen = {}
    # car_try = {}
    while target2 < target:
        sample_cars = rd.sample(list_car.keys(), 1)[0]
        "id of the cell where there will be an attempt of crime"
        grid_trial = list_car[sample_cars]["id_grid"]
        trials += 1
        "past thefts in the cell"
        max_thefts = max([list_grid[i]["pt"] for i in list_grid])
        if max_thefts == 0:
            max_t = 1
        else:
            max_t = max_thefts
        pt_own = list_grid[grid_trial]["pt"] / max_t
        pt_nb = 0
        for nb in list_grid[grid_trial]["nb"]:
            pt_nb += list_grid[nb]["pt"] / (max_t * len(list_grid[grid_trial]["nb"]))
        "delta -> difficulty"
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


def tournament(population, n_tourn, sol_per_pop, fitness_res):
    pop_tournament = []
    fitness_tournament = []
    for i in range(0, (sol_per_pop-1)):
        muestra = rd.sample(fitness_res, k=n_tourn)
        max_fitness_idx_tourn = np.where(fitness_res == max(muestra))[0][0]
        fitness_tournament.append(max(muestra))
        pop_tournament.append(population[max_fitness_idx_tourn])
    max_all_idx_tourn = np.where(fitness_res == max(fitness_res))[0][0]
    fitness_tournament.append(max(fitness_res))
    pop_tournament.append(population[max_all_idx_tourn]) 
    return pop_tournament, fitness_tournament


def crossover(muestra):
    cutpoint = rd.sample([0, 1, 2, 3], k=1)
    idx_genes = rd.sample([0, 1, 2, 3, 4], k=5)
    if cutpoint == 0:
        cross = np.array([[muestra[0][idx_genes[0]], idx_genes[0]],
                        [muestra[0][idx_genes[1]], idx_genes[1]],
                        [muestra[1][idx_genes[2]], idx_genes[2]],
                        [muestra[1][idx_genes[3]], idx_genes[3]],
                        [muestra[1][idx_genes[4]], idx_genes[4]],
                        [muestra[0][5], 5],
                        [muestra[0][6], 6],
                        [muestra[0][7], 7],
                        [muestra[0][8], 8]])
    elif cutpoint == 1:
        cross = np.array([[muestra[0][idx_genes[0]], idx_genes[0]],
                          [muestra[0][idx_genes[1]], idx_genes[1]],
                          [muestra[0][idx_genes[2]], idx_genes[2]],
                          [muestra[1][idx_genes[3]], idx_genes[3]],
                          [muestra[1][idx_genes[4]], idx_genes[4]],
                          [muestra[0][5], 5],
                          [muestra[0][6], 6],
                          [muestra[0][7], 7],
                          [muestra[0][8], 8]])
    elif cutpoint == 2:
        cross = np.array([[muestra[0][idx_genes[0]], idx_genes[0]],
                          [muestra[0][idx_genes[1]], idx_genes[1]],
                          [muestra[0][idx_genes[2]], idx_genes[2]],
                          [muestra[0][idx_genes[3]], idx_genes[3]],
                          [muestra[1][idx_genes[4]], idx_genes[4]],
                          [muestra[1][5], 5],
                          [muestra[1][6], 6],
                          [muestra[1][7], 7],
                          [muestra[1][8], 8]])
    else:
        cross = np.array([[muestra[0][idx_genes[0]], idx_genes[0]],
                          [muestra[1][idx_genes[1]], idx_genes[1]],
                          [muestra[1][idx_genes[2]], idx_genes[2]],
                          [muestra[1][idx_genes[3]], idx_genes[3]],
                          [muestra[1][idx_genes[4]], idx_genes[4]],
                          [muestra[1][5], 5],
                          [muestra[1][6], 6],
                          [muestra[1][7], 7],
                          [muestra[1][8], 8]])
    cross = sorted(cross, key=lambda x: x[1])
    offspring = np.transpose(cross)[0]
    return offspring.tolist()


def crossover2(population, fitness):
    # selecting 2 from tournament
    sample_cr_idx = rd.sample(range(0, len(population)), k=2)
    sample_cr = []
    for i in [0, 1]:
        sample_cr.append(population[sample_cr_idx[i]])                

    result_crom = crossover(sample_cr)
    # selecting one of the parents
    sample_pop = rd.sample([0, 1], k=1)
    # removing the parent selected
    population.pop(sample_cr_idx[sample_pop[0]])
    fitness.pop(sample_cr_idx[sample_pop[0]])
    return result_crom


def mutate(muestra, var):
    for i in range(0, len(muestra)):
        idx_mutate = rd.sample([0, 1, 2, 3, 4], k=1)[0]
        muestra[i][idx_mutate] += np.random.normal(0, var)
        if muestra[i][idx_mutate] < 0:
            muestra[i][idx_mutate] = 0
        if rd.random() >= 0.5:
            muestra[i][5] += np.random.normal(0, var)
            if muestra[i][5] < 0.05:
                muestra[i][5] = 0.05
            if muestra[i][5] > 1:
                muestra[i][5] = 1
        if rd.random() >= 0.5:
            muestra[i][8] += np.random.normal(0, var)
            if muestra[i][8] < 0:
                muestra[i][8] = 0
            if muestra[i][8] > 1:
                muestra[i][8] = 1
        if rd.random() >= 0.5:
            muestra[i][6] += np.random.normal(0, var)
            if muestra[i][6] < 0.3:
                muestra[i][6] = 0.3
            if muestra[i][6] > 1:
                muestra[i][6] = 1
    return muestra 


def mutate2(population, fitness, ss_mutate, var):
    #selecting population for mutation
    sample_mt_idx = rd.sample(range(0, len(population)), k=ss_mutate)
    sample_mt = []
    for i in range(0, len(sample_mt_idx)):
        sample_mt.append(population[sample_mt_idx[i]])

    result_mt = mutate(sample_mt, var)
    # removing one parent
    for index in sorted(sample_mt_idx, reverse=True):
        del population[index]
        del fitness[index]
    return result_mt
