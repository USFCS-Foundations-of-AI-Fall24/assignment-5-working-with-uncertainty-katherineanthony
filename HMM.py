

import random
import argparse
import codecs
import os
from collections import defaultdict
from fileinput import filename

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
        emit_dict = defaultdict(dict) ## update this to be a default dict
        with open(emit_file, 'r') as f:
            for line in f.readlines():
                line = line.split()
                if line[0] not in emit_dict:
                    emit_dict[line[0]] = {}
                if line[1] not in emit_dict[line[0]]:
                    emit_dict[line[0]][line[1]] = {}
                emit_dict[line[0]].update({line[1]: line[2]})

        trans_dict = defaultdict(dict)
        with open(trans_file, 'r') as f:
            for line in f.readlines():
                line = line.split()
                if line[0] not in trans_dict:
                    trans_dict[line[0]] = {}
                if line[1] not in trans_dict[line[0]]:
                    trans_dict[line[0]][line[1]] = {}
                trans_dict[line[0]].update({line[1]: line[2]})
        if basename == "partofspeech":
            for item in emit_dict.keys():
                sum = 0
                count = 0
                for val in emit_dict[item].keys():
                    sum += float(emit_dict[item].get(val, 0))
                    count += 1

                if sum < 1:
                    for val in emit_dict[item].keys():
                        emit_dict[item][val] = float(emit_dict[item].get(val, 0)) / count
            for item in trans_dict.keys():
                sum = 0
                count = 0
                for val in trans_dict[item].keys():
                    sum += float(trans_dict[item].get(val, 0))
                    count += 1

                if sum < 1:
                    for val in trans_dict[item].keys():
                        trans_dict[item][val] = float(trans_dict[item].get(val, 0)) / count

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

            trans_states.append(str(trans_choice[0]))
            emit_states.append(str(emit_choice[0]))
            curr_state = str(trans_choice[0])
            i += 1

        return Sequence(trans_states, emit_states)

    def forward(self, sequence):

        rows = list(self.transitions.keys()) ## these are the columns
        columns = ["-"] + sequence.outputseq
        row_length = len(rows)
        column_length = len(columns)
        numpy.set_printoptions(suppress=True)
        m = numpy.zeros((row_length, column_length))
        for i in range(column_length):

            for j in range(row_length):
                if j == 0 or i == 0:
                    m[j, i] = 0 ## checking if it's the base case of #
                else:
                    total = 0
                    k = 1
                    if i == 1: ## base case (use hash)
                        curr_mood = rows[j]
                        curr_state = columns[i]
                        prob_curr_res_given_curr_mood = float(self.emissions[curr_mood].get(curr_state, 0))
                        prob_prev_k_mood = float(self.transitions["#"].get(curr_mood, 0))
                        total = prob_curr_res_given_curr_mood * prob_prev_k_mood
                        m[j, i] = round(total, 5)
                    else:
                        while k < len(rows):
                            curr_i_mood = rows[k]
                            curr_mood = rows[j]
                            curr_state = columns[i]
                            prob_curr_res_given_curr_mood = float(self.emissions[curr_mood].get(curr_state, 0))
                            prob_curr_mood_given_k_state = float(self.transitions[curr_i_mood].get(curr_mood, 0))
                            prob_prev_k_mood = float(m[k, i - 1])
                            curr_total = (prob_curr_res_given_curr_mood * prob_curr_mood_given_k_state * prob_prev_k_mood)
                            total += curr_total

                            k += 1

                        m[j, i] = round(total, 5)
        max_state = rows[1]
        for final_i in range(row_length):
            max = 0
            if m[final_i, column_length - 1] > max:
                max = m[final_i, column_length - 1]
                max_state = rows[final_i]
        return max_state



    def viterbi(self, sequence):
        rows = list(self.transitions.keys())  ## these are the columns
        columns = ["-"] + sequence.outputseq
        row_length = len(rows)
        column_length = len(columns)
        numpy.set_printoptions(suppress=True)
        prob_matrix = numpy.zeros((row_length, column_length))
        bk_ptr_matrix = numpy.zeros((row_length, column_length))
        for i in range(column_length):

            for j in range(row_length):
                if j == 0 or i == 0:
                    prob_matrix[j, i] = 0  ## checking if it's the base case of #
                else:
                    k = 1
                    if i == 1:  ## base case (use hash)
                        curr_mood = rows[j]
                        curr_state = columns[i]

                        prob_curr_res_given_curr_mood = self.emissions[curr_mood].get(curr_state, 0)
                        if prob_curr_res_given_curr_mood is None:
                            prob_curr_res_given_curr_mood = 0
                        else:
                            prob_curr_res_given_curr_mood = float(prob_curr_res_given_curr_mood)
                        prob_prev_k_mood = float(self.transitions["#"].get(curr_mood, 0))
                        total = prob_curr_res_given_curr_mood * prob_prev_k_mood
                        prob_matrix[j, i] = total
                        bk_ptr_matrix[j, i] = 0
                    else:
                        max_i = 1
                        max_val = -1
                        while k < len(rows):

                            curr_i_mood = rows[k]
                            if not curr_i_mood == "#":
                                curr_mood = rows[j]
                                curr_state = columns[i]
                                prob_curr_res_given_curr_mood = self.emissions[curr_mood].get(curr_state, 0)
                                if prob_curr_res_given_curr_mood is None:
                                    prob_curr_res_given_curr_mood = 0
                                else:
                                    prob_curr_res_given_curr_mood = float(prob_curr_res_given_curr_mood)
                                prob_curr_mood_given_k_state = (self.transitions[curr_i_mood].get(curr_mood, 0))
                                if prob_curr_mood_given_k_state is None:
                                    prob_curr_mood_given_k_state = 0
                                else:
                                    prob_curr_mood_given_k_state = float(prob_curr_mood_given_k_state)
                                prob_prev_k_mood = float(prob_matrix[k, i - 1])
                                curr_total = (
                                            prob_curr_res_given_curr_mood * prob_curr_mood_given_k_state * prob_prev_k_mood)
                                if curr_total > max_val:
                                    max_val = curr_total
                                    max_i = k
                            k += 1

                        prob_matrix[j, i] = round(max_val, 7)
                        bk_ptr_matrix[j, i] = max_i

        sz = len(columns) - 1

        max_state = rows[1]
        max_i = 1
        for final_i in range(row_length):
            max = 0
            if prob_matrix[final_i, column_length - 1] > max:
                max = prob_matrix[final_i, column_length - 1]
                max_state = rows[final_i]
                max_i = final_i
        state_seq = []
        next_i = int(max_i)

        while sz > 0:
            curr_state = rows[next_i]
            state_seq.append(curr_state)
            next_i = int(bk_ptr_matrix[next_i, sz])
            sz -= 1
        state_seq.reverse()

        return state_seq

    def lander_forward(self, sequence):
        safe_spots = ["2,5", "3,4", "4,3", "4,4", "5,5"]
        spot = self.forward(sequence)
        if spot in safe_spots:
            return "Safe"
        return "Not safe"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('model')
    parser.add_argument('--generate', type=int)
    parser.add_argument('--viterbi', type=str)
    parser.add_argument('--forward', type=str)

    args = parser.parse_args()


    h = HMM()
    h.load(args.model)

    if args.generate is not None:
        print(h.generate(args.generate))
    if args.viterbi or args.forward:
        file = ""
        if args.viterbi:
            file = args.viterbi
        else:
            file = args.forward
        try:
            with open(file, 'r') as f:
                set_seq = False
                set_out = False
                outseq = []
                state_seq = []
                for line in f.readlines():
                    if not set_seq:
                        state_seq = line.split()
                        set_seq = True
                        # print(state_seq)
                    elif not set_out:
                        outseq = line.split()
                        set_out = True
                    if set_seq and set_out:

                        print("for seq:", outseq)
                        if args.viterbi:
                            print("most likely states:", h.viterbi(Sequence(state_seq, outseq)))
                        else:
                            if args.model == "lander":
                                print("next state:", h.lander_forward(Sequence(state_seq, outseq)))
                            else:
                                print("next state:", h.forward(Sequence(state_seq, outseq)))
                        print("------------")

                        set_seq = False
                        set_out = False
                        state_seq = []
                        outseq = []
        except FileNotFoundError:
            print(f"Error: The file {args.viterbi} does not exist.")


