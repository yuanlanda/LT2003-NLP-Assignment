import sys
import os
import argparse
import math
from loader import load_dir

def load_data(rootdir):
    '''
    Loads all the data by searching the given directory for
    subdirectories, each of which represent a class.  Then returns a
    dictionary of class vs. text document instances.
    '''
    classdict = {}
    for classdir in os.listdir(rootdir):
        fullpath = os.path.join(rootdir, classdir)
        print("Loading from {}.".format(fullpath))
        if os.path.isdir(fullpath):
            classdict[classdir] = load_dir(fullpath)
    # print(classdict)

    return classdict

### calc_prob IS THE ONLY FUNCTION TO MODIFY
def calc_prob(classdict, classname, word):
    '''
    Calculates p(classname|word) given the corpus in classdict.
    '''

    word_count_total = 0
    for key in classdict:
        words_list = classdict[key]
        for words in words_list:
            i = 0
            for word_tmp in words:
                i += 1
                if word_tmp == word[0]:
                    if (len(word) > 1 and i < len(words)-1):
                        if words[i] == word[1]:
                            word_count_total +=1
                            break
                    elif len(word) == 1:
                        word_count_total +=1
                        break
                    
    
    word_count_class = 0
    class_words_list = classdict[classname]
    for words in class_words_list:
        i = 0
        for word_tmp in words:
            i +=1
            if word_tmp == word[0]:
                if (len(word) > 1 and i < len(words)-1):
                    if words[i] == word[1]:
                        word_count_class +=1
                        break
                elif len(word) == 1:
                    word_count_class +=1
                    break

    ### YOU FILL IN THIS BLANK, INCLUDING REPLACING THE FOLLOWING
    ### LINE AS APPROPRIATE:
    if word_count_class == 0:
        return 0
    else:
        return word_count_class/word_count_total


if __name__ == "__main__":

    '''
    Entry point for the code. We load the command-line arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("filesdir", help="The root directory containing the class directories and text files.")
    parser.add_argument("classname", help="The class of interest.")
    parser.add_argument("feature", nargs = "+", help="The word of interest for calculating -log2 p(class|feature).")

    args = parser.parse_args()

    corpus = load_data(args.filesdir)

    print("Number of classes in corpus: {}".format(len(corpus)))
    
    print("Looking up probability of class {} given word {}.".format(args.classname, args.feature))
    prob = calc_prob(corpus, args.classname, args.feature)
    if prob == 0:
        print("-log2 p({}|{}) is undefined.".format(args.classname, args.feature))
    else:
        print("-log2 p({}|{}) = {:.3f}".format(args.classname, args.feature, -math.log2(prob)))
    
