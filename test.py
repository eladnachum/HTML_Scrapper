#!/bin/python

import sys
def calculate_possible_steps(current,step_type,path):
    steps = []
    arith = [1,-1]

    for x in arith:
        for y in arith:
            if (0 <= (current[0] + (x * step_type[0])) <= n - 1 and 0 <= (current[1] + (y *step_type[1])) <= n - 1):
                if ([(current[0] + (x * step_type[0])),(current[1] + (y *step_type[1]))] not in path):
                    steps.append ([(current[0] + (x * step_type[0])),(current[1] + (y *step_type[1]))])
    for x in arith:
        for y in arith:
            if (0 <= (current[0] + (x * step_type[1])) <= n - 1 and 0 <= (current[1] + (y *step_type[0])) <= n - 1):
                if ([(current[0] + (x * step_type[1])),(current[1] + (y *step_type[0]))] not in path):
                    steps.append ([(current[0] + (x * step_type[1])),(current[1] + (y *step_type[0]))])
    return steps

def go(current,step_type,path):
    if (current[0] is n-1 and current[1] is n-1):
        if knights[i-1][j-1] is -1:
            knights[i-1][j-1] = len(path)
        else:
            knights [i-1][j-1] = min(len(path),knights[i-1][j-1])
        return

    possible_steps = calculate_possible_steps(current,step_type,path)
    for step in possible_steps:
        path.append(step)
        go(step,step_type,path)
        path.pop()
    return

n=5
knights = [[-1 for x in range(1,n)] for y in range(1,n)]


for i in range (1,n):
    for j in range (1,n):
            #knights[i][j] = how_many(0,0,i,j)
            go([0,0],[i,j],[])

print knights