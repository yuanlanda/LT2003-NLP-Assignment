import os
import sys
### YOU CAN ADD STANDARD PYTHON MODULE IMPORTS HERE IF YOU NEED THEM

def displayArcs(arcs, sentence):
    print(sentence)

    for arc in arcs:
        h, d, l = arc
        print(sentence[h]["form"], "---" + l + "-->", sentence[d]["form"])
    print()


def displayOriginalArcs(sentence):
    for x in sorted(sentence):
        if sentence[x]["head"] > 0:
            print(sentence[sentence[x]["head"]]["form"], "---" + sentence[x]["deprel"] + "-->", sentence[x]["form"])
    print()


### YOU WILL MODIFY THIS FUNCTION
def parse_arc_eager(sentence, transition_list = None):
    stack = []
    buffer = [x for x in sorted(sentence)]
    arcs = []
    # print(buffer)
    while buffer != []:
        # pick the first transition
        t = transition_list.pop(0)

        #i = top element of the stack
        i = None if len(stack) == 0 else stack[0]

        # j = first element of the buffer
        j = buffer[0]

        if t == 'SHIFT':
            stack.append(j)
            buffer.pop(0)
        elif "LEFT-ARC-" in t:
            if len(stack) < 2:
                stack.append(j)
                buffer.pop(0)
            arcs.append([stack[-1],stack[-2],t[9:]])
            stack.pop(-2)
        elif "RIGHT-ARC-" in t:
            if len(stack) < 2:
                stack.append(j)
                buffer.pop(0)
            arcs.append([stack[-2],stack[-1],t[10:]])
        elif t == 'REDUCE':
            stack.pop()
        
    return arcs

    
def test_parse():
    sentence = {
        1: {"form": "the"},
        2: {"form": "cat"},
        3: {"form": "sits"},
        4: {"form": "on"},
        5: {"form": "the"},
        6: {"form": "mat"},
        7: {"form": "today"}
    }
    
    transition_sequence = ["SHIFT", "LEFT-ARC-det", "SHIFT", "LEFT-ARC-nsubj", "SHIFT", "SHIFT", "SHIFT", "LEFT-ARC-det", "LEFT-ARC-case", "RIGHT-ARC-nmod", "REDUCE", "RIGHT-ARC-advmod", "REDUCE"]
    
    arcs = parse_arc_eager(sentence, transition_list=transition_sequence)
    displayArcs(arcs, sentence)



if __name__ == "__main__":
    test_parse()
