
import random as rd
import datetime
import multiprocessing as mp
import _1_0_functions_X4_grilla
import os
import sys

if __name__ == '__main__':

    "Directory"
    dir = ""
    folder1 = dir+"grid"

    # define the name of the directory to be created
    try:
        os.mkdir(folder1)
    except OSError:
        print ("Creation of the directory %s failed" % folder1)
    else:
        print ("Successfully created the directory %s " % folder1)

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
    ' # cantidad de poblacion inicial'

    cores = int(36)
    jump = [0.1, 0.3, 0.5, 0.7, 0.9]
    t_jump = [0.1, 0.5, 0.9]
    lamb_jump = [0.3, 0.5]
    spread_jump = [0.1, 0.5, 0.9, 1]

    abm_grid = [[i,         # 0_i: Id nb (SCaCodigo)
                 j,         # 1_j: N_cars (n_cars)
                 k,         # 2_k: CAI
                 l,         # 3_l: comer_mas_lin
                 m,         # 4_m: parking_lin
                 n,         # 5_n: real thefts by nb
                 o,         # 6_o: nb_of_nb
                 ini_cond,  # 7_0: past thefts (initialization in zero)
                 p]         # 8_p: SE
                for i in jump for j in jump for k in jump
                for l in jump for m in jump for n in t_jump for o in lamb_jump for p in spread_jump]

    sol_per_pop = len(abm_grid)
    s_chunks = 500
    size = int(sol_per_pop/s_chunks)

    inf = 0
    for k in range(0, size):
        sup = inf + s_chunks
        abm_grid_chunk = abm_grid[inf:sup]

        pool_ip = mp.Pool(cores)
        results = (pool_ip.map_async(_1_0_functions_X4_grilla.cal_pop_fitness, [chrom for chrom in abm_grid_chunk],
                                     error_callback=print)).get()
        pool_ip.close()
        pool_ip.join()

        p_parameters = []
        p_cars_st = []
        p_nb = []
        p_fitness1 = []
        p_fitness2 = []
        p_trials = []

        for i in range(0, len(abm_grid_chunk)):
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

        outF = open(dir+"grid/_"+str(ini_cond)+"_parameters_grid"+str(k)+".txt", "w")
        outF.writelines(str(p_parameters))
        outF.close()

        outF = open(dir+"grid/_"+str(ini_cond)+"_p_nb_grid"+str(k)+".txt", "w")
        outF.writelines(str(theft_nb))
        outF.close()

        outF = open(dir+"grid/_"+str(ini_cond)+"_p_fitness1_grid"+str(k)+".txt", "w")
        outF.writelines(str(p_fitness1))
        outF.close()

        outF = open(dir+"grid/_"+str(ini_cond)+"_p_fitness2_grid"+str(k)+".txt", "w")
        outF.writelines(str(p_fitness2))
        outF.close()

        outF = open(dir+"grid/_"+str(ini_cond)+"_p_trials_grid"+str(k)+".txt", "w")
        outF.writelines(str(p_trials))
        outF.close()

        print(datetime.datetime.now())
        print("End chunk: " + str(k) + " de " + str(size))

        inf += s_chunks

    print("End grid")

