

import random
import argparse
import codecs
import os
from collections import defaultdict

import numpy

# Sequence - represents a sequence of hidden states and corresponding
# output variables.

class Sequence:
    def __init__(self, stateseq, outputseq):
        self.stateseq  = stateseq   # sequence of states
        self.outputseq = outputseq  # sequence of outputs
    def __str__(self):
        return ' '.join(self.stateseq)+'\n'+' '.join(self.outputseq)+'\n'
    def __repr__(self):
        return self.__str__()
    def __len__(self):
        return len(self.outputseq)

# HMM model
class HMM:
    def __init__(self, transitions={}, emissions={}):
        """creates a model from transition and emission probabilities
        e.g. {'happy': {'silent': '0.2', 'meow': '0.3', 'purr': '0.5'},
              'grumpy': {'silent': '0.5', 'meow': '0.4', 'purr': '0.1'},
              'hungry': {'silent': '0.2', 'meow': '0.6', 'purr': '0.2'}}"""



        self.transitions = transitions
        self.emissions = emissions

    ## part 1 - you do this.
    def load(self, basename):
        """reads HMM structure from transition (basename.trans),
        and emission (basename.emit) files,
        as well as the probabilities."""

        emit_file = basename + '.emit'
        trans_file = basename + '.trans'
        emit_dict = {}
        with open(emit_file, 'r') as f:
            for line in f.readlines():
                line = line.split()
                if line[0] not in emit_dict:
                    emit_dict[line[0]] = {}
                if line[1] not in emit_dict[line[0]]:
                    emit_dict[line[0]][line[1]] = {}
                emit_dict[line[0]].update({line[1]: line[2]})

        trans_dict = {}
        with open(trans_file, 'r') as f:
            for line in f.readlines():
                line = line.split()
                if line[0] not in trans_dict:
                    trans_dict[line[0]] = {}
                if line[1] not in trans_dict[line[0]]:
                    trans_dict[line[0]][line[1]] = {}
                trans_dict[line[0]].update({line[1]: line[2]})

        self.emissions = emit_dict
        self.transitions = trans_dict
        return

   ## you do this.
    def generate(self, n):
        ## monte carlo situation
        i = 0
        initial_state = random.choice(list(self.transitions.get("#").keys()))
        trans_states = []
        emit_states = []
        curr_state = initial_state
        while i < n:
            trans_keys = list(self.transitions.get(curr_state).keys())
            trans_values = list(map(float, list(self.transitions[curr_state].values())))
            trans_choice = random.choices(population=trans_keys, weights=trans_values)

            emit_keys = list(self.emissions.get(curr_state).keys())
            emit_values = list(map(float, list(self.emissions[curr_state].values())))
            emit_choice = random.choices(population=emit_keys, weights=emit_values)
            ## generate Sequence
            trans_states.append(str(trans_choice[0]))
            emit_states.append(str(emit_choice[0]))
            curr_state = str(trans_choice[0])
            i += 1

        return trans_states + emit_states

    def forward(self, sequence):
        pass ## TODO: do this first
    ## you do this: Implement the Viterbi algorithm. Given a Sequence with a list of emissions,
    ## determine the most likely sequence of states.






    def viterbi(self, sequence):
        pass
    ## You do this. Given a sequence with a list of emissions, fill in the most likely
    ## hidden states using the Viterbi algorithm.


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('model')
    parser.add_argument('--generate', type=int)

    args = parser.parse_args()

    h = HMM()
    h.load(args.model)
    print(h.generate(args.generate))


