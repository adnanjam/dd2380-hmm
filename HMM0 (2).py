import sys

# Read the input first


def readMatrix(line):
    rows = int(line[0])
    cols = int(line[2])
    data = line[4:].split(" ")
    M = []
    i = 0
    for r in range(rows):
        M.append([])
        for c in range(cols):
            M[r].append(data[i])
            i += 1
    return M


def matMul(A, B):
    return None


read = sys.stdin.read().split("\n")

A = readMatrix(read[0])
B = readMatrix(read[1])
pi = readMatrix(read[2])

print(A)

# We need to compute the probability for observing each observation.

# First we need to multiply the transition matrix (A) with current estimate of states:
