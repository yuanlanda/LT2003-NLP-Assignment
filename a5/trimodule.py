import sys
import os
import random

class TrigramModel:
    def __init__(self, inputstring, n, seed):
        self.tridict = {}
        self.outputstring = ''
        for position in range(len(inputstring) - 2):
            char0 = inputstring[position] + inputstring[position + 1]
            char1 = inputstring[position + 2]

            if char0 in self.tridict:
                if char1 in self.tridict[char0]:
                    self.tridict[char0][char1] += 1
                else:
                    self.tridict[char0][char1] = 1
            else:
                self.tridict[char0] = {}
                self.tridict[char0][char1] = 1

        self.probdict = {}
        for char0 in self.tridict.keys():
            if char0 not in self.probdict:
                self.probdict[char0] = {}

            for char1 in self.tridict[char0].keys():
                fullcount = sum(self.tridict[char0].values())
                self.probdict[char0][char1] = self.tridict[char0][char1]/fullcount

    def __getitem__(self,item):
        return self.outputstring[item]

class TrigramModelWithDistribution(TrigramModel):
    def __init__(self, inputstring, n, seed):
        super().__init__(inputstring, n, seed)
        '''
        Predicts n characters using random sampling from the 
        distribution starting with the seed.
        '''
        if len(seed) != 2:
            raise ValueError("Need exactly two characters for prediction.")

        inputchar0 = seed

        self.outputstring = "{}".format(inputchar0) 
        for output in range(n):
            choices = self.probdict[inputchar0]
            randomval = random.random()
            total = 0
            mychoice = ''
            for key in choices:
                total += choices[key]
                if randomval < total:
                    mychoice = key
                    break
        #options = sorted(choices.keys(), key=lambda x: choices[x], reverse=True)
        #print(options)
            self.outputstring += mychoice


class TrigramModelWithTopK(TrigramModel):
    def __init__(self, inputstring, n, seed, k):
        super().__init__(inputstring, n, seed)
        self.k = k

        '''
        Predicts n characters using random sampling from the 
        distribution starting with the seed.
        '''
        if len(seed) != 2:
            raise ValueError("Need exactly two characters for prediction.")

        inputchar0 = seed

        self.outputstring = "{}".format(inputchar0)
        for output in range(n):
            choices = self.probdict[inputchar0]
            options = sorted(choices.keys(), key=lambda x: choices[x], reverse=True)
            mychoice = random.choice(options[:k])
        #print(options)
            self.outputstring += mychoice
