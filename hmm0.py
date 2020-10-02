import sys

# Read the input first


def initializeMatrix(rows, cols): return [
    [0 for c in range(cols)] for r in range(rows)]


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


def matmul(A, B):
    Out = initializeMatrix(len(A), len(B[0]))

    # Take the rows of the first matrix
    for rowA in range(len(A)):
        for colB in range(len(B[0])):
            col = [r[colB] for r in B]  # Get all elements in a column of B
            Out[rowA][colB] = sum([x * y for x, y, in zip(A[rowA], col)])
    return Out


def printMatrix(M):
    rows = len(M)
    cols = len(M[0])
    result = ' '.join(map(str, [element for row in M for element in row]))
    print(f"{rows} {cols} {result}")


read = sys.stdin.read().split("\n")

A = readMatrix(read[0])
B = readMatrix(read[1])
pi = readMatrix(read[2])

states = matmul(pi, A)

# Multiply the result with the observation matrix (B)
obsDist = matmul(states, B)

printMatrix(obsDist)

# We need to compute the probability for observing each observation.

# First we need to multiply the transition matrix (A) with current estimate of states:
