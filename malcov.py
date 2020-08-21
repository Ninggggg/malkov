import sys
import math
from typing import List
import random

L = 6
H = 5
epsilon = 0.01
gamma = 0.99

r = [None for i in range(L * H)]

for i in range(1, 4):
    for j in range(1, 5):
        if i != 2 or j != 2:
            if i == 1 and j == 4:
                r[i * L + j] = 1
            elif i == 2 and j == 4:
                r[i * L + j] = -1
            else:
                r[i * L + j] = -0.04

def display(r): #display the maze
    for i in range(H):
        for j in range(L):
            if r[i * L + j] == None:
                sys.stdout.write('W')
            else:
                sys.stdout.write('.')
        print('')

def value_iteration():  # value iteration
    U1 = [0 for i in range(L * H)]  # initial all the U zero
    index = []
    for i in range(L * H):
        index.append(None)
    while True:
        U = U1[:]
        delta = 0
        for k in range(H * L):
            if r[k] != None:
                if k != L + 4 and k != 2 * L + 4:
                    lis = sum_uti(k, U)
                    maxi = max(lis)
                    ind = lis.index(max(lis))
                    U1[k] = r[k] + gamma * maxi
                    index[k] = ind
                else:
                    U1[k] = r[k]
                    index[k] = -1
                delta = max(delta, abs(U1[k] - U[k]))
        print(U1)
        if delta < epsilon * (1 - gamma) / gamma:
            break
    return U1, index

def iter_display(x):
    for i in range(H):
        for j in range(L):
            if x[i * L + j] == None:
                sys.stdout.write('W')
            elif i == 1 and j == 4:
                sys.stdout.write('+')
            elif i == 2 and j == 4:
                sys.stdout.write('-')
            elif x[i * L + j] == 0:
                sys.stdout.write('<')
            elif x[i * L + j] == 1:
                sys.stdout.write('>')
            elif x[i * L + j] == 2:
                sys.stdout.write('^')
            elif x[i * L + j] == 3:
                sys.stdout.write('v')
        print('')

def sum_uti(x, U):
    d = [None for i in range(4)]
    count = 0
    xarr = [x - 1, x + 1, x - 6, x + 6]
    for i in xarr:
        if r[i] == None:
            d[count] = U[x]
        else:
            d[count] = U[i]
        count = count + 1
    left = 0.8 * d[0] + 0.1 * d[2] + 0.1 * d[3]
    right = 0.8 * d[1] + 0.1 * d[2] + 0.1 * d[3]
    up = 0.8 * d[2] + 0.1 * d[0] + 0.1 * d[1]
    down = 0.8 * d[3] + 0.1 * d[0] + 0.1 * d[1]
    lis = [left, right, up, down]
    return lis

"""
display(r)
u_final, direc_final = value_iteration()
print('')
iter_display(direc_final)
"""

def policy_iteration():
    U = [0 for i in range(L * H)]
    pi = [None for i in range(L * H)]
    for i in range(L * H):
        if r[i] != None:
            pi[i] = random.randint(0, 3)
    while True:
        U = policy_evaluation(pi, U)
        unchanged = True
        for k in range(H * L):
            if r[k] != None:
                if k != L + 4 and k != 2 * L + 4:
                    lis = sum_uti(k, U)
                    ind = lis.index(max(lis))
                    if ind != pi[k]:
                        pi[k] = ind
                        unchanged = False
        if unchanged:
            return pi

def policy_evaluation(pi, U):
    for i in range(L * H):
        if r[i] != None:
            if i != L + 4 and i != 2 * L + 4:
                lis = sum_uti(i, U)
                d = pi[i]
                U[i] = r[i] + gamma * lis[d]
            else:
                U[i] = r[i]
                pi[i] = -1
    return U

pi = policy_iteration()
iter_display(pi)