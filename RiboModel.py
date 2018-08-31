"""
Author: Raghav Chanchani
Date last modified: 8/30/2018
Description: Uses a discrete-time Markov chain to simulate ribosome distribution
    along a given gene using the assumptions listed below. No final absorption state.
    Does not consider specific nucleotides.
References:
1. book.bionumbers.org/what-is-faster-transcription-or-translation
2. http://www.columbia.edu/~ks20/stochastic-I/stochastic-I-MCI.pdf
3. https://github.com/gvanderheide/discreteMarkovChain

Assumptions:
Initiation when ribosome reads AUG
Elongation in-between
Ribosome moves one triplet with each elongation step
Ribosomes are recycled once they move off of the gene
If any ribosomes' center position under 30 apart, not allowed to move until >= 30
Termination when ribosome reads UAG, UAA, or UGA
Number of ribosomes conserved
(Ribosome may be 30 nt long in reality but is user-defined here)
Ribosome reads 60nt/s at max (1)
"""
import numpy as np
import math
import sys
import os
from os import path
import argparse
from itertools import chain
import matplotlib.pyplot as plt
#from discreteMarkovChain import markovChain

class ribosome:
    def __init__(self):
        self.position = -1
        self.counter = 0
    def set_position(self, new_position):
        self.position = new_position
    def set_counter(self, new_count):
        self.counter = new_count

def read_gene(fastq):
    global gene_length
    global mRNA
    temp_list = []

    try:
        with open(fastq) as inputFileHandle:
            line_list = [lines.split() for lines in inputFileHandle]  # extract lines
            while line_list:
                temp_list.extend(line_list.pop(0))
                while temp_list:
                    mRNA.extend(temp_list.pop(0))
            gene_length = int(len(mRNA)/3)
            return inputFileHandle.read(), gene_length, mRNA
    except IOError:
        sys.stderr.write("read_gene - Error: Could not open {}\n".format(fastq))
        sys.exit(-1)

def make_matrix():
    global probability
    global gene_length
    #global probs

    for col in range(gene_length):
        for row in range(gene_length):
            if row == col:
                probs[row][col] = probability
                if row == gene_length - 1:
                    probs[row][0] = abs(1-probability)
            if row + 1 == col:
                probs[row][col] = abs(1-probability)
    mc = markovChain(probs)
    mc.computePi('linear')                                      # computation method of steady-state probabilities
    steady_state_probs = mc.pi                                  # steady-state probabilities of moving into different nucleotides
    print('equilibrium state: {}'.format(steady_state_probs))

    return

def move(ribosome):
    global gene_length
    global probability
    global steady_state_probs

    position = ribosome.position
    if ribosome.position < gene_length:
        moves = np.random.random() <= probability # or based on position of ribosome and probs
        if moves:
            ribosome.position = position + 1
            ribosome.counter = 1
        else:
            ribosome.counter += 1
    return ribosome

def create_histogram(ribosome_array):
    global gene_length
    global ribo_size
    global fname

    count_array = [ribosome.position for ribosome in ribosome_array]
    ax = plt.gca()
    ax.set_title('Ribosome Occupancy ' + os.path.splitext(str(fname))[0])
    #ax.set_xscale('log')
    ax.set_yscale('log')
    plt.hist(count_array, bins=range(min(count_array)*200,gene_length + 10, 10))
    #plt.hist(count_array,range=[-1,gene_length],bins=gene_length)
    plt.xlabel('Location on Gene (codon)')
    plt.ylabel('Ribosome Frequency');
    plt.show()

    return

