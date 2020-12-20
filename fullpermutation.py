import copy
from functools import lru_cache
All = []

@lru_cache()
def fullpermutation(string, k, m):
    if k == m:
        All.append(copy.copy(string))
        return
    else:
        for i in range(k, m):
            string[k], string[i] = string[i], string[k]
            fullpermutation(string, k + 1, m)
            string[k], string[i] = string[i], string[k]  
    

def perm(string):
    string = list(string)
    fullpermutation(string, 0, len(string))
    return All
            
    
