# -*- coding: cp1252 -*-
import itertools

def productOnIterables(iter1,iter2): # cartesianproduct on two iterables
    for a in itertools.product(iter1,iter2):
            yield a

def unique(iterable):
    seen = set()
    for x in iterable:
        if x in seen:
            continue
        seen.add(x)
        yield x

def optionsFactory(steps,extraOptions=[True,False]): #iterator
    permutatedSteps=unique(itertools.permutations(steps))
    finals=productOnIterables(permutatedSteps,extraOptions)
    for final in finals:
        a=list(final[0])
        a.append(3) # three is the code for "apply schemas until you solve the problem"
                    # it appears at the end of the steps
        yield (a,final[1])
