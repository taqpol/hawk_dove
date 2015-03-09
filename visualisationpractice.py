import numpy
import numpy as np
from time import time, strftime
import os
from pylab import *

global k
global y
global mutation_count
global recomb_mutate_cycles
y = 2000
k = 150
mutation_count = 600
recomb_mutate_cycles = 700


def fight(board):
    fitness = []
    for row in range(y):
        pool = np.random.randint(0,y-1,y/10)
        one_player_fitness = np.zeros(len(pool))
        for bouts in range(len(pool)):
            player_1_choice = np.random.randint(0,199)
            player_2_choice = np.random.randint(0,199)
            one_player_fitness[bouts] = \
            (board[row,player_1_choice] > board[bouts,player_2_choice])*\
            (k - board[row,player_1_choice]) + \
            (board[row,player_1_choice] < board[bouts,player_2_choice])*\
            (-board[row,player_1_choice]) + \
            (board[row,player_1_choice] == board[bouts,player_2_choice])*(k/2)
        fitness.append(one_player_fitness)
    fitness_array = np.asarray(fitness)
    fitness = np.asarray([numpy.mean(fitness_array[x,]) for x in range(y)])
    return fitness

    
def selection(fitness):
    fitness1 = fitness + abs(min(fitness))
    combined = sum(fitness1)
    fitness = fitness1/combined 
    board_index = np.arange(y)
    selection = np.random.choice(board_index, y, replace=True, p = fitness)
    return selection


def mutate(board_copy):
    selected = np.random.randint(0,y-1, mutation_count)
    for individuals in selected:
        mutated_value = np.random.randint(0,199)
        board_copy[individuals, mutated_value] = np.random.randint(1,1200)
    return board_copy


def crossover(board_copy):
    recombination_point = np.random.randint(0,199)
    parent1 = np.random.randint(0,y-1)
    parent2 = np.random.randint(0,y-1)
    chromosome_break_forward1 = board_copy[parent1, recombination_point:]
    chromosome_break_forward2 = board_copy[parent2, recombination_point:]
    chromosome_break_reverse1 = board_copy[parent1, :recombination_point]
    chromosome_break_reverse2 = board_copy[parent2, :recombination_point]
    board_copy[parent1,] = np.concatenate((chromosome_break_reverse1,
        chromosome_break_forward2))
    board_copy[parent2,] = np.concatenate((chromosome_break_reverse2, 
        chromosome_break_forward1))
    return board_copy

def figure_creator(current_array, file_number):
    q = arange(y)
    chromosome_contents = [numpy.mean(current_array[i,]) for i in range(y)]
    hist2d(chromosome_contents,q, bins = 60)
    #os.makedirs(os.path.join("C:\\Users\\Nike\\Desktop\\Graphs\\2D Hist\\", strftime('%c')))
    savefig('C:\\Users\\Nike\\Desktop\\Graphs\\2D Hist\\%s.png' %file_number)
#    hist(chromosome_contents)
#    savefig('C:\\Users\\Nike\\Desktop\\Graphs\\1D Hist\\histogram %s.png' %file_number)
#    scatter(chromosome_contents,q)
#    savefig('C:\\Users\\Nike\\Desktop\\Graphs\\Scatter\\scatter %s.png' %file_number)
#    new_directory = os.path.join("C:\\Users\\Nike\\Desktop\\Graphs\\2D Hist\\", strftime('%c'))
#    os.makedirs(new_directory)
    np.save('C:\\Users\\Nike\\Desktop\\Graphs\\RawData\\%s' %file_number, current_array)
    file_number += 1
    return file_number
    
def newgen(selection, fight, mutate):
    file_number = 0
    board = np.random.randint(1,1200,(y,200))
    current_array = board
    file_number = figure_creator(current_array, file_number)
    for i in range(recomb_mutate_cycles):
        fitness = fight(board)
        indices = selection(fitness)
        board_copy = board[indices,]
        board_copy = mutate(board_copy)
        board_copy = crossover(board_copy)
        current_array = board_copy
        file_number = figure_creator(current_array, file_number)
    while numpy.array_equal(board,board_copy) == False:
        board = board_copy
        fitness = fight(board)
        indices = selection(fitness)
        board_copy = board[indices,]
        board_copy = crossover(board_copy)
        current_array = board_copy
        file_number = figure_creator(current_array, file_number)
    return board_copy


then = time()
f = newgen(selection,fight,mutate)
print("Ran in %s seconds" % (time()-then))

#remember to implement a time/date sensitive naming convention
