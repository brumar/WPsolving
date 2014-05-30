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

def optionsFactory(options): #iterator
    listes=unique(itertools.permutations(options))
    finals=productOnIterables(listes,[True,False])
    for final in finals:
        a=list(final[0])
        a.append(3)
        yield (a,final[1])