def main():
    global gene_length
    global mRNA
    #global probs
    global probability
    global steady_state_probs
    global ribo_size
    global fname

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('kI',type=float,help='float greater than 0.0 rib./sec.')
    parser.add_argument('kE',type=float,help='float greater than 0.0 codon./sec.')
    parser.add_argument('time',type=int,help='integer greater than 0 sec.')
    parser.add_argument('probability',type=float,help='float greater than 0.0 odds of moving forward.')
    parser.add_argument('size',type=int,help='integer greater than 0 nucleotides.')

    args = parser.parse_args()
    ribosomes = 200     # number of ribosomes in simulation
    ribosome_array = [] # storage for all ribosomes in simulation
    gene_length = 0
    mRNA = []
    steady_state_probs = []
    #kR = 20.0/3.0           # aa/s formed by ribosomes
    kI = args.kI        # initiation rate
    kE = args.kE        # elongation rate
    time = args.time    # simulation time-length
    probability = args.probability
    ribo_size = args.size      # nt covered by one ribosome
    fname = args.filename
    if os.path.splitext(str(fname))[1] != '.txt':
        parser.error("file must be a .txt file")
    if kI <= 0.0:
        parser.error("initiation rate must be a float greater than 0 rib./sec.")
    if kE <= 0.0:
        parser.error("elongation rate must be a float greater than 0.0 codon./sec.")
    if time <= 0:
        parser.error("simulation time-length must be an integer greater than 0 seconds")
    if probability <= 0.0:
        parser.error("probability of ribosome movement must be a float greater than 0.0")
    if ribo_size <= 0:
        parser.error("simulation ribosome length must be an integer greater than 0 nucleotides")

    ribosome_array = [ribosome() for complex in range(ribosomes)]
    flag, gene_length, mRNA = read_gene(args.filename)
    #probs = np.full((gene_length/3,gene_length/3),0.0)
    discrete_time = [step for step in range(time)]
    for t_step in discrete_time:
        for complex in range(len(ribosome_array) - 1): # for each ribosome...
            step = ribosome_array[complex].counter
            if t_step % kI == 0: # if initiation timestep
                if step % kE == 0: # if elongation timestep
                    if ribosome_array[complex].position == 0: # if at beginning of gene
                        if complex == 0: # if first ribosome in the simulation
                            if ribosome_array[complex].counter == 1: # if just arrived at beginning of gene
                                ribosome_array[complex].counter += 1
                                continue # move on to next ribosome
                            else: ribosome_array[complex] = move(ribosome_array[complex]) # if not just arrived then attempt to move
                        else:
                            if abs(ribosome_array[complex].position-ribosome_array[complex-1].position) > \
                            ribo_size-1: # if correct distance fom other ribosome
                                ribosome_array[complex] = move(ribosome_array[complex])
                            else: ribosome_array[complex].counter += 1
                    elif ribosome_array[complex].position == -1: # if not on gene yet
                        if complex == 0: # if first ribosome in the simulation
                            moves = np.random.random() <= probability
                            if moves:
                                ribosome_array[complex].counter = 1
                                ribosome_array[complex].position = 0
                            else: ribosome_array[complex].counter += 1
                        else:
                            if abs(ribosome_array[complex].position-ribosome_array[complex-1].position) > \
                            ribo_size-1: # if correct distance fom other ribosome
                                moves = np.random.random() <= probability
                                if moves:
                                    ribosome_array[complex].counter = 1
                                    ribosome_array[complex].position = 0
                                else: ribosome_array[complex].counter += 1
                            else: ribosome_array[complex].counter += 1
                    else: # if somewhere on gene not at beginning
                        if complex == 0: # if first ribosome in the simulation
                            ribosome_array[complex] = move(ribosome_array[complex])
                            if ribosome_array[complex].position > gene_length:
                                ribosome_array[complex].position = -1
                                ribosome_array[complex].counter = 0
                        else:
                            if abs(ribosome_array[complex].position-ribosome_array[complex-1].position) > \
                            ribo_size-1:
                                ribosome_array[complex] = move(ribosome_array[complex])
                                if ribosome_array[complex].position > gene_length: # if the ribosome leaves the ribosome it is recycled
                                    ribosome_array[complex].position = -1
                                    ribosome_array[complex].counter = 0
                            else: ribosome_array[complex].counter += 1
                else: # if not an elongation timestep and only an initiation timestep
                    if complex == 0: # if first ribosome in the simulation
                        if ribosome_array[complex].position == -1:
                            moves = np.random.random() <= probability
                            if moves:
                                ribosome_array[complex].counter = 1
                                ribosome_array[complex].position = 0
                        else: ribosome_array[complex].counter += 1 # check other conditions
                    else: # if complex > 0
                        if ribosome_array[complex].position == -1: # if ribosome was not initialized
                            if abs(ribosome_array[complex].position-ribosome_array[complex-1].position) > \
                            ribo_size-1:
                                moves = np.random.random() <= probability
                                if moves:
                                    ribosome_array[complex].counter = 1
                                    ribosome_array[complex].position = 0
                            else: ribosome_array[complex].counter += 1
                        else: ribosome_array[complex].counter += 1
            else: # if not an initiation timestep
                if ribosome_array[complex].position == 0: # if at the beginning of the mRNA
                    if step % kE == 0: # if an elongation step
                        if complex == 0: # if first ribosome in the simulation
                                ribosome_array[complex] = move(ribosome_array[complex]) # attempt to move
                                if ribosome_array[complex].position > gene_length: # if the ribosome leaves the ribosome it is recycled
                                    ribosome_array[complex].position = -1
                                    ribosome_array[complex].counter = 0
                        else:
                            if abs(ribosome_array[complex].position-ribosome_array[complex-1].position) > \
                            ribo_size-1: # if correct distance away from other ribosomes
                                ribosome_array[complex].position = move(ribosome_array[complex]) # attempt to move
                                if ribosome_array[complex].position > gene_length: # if the ribosome leaves the ribosome it is recycled
                                    ribosome_array[complex].position = -1
                                    ribosome_array[complex].counter = 0
                            else: ribosome_array[complex].counter += 1
                    else: ribosome_array[complex].counter += 1 # if not an elongation step then increment amount of time spent in current state
                elif ribosome_array[complex].position > 0: # if away from the beginning of the mRNA
                    if step % kE == 0: # if elongation step
                        if complex == 0:
                                ribosome_array[complex].position = move(ribosome_array[complex])
                                if ribosome_array[complex].position > gene_length: # if the ribosome leaves the ribosome it is recycled
                                    ribosome_array[complex].position = -1
                                    ribosome_array[complex].counter = 0
                        else:
                            if abs(ribosome_array[complex].position-ribosome_array[complex-1].position) > \
                            ribo_size-1:
                                ribosome_array[complex].position = move(ribosome_array[complex])
                                if ribosome_array[complex].position > gene_length: # if the ribosome leaves the ribosome it is recycled
                                    ribosome_array[complex].position = -1
                                    ribosome_array[complex].counter = 0
                            else: ribosome_array[complex].counter += 1
                    else: ribosome_array[complex].counter += 1 # if not an elongation step then increment amount of time spent in current state
                else:
                    if step % kE == 0:
                        continue
                    else: ribosome_array[complex].counter += 1 # if the ribosome was in state -1 then increment time spent in current state

    create_histogram(ribosome_array)
    print("1st ribosome simulate has been in current position for {} second(s) and is at codon {}.\n".format(ribosome_array[0].counter,ribosome_array[0].position))
    print("3rd ribosome simulate has been in current position for {} second(s) and is at codon {}.\n".format(ribosome_array[2].counter,ribosome_array[2].position))
    print("10th ribosome simulate has been in current position for {} second(s) and is at codon {}.".format(ribosome_array[9].counter,ribosome_array[9].position))

if __name__=="__main__": main()

