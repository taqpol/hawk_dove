import numpy
import numpy as np
from time import strftime
import os
from pylab import *

global payoff
global pop_size
global mutation_count
global recomb_mutate_cycles
pop_size = 2000
payoff = 600
mutation_count = 500
recomb_mutate_cycles = 500


#tabulates the performance of each individual against pop_size/10 random individuals 
#from the same array
def fight(board):
    fitness = []
    for row in range(pop_size):
        pool = np.random.randint(0,pop_size-1,pop_size/10)
        one_player_fitness = np.zeros(len(pool))
        for bouts in range(len(pool)):
            player_1_choice = np.random.randint(0,199)
            player_2_choice = np.random.randint(0,199)
            one_player_fitness[bouts] = \
            (board[row,player_1_choice] > board[bouts,player_2_choice])*\
            (payoff - board[row,player_1_choice]) + \
            (board[row,player_1_choice] < board[bouts,player_2_choice])*\
            (-board[row,player_1_choice]) + \
            (board[row,player_1_choice] == board[bouts,player_2_choice])*(payoff/2)
        fitness.append(one_player_fitness)
    fitness_array = np.asarray(fitness)
    fitness = np.asarray([numpy.mean(fitness_array[x,]) for x in range(pop_size)])
    return fitness


#generates a series of weighted probabilities for each chromosome based on how 
#they did while fighting    
def selection(fitness):
    fitness1 = fitness + abs(min(fitness))
    combined = sum(fitness1)
    fitness = fitness1/combined 
    board_index = np.arange(pop_size)
    selection = np.random.choice(board_index, pop_size, replace=True, p = fitness)
    return selection


#takes one value in randomly selected chromosomes and changes it to something else
def mutate(board_copy):
    selected = np.random.randint(0,pop_size-1, mutation_count)
    for individuals in selected:
        mutated_value = np.random.randint(0,199)
        board_copy[individuals, mutated_value] = np.random.randint(1,1200)
    return board_copy


#selects a point at random and selects two chromosomes. the beginning of each
#chromosome to the point, and the end of each chromosome to the point, are recombined
#to create two novel chromosomes
def crossover(board_copy):
    recombination_point = np.random.randint(0,199)
    parent1 = np.random.randint(0,pop_size-1)
    parent2 = np.random.randint(0,pop_size-1)
    chromosome_break_forward1 = board_copy[parent1, recombination_point:]
    chromosome_break_forward2 = board_copy[parent2, recombination_point:]
    chromosome_break_reverse1 = board_copy[parent1, :recombination_point]
    chromosome_break_reverse2 = board_copy[parent2, :recombination_point]
    board_copy[parent1,] = np.concatenate((chromosome_break_reverse1,
        chromosome_break_forward2))
    board_copy[parent2,] = np.concatenate((chromosome_break_reverse2, 
        chromosome_break_forward1))
    return board_copy


#generates a histogram and dumps raw numpy arrays to a time-stamped folder, 
#numbering each one to prevent file conflicts
def figure_creator(current_array, file_number, parent_dir):
    np.save(os.path.join(parent_dir, 'RawData\\%s' %file_number), current_array)
    file_number += 1
    return file_number
    
    
#creates file paths to store graphs and arrays in, and writes the conditions of
#each run to a file to compare results between runs    
def housekeeping():   
    assert pop_size >= mutation_count, "mutation_count cannot exceed pop_size"
    timestamp = strftime('%B %d %Y, %H %M %S')
    parent_dir = os.path.join(os.path.expanduser("~"), "Desktop\\Graphs\\%s\\" %timestamp)
    os.makedirs(os.path.join(parent_dir, 'RawData'))
    f = open(os.path.join(parent_dir, "conditions.txt"), 'w') 
    f.write('Population size = %s\n\
Number of mutated individuals per round: %s\n\
Resource allocation per round: %s\n\
Rounds of Mutation/Crossover: %s' %(pop_size, mutation_count, payoff,
                                        recomb_mutate_cycles))
    return parent_dir
    
    
#combined function runs all of the above functions according to parameters
#set by the globals
def newgen(selection, fight, mutate, housekeeping):
    file_number = 0
    board = np.random.randint(1,1200,(pop_size,200))
    parent_dir = housekeeping()
    current_array = board
    file_number = figure_creator(current_array, file_number, parent_dir)
    for i in range(recomb_mutate_cycles):
        fitness = fight(board)
        indices = selection(fitness)
        board_copy = board[indices,]
        board_copy = mutate(board_copy)
        board_copy = crossover(board_copy)
        current_array = board_copy
        file_number = figure_creator(current_array, file_number, parent_dir)
    while numpy.array_equal(board,board_copy) == False:
        board = board_copy
        fitness = fight(board)
        indices = selection(fitness)
        board_copy = board[indices,]
        board_copy = crossover(board_copy)
        current_array = board_copy
        file_number = figure_creator(current_array, file_number, parent_dir)
    return board_copy

newgen(selection, fight, mutate, housekeeping)