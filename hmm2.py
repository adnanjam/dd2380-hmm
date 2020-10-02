import sys
from math import log
from decimal import Decimal
# Read the input first


def argmax(a):
    m = max(a)
    max_idx = [i for i, j in enumerate(a) if j == m]
    return max_idx[-1]


def initializeMatrix(rows, cols): return [
    [Decimal(0) for c in range(cols)] for r in range(rows)]


def readMatrix(line):
    rows = int(line[0])
    cols = int(line[2])
    data = line[4:].split(" ")
    M = initializeMatrix(rows, cols)
    i = 0
    for r in range(rows):
        for c in range(cols):
            try:
                M[r][c] = Decimal(data[i])
            except:
                pass
            i += 1
    return M


read = sys.stdin.read().split("\n")

A = readMatrix(read[0])
B = readMatrix(read[1])
pi = readMatrix(read[2])

N = len(A)

# The sequence of emissions given
seq = [int(x) for x in read[3].strip()[2:].split(" ")]
T = len(seq)

# delta is a TxN matrix
# T = number of steps in the sequence
# N = number of states in the model
delta = initializeMatrix(T, N)
delta_idx = initializeMatrix(len(seq), N)
# Calculate initial value of delta (base-case)

obs_0 = seq[0]
# for each state, multiply the P of starting in that state pi[i]
# with the P of observing the first observation in the sequence, at that state
# delta[0] = [log(pi[0][i] * B[i][obs_0]) for i in range(N)]
delta[0] = [pi[0][i] * B[i][obs_0] for i in range(N)]

# delta_idx[0] = argmax(delta[0])

# Now we can calculate all steps up to T for delta:
for t in range(1, T):
    obs_t = seq[t]
    # print(f"\nT: {t}")
    for i in range(N):
        temp = [delta[t-1][j] * A[j][i] * B[i][obs_t] for j in range(N)]
        # print(temp)
        delta[t][i] = max(temp)
        # store the index of most likely state
        delta_idx[t][i] = argmax(temp)

    # print(f"Delta: {t} {delta[t]}")

X = [0 for i in range(T)]  # initialize path list

X[-1] = argmax(delta[-1])  # set the last element


for t in range(T-2, -1, -1):
    # print(t)
    prev_idx = X[t+1]
    X[t] = delta_idx[t+1][prev_idx]


print(" ".join(map(str, X)))
