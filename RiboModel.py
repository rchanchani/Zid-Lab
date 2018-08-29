"""
Author: Raghav Chanchani
Date last modified: 8/27/2018
Description: Uses a 1-directional discrete-time Markov chain to simulate ribosome distribution
    along a given gene using the assumptions listed below.
References:
1. book.bionumbers.org/what-is-faster-transcription-or-translation
2. http://www.columbia.edu/~ks20/stochastic-I/stochastic-I-MCI.pdf
3. https://github.com/gvanderheide/discreteMarkovChain

Assumptions:
Initiation when ribosome reads AUG
Elongation in-between
Ribosome moves one triplet with each elongation step
If any ribosomes' center position under 30 apart, not allowed to move until >= 30
Termination when ribosome reads UAG, UAA, or UGA
Number of ribosomes conserved
Ribosome covers 30 nucleotides
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
from discreteMarkovChain import markovChain

class ribosome:
    def __init__(self):
        #self.number = 0
        self.position = 0

    #def set_number(self, new_number):
    #    self.number = new_number
    def set_position(self, new_position):
        self.position = new_position

"""
if any ribosomes' center position under 30 apart, not allowed to move until >= 30
if t = 0:
    for ribosome in num_ribo:
        ribosome.center_position = 0
        t += 1
else:
    if ([center_position - 1,center_position,center_position+1] in stop_codon)
"""
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
            gene_length = len(mRNA)
            return inputFileHandle.read(), gene_length, mRNA
    except IOError:
        sys.stderr.write("read_gene - Error: Could not open {}\n".format(fastq))
        sys.exit(-1)

def move(ribosome):
    global gene_length
    global probs
    global probability
    global state_probs
    position = ribosome.position
    moves = False

    # Generate probability matrix for movements to adjacent nucleotides
    for col in range(gene_length):
        for row in range(gene_length):
            if row == col:
                probs[row][col] = probability
                if row == gene_length - 1:
                    probs[row][0] = abs(1-probability)
            if row + 1 == col:
                probs[row][col] = abs(1-probability)
    mc = markovChain(probs)
    mc.computePi('linear')                               # computation method of probabilities
    state_probs = mc.pi                                  # probabilities of moving into different nucleotides
    print('equilibrium state: {}'.format(state_probs))
    moves = np.random.random() < 0.1 # or based on position of ribosome and probs
    if moves:
        ribosome.position = position + 1
    return ribosome

def create_histogram(ribosome_array,gene_length):
    count_array = [ribosome.position for ribosome in ribosome_array]
    plt.hist(count_array, bins = gene_length)
    plt.xlabel('Location on Gene')
    plt.ylabel('Ribosome Frequency');
    plt.show()
    return

def main():
    global gene_length
    global mRNA
    global probs
    global probability
    global state_probs

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('kI',type=float,help='float greater than 0')
    parser.add_argument('kE',type=float,help='float greater than 0')
    parser.add_argument('kT',type=float,help='float greater than 0')
    parser.add_argument('time',type=float,help='float greater than 0')
    args = parser.parse_args()
    ribosomes = 500     # number of ribosomes in simulation
    ribosome_array = [] # storage for all ribosomes in simulation
    gene_length = 0
    mRNA = []
    state_probs = []
    probability = 0.1
    size_ribo = 30      # nt covered by one ribosome
    kR = 20             # nt/s read by ribosomes
    kI = args.kI        # initiation rate
    kE = args.kE        # elongation rate
    kT = args.kT        # termination rate
    time = args.time    # simulation time-length

    if os.path.splitext(str(args.filename))[1] != '.txt':
        parser.error("file must be a .txt file")
    if kI <= 0.0:
        parser.error("initiation rate must be a float greater than 0")
    if kE <= 0.0:
        parser.error("elongation rate must be a float greater than 0")
    if kT <= 0.0:
        parser.error("termination rate must be a float greater than 0")
    if time <= 0.0:
        parser.error("simulation time-length must be a float greater than 0")

    ribosome_array = [ribosome() for complex in range(ribosomes)]
    flag, gene_length, mRNA = read_gene(args.filename)
    probs = np.full((gene_length,gene_length),0.0000)
    for complex in range(len(ribosome_array)):
        ribosome_array[complex] = move(ribosome_array[complex])
    print(probs)
    create_histogram(ribosome_array,gene_length)

if __name__=="__main__": main()
