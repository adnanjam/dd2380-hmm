import sys

# Read the input first


def initializeMatrix(rows, cols): return [
    [0.0 for c in range(cols)] for r in range(rows)]


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


read = sys.stdin.read().split("\n")

A = readMatrix(read[0])
N = len(A)
B = readMatrix(read[1])
pi = readMatrix(read[2])

# The sequence of emissions given
seq = [int(x) for x in read[3].strip()[2:].split(" ")]
T = len(seq)


# alpha is a TxN matrix
# T = number of steps in the sequence
# N = number of states in the model
alpha = initializeMatrix(len(seq), N)

# Calculate initial value of alpha (base-case)

obs_0 = seq[0]
# for each state, multiply the P of starting in that state pi[i]
# with the P of observing the first observation in the sequence, at that state
alpha[0] = [pi[0][i] * B[i][obs_0] for i in range(N)]

# Now we can calculate all steps up to T for alpha:
for t in range(1, T):
    obs_t = seq[t]
    for i in range(N):
        alpha[t][i] = sum([alpha[t-1][j] * A[j][i]
                           for j in range(N)]) * B[i][obs_t]

p = sum(alpha[-1])

print(p)
