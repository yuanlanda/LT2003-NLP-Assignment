Part 1

I used python magic methods '__getitem__' to return outputstring at each generated character when 'character' in 'model'(the instance of TrigramModelWithDistribution) is called in the for loop in trigram.py. But I'm curious about why should we design such mechanism to get the value of outputstring instead of calling the predict function directly？



Part 2

Unchanged 3-layer nested dictionaries of probdict example:

{'\n': {'J': {'A': 0.18518518518518517, 'a': 0.48148148148148145, 'o': 0.1111111111111111, 'u': 0.14814814814814814, ' ': 0.037037037037037035, 'O': 0.037037037037037035}}}


I merged the first two dictionaries together. This is my 2-layer nested dictionaries of probdict example:

{'\nJ': {'A': 0.18518518518518517, 'a': 0.48148148148148145, 'o': 0.1111111111111111, 'u': 0.14814814814814814, ' ': 0.037037037037037035, 'O': 0.037037037037037035}}



Part 3

I add another integer argument 'k' to parser and TrigramModelWithTopK initial method require arguments. The outputstring is the k top ranked alternatives choosed from the model.

command instruction example:
      
      python3 trigram.py --topk ./crude 10 yo 3

