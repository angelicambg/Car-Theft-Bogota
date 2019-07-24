
import random as rd
import datetime
import multiprocessing as mp
import _1_0_functions_X4
import os
import sys

if __name__ == '__main__':

    "Directory"
    dir = "D:/tesis/Model_neighbors/X4_ABM/"
    folder1 = dir+"_0_pob_ini"
    folder2 = dir+"_1_cross"
    folder3 = dir+"_2_mt"
    folder4 = dir+"_3_generation"

    # define the name of the directory to be created
    try:
        os.mkdir(folder1)
    except OSError:
        print ("Creation of the directory %s failed" % folder1)
    else:
        print ("Successfully created the directory %s " % folder1)

    try:
        os.mkdir(folder2)
    except OSError:
        print ("Creation of the directory %s failed" % folder2)
    else:
        print ("Successfully created the directory %s " % folder2)

    try:
        os.mkdir(folder3)
    except OSError:
        print("Creation of the directory %s failed" % folder3)
    else:
        print("Successfully created the directory %s " % folder3)

    try:
        os.mkdir(folder4)
    except OSError:
        print("Creation of the directory %s failed" % folder4)
    else:
        print("Successfully created the directory %s " % folder4)

    print(datetime.datetime.now())
    """
    1: mz random,
    2: se_mz y gain correlated
    3: predios random
    4: se_predios y gain correlated
    """
    #ini_cond = 3
    if len(sys.argv) > 2:
        print("Wrong number of parameters", str(sys.argv))
    elif len(sys.argv) == 1:
        print("not argument define")
    else:
        try:
            # sys.argv[0] is the script name
            ini_cond = int(sys.argv[1])
            print("Cond arg set to: " + str(ini_cond))
        except:
            print("Wrong value")
    """
    sol_per_pop:        initial population for the genetic algorithm
    num_generations:    number of generations for execution
    n_for_t:            number of population for tournament
    size_cross          number of population for crossover
    ss_mutate           number of population for mutation
    var                 variance applied for mutation
    cores               number of cores for parallelization

    """
    sol_per_pop = 2000
    num_generations = 50
    n_for_t = 3
    size_cross = 128
    ss_mutate = 128
    var = 0.002
    new_population = []
    cores = int(36)

    for i in range(0, sol_per_pop):
            new_population.append([rd.random(),         # CAI
                                   rd.random(),         # commer
                                   rd.random(),         # parking
                                   rd.random(),         # robos pasados
                                   rd.random(),         # incremento en seguridad
                                   rd.uniform(.1, 1),   # tasa de incremento en seguridad
                                   rd.uniform(.3, 1),   # lambda
                                   ini_cond,            # condicion incial para saber cual tomar
                                   rd.random()])        # parametro para spread de vecinos

    pool_ip = mp.Pool(cores)
    results = (pool_ip.map_async(_1_0_functions_X4.cal_pop_fitness, [chrom for chrom in new_population],
                                 error_callback=print)).get()
    pool_ip.close()
    pool_ip.join()

    p_parameters = []
    p_cars_st = []
    p_nb = []
    p_fitness1 = []
    p_fitness2 = []
    p_trials = []

    for i in range(0, sol_per_pop):
        p_parameters.append(results[i][0])
        p_nb.append(results[i][2])
        p_fitness1.append(results[i][3])
        p_fitness2.append(results[i][4])
        p_trials.append(results[i][5])

    theft_nb = {}
    for t_nb in range(0, len(p_nb)):
        theft_nb_gen = {}
        for t_nb_g in p_nb[t_nb]:
            theft_nb_gen[t_nb_g] = p_nb[t_nb][t_nb_g]["pt"]
        theft_nb[t_nb] = theft_nb_gen

    outF = open(dir+"_0_pob_ini/_"+str(ini_cond)+"_parameters.txt", "w")
    outF.writelines(str(p_parameters))
    outF.close()

    outF = open(dir+"_0_pob_ini/_"+str(ini_cond)+"_p_nb.txt", "w")
    outF.writelines(str(theft_nb))
    outF.close()

    outF = open(dir+"_0_pob_ini/_"+str(ini_cond)+"_p_fitness1.txt", "w")
    outF.writelines(str(p_fitness1))
    outF.close()

    outF = open(dir+"_0_pob_ini/_"+str(ini_cond)+"_p_fitness2.txt", "w")
    outF.writelines(str(p_fitness2))
    outF.close()

    outF = open(dir+"_0_pob_ini/_"+str(ini_cond)+"_p_trials.txt", "w")
    outF.writelines(str(p_trials))
    outF.close()

    print(datetime.datetime.now())

    print("End-fitness initial population")

    ###########################################################
    ###########################################################
    #generaciones
    ###########################################################
    ###########################################################
    for i in range(0, num_generations):
        if i == 0:
            [pop_tour, fitness_tour] = _1_0_functions_X4.tournament(p_parameters, n_for_t, sol_per_pop, p_fitness1)
        else:
            [pop_tour, fitness_tour] = _1_0_functions_X4.tournament(pop_tour, n_for_t, sol_per_pop, fitness_tour)

        cross_parameters = []
        cross_cars_st = []
        cross_nb = []
        cross_fitness1 = []
        cross_fitness2 = []
        cross_trials = []
        result_cross = []
        for j in range(0, size_cross):
            result_cross.append(_1_0_functions_X4.crossover2(pop_tour, fitness_tour))

        pool_cross = mp.Pool(cores)
        results_cross = (pool_cross.map_async(_1_0_functions_X4.cal_pop_fitness, [cross for cross in result_cross],
                                              error_callback=print)).get()
        pool_cross.close()
        pool_cross.join()

        for k in range(0, size_cross):
            cross_parameters.append(results_cross[k][0])
            cross_nb.append(results_cross[k][2])
            cross_fitness1.append(results_cross[k][3])
            cross_fitness2.append(results_cross[k][4])
            cross_trials.append(results_cross[k][5])

        theft_nb_cross = {}
        for t_nb in range(0, len(cross_nb)):
            theft_nb_cross_gen = {}
            for t_nb_g in cross_nb[t_nb]:
                theft_nb_cross_gen[t_nb_g] = cross_nb[t_nb][t_nb_g]["pt"]
            theft_nb_cross[t_nb] = theft_nb_cross_gen

        outF = open(dir + "_1_cross/_" + str(ini_cond) + "_cross"+str(i)+"_parameters.txt", "w")
        outF.writelines(str(cross_parameters))
        outF.close()

        outF = open(dir + "_1_cross/_" + str(ini_cond) + "_cross"+str(i)+"_nb.txt", "w")
        outF.writelines(str(theft_nb_cross))
        outF.close()

        outF = open(dir + "_1_cross/_" + str(ini_cond) + "_cross"+str(i)+"_fitness1.txt", "w")
        outF.writelines(str(cross_fitness1))
        outF.close()

        outF = open(dir + "_1_cross/_" + str(ini_cond) + "_cross"+str(i)+"_fitness2.txt", "w")
        outF.writelines(str(cross_fitness2))
        outF.close()

        outF = open(dir + "_1_cross/_" + str(ini_cond) + "_cross"+str(i)+"_trials.txt", "w")
        outF.writelines(str(cross_trials))
        outF.close()

        mt_parameters = []
        mt_cars_st = []
        mt_nb = []
        mt_fitness1 = []
        mt_fitness2 = []
        mt_trials = []

        result_mt = _1_0_functions_X4.mutate2(pop_tour, fitness_tour, ss_mutate, var)

        pool_mt = mp.Pool(cores)
        results_mt = (pool_mt.map_async(_1_0_functions_X4.cal_pop_fitness, [mut for mut in result_mt],
                                        error_callback=print)).get()
        pool_mt.close()
        pool_mt.join()

        for k in range(0, ss_mutate):
            mt_parameters.append(results_mt[k][0])
            mt_nb.append(results_mt[k][2])
            mt_fitness1.append(results_mt[k][3])
            mt_fitness2.append(results_mt[k][4])
            mt_trials.append(results_mt[k][5])

        theft_nb_mt = {}
        for t_nb in range(0, len(mt_nb)):
            theft_nb_mt_gen = {}
            for t_nb_g in mt_nb[t_nb]:
                theft_nb_mt_gen[t_nb_g] = mt_nb[t_nb][t_nb_g]["pt"]
            theft_nb_mt[t_nb] = theft_nb_mt_gen

        outF = open(dir + "_2_mt/_" + str(ini_cond) + "_mt"+str(i)+"_parameters.txt", "w")
        outF.writelines(str(mt_parameters))
        outF.close()

        outF = open(dir + "_2_mt/_" + str(ini_cond) + "_mt"+str(i)+"_nb.txt", "w")
        outF.writelines(str(theft_nb_mt))
        outF.close()

        outF = open(dir + "_2_mt/_" + str(ini_cond) + "_mt"+str(i)+"_fitness1.txt", "w")
        outF.writelines(str(mt_fitness1))
        outF.close()

        outF = open(dir + "_2_mt/_" + str(ini_cond) + "_mt"+str(i)+"_fitness2.txt", "w")
        outF.writelines(str(mt_fitness2))
        outF.close()

        outF = open(dir + "_2_mt/_" + str(ini_cond) + "_mt"+str(i)+"_trials.txt", "w")
        outF.writelines(str(mt_trials))
        outF.close()

        # adding the crossover result
        pop_tour += cross_parameters
        fitness_tour += cross_fitness1

        # adding the mutation result
        pop_tour += mt_parameters
        fitness_tour += mt_fitness1

        outF = open(dir + "_3_generation/_" + str(ini_cond) + "_fitness_gen_"+str(i)+".txt", "w")
        outF.writelines(str(fitness_tour))
        outF.close()
        outF = open(dir + "_3_generation/_" + str(ini_cond) + "_parameters_gen_"+str(i)+".txt", "w")
        outF.writelines(str(pop_tour))
        outF.close()
        print(i)
        print(datetime.datetime.now())
