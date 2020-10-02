import sys

# Read the input first


def initializeMatrix(rows, cols):
    M = []
    for row in range(rows):
        M.append([])
        for col in range(cols):
            M[row].append(0)

    return M


def readMatrix(line):
    rows = int(line[0])
    cols = int(line[2])
    data = line[4:].split(" ")
    M = initializeMatrix(rows, cols)
    i = 0
    for r in range(rows):
        for c in range(cols):
            M[r][c] = float(data[i])
            i += 1
    return M


def matMul(A, B):
    Out = []

    # Take the rows of the first matrix
    for rows in range(len(A)):
        for cols in range(len(B[0])):
            a = true
    return None


read = sys.stdin.read().split("\n")

A = readMatrix(read[0])
B = readMatrix(read[1])
pi = readMatrix(read[2])

print(A)

# We need to compute the probability for observing each observation.

# First we need to multiply the transition matrix (A) with current estimate of states:
