import sys
import math
# Read the input first


# def cap(x): return 1e-20 if x == 0 else x


def argmax(a):
    m = max(a)
    max_idx = [i for i, j in enumerate(a) if j == m]
    return max_idx[-1]


def initializeMatrix(rows, cols): return [
    [float(0) for c in range(cols)] for r in range(rows)]


def readMatrix(line):
    line = line.strip().split(" ")
    rows = int(line[0])
    cols = int(line[1])
    data = line[2:]
    M = initializeMatrix(rows, cols)
    i = 0
    for r in range(rows):
        for c in range(cols):
            try:
                M[r][c] = float(data[i])
            except:
                pass
            i += 1
    return M

def printMatrix(M):
    rows = len(M)
    cols = len(M[0])
    result = ' '.join(map(str, [element for row in M for element in row]))
    print(f"{rows} {cols} {result}")


def calcAlpha(A, B, pi, seq):
    # alpha is a TxN matrix
    # T = number of steps in the sequence
    # N = number of states in the model
    alpha = initializeMatrix(T, N)
    C = [float(0) for i in range(T)] # Initialize C "matrix" (list)

    # Calculate initial value of alpha (base-case)
    # for each state, multiply the P of starting in that state pi[i]
    # with the P of observing the first observation in the sequence, at that state
    alpha[0] = [pi[0][i] * B[i][seq[0]] for i in range(N)]
    C[0] = 1/sum(alpha[0])

    # Scale all alpha[0]:
    alpha[0] = [C[0]*alpha[0][i] for i in range(N)]

    # Now we can calculate all steps up to T for alpha:
    for t in range(1, T):
        for i in range(N):
            alpha[t][i] = sum([alpha[t-1][j] * A[j][i] for j in range(N)]) * B[i][seq[t]]
        C[t] = 1/sum(alpha[t])
        alpha[t] = [C[t]*alpha[t][i] for i in range(N)]

    return alpha, C


def calcBeta(A, B, C, pi, seq):
    # beta is a TxN matrix
    # T = number of steps in the sequence
    # N = number of states in the model
    beta = initializeMatrix(T, N)

    # Calculate last value of beta (base-case)

    # for each state, multiply the P of starting in that state pi[i]
    # with the P of observing the first observation in the sequence, at that state
    beta[-1] = [C[-1]] * N

    # Now we can calculate all steps down to 0 for beta (backwards)
    for t in range(T-2, -1, -1):
        beta[t] = [sum([beta[t+1][j]*B[j][seq[t+1]]*A[i][j] for j in range(N)]) * C[t] for i in range(N)]
    return beta


def calcGammas(A, B, seq, alpha, beta):
    # first calculate d-gamma
    N = len(A)
    T = len(seq)
    
    d_gamma = initializeMatrix(T-1, N)
    gamma = initializeMatrix(T, N)

    for t in range(T-1):
        for i in range(N):
            # initialise the third dimension vector
            d_gamma[t][i] = [float(0) for x in range(N)] 
            for j in range(N):
                d_gamma[t][i][j] = alpha[t][i] * A[i][j] * B[j][seq[t+1]] * beta[t+1][j]
                gamma[t][i] += d_gamma[t][i][j] # Sum over all j's to get gamma

    # Special case for last:
    gamma[-1] = [alpha[-1][i] for i in range(N)]
    return d_gamma, gamma


read = sys.stdin.read().split("\n")

A = readMatrix(read[0])
B = readMatrix(read[1])
pi = readMatrix(read[2])

N = len(A)
K = len(B[0])

# The sequence of emissions given
seq = [int(x) for x in read[3].strip().split(" ")[1:]]
T = len(seq)

maxIterations = 100
iterations = 0
oldLogProb = -math.inf

# Run learning algorithm until max iterations is not reached
while True:


    # 1. Forward-pass: calculate  alpha
    alpha, C = calcAlpha(A, B, pi, seq)

    # 2. Backward-pass: calculate beta
    beta = calcBeta(A, B, C, pi, seq)
    # 3. Compute d-gamma
    d_gamma, gamma = calcGammas(A, B, seq, alpha, beta)

    # 4. Re-estimate pi:
    pi[0] = [gamma[0][i] for i in range(N)]

    # 5. Re-estimate A:
    for i in range(N):
        denominator = sum([gamma[t][i] for t in range(T-1)])
        for j in range(N):
            A[i][j] = sum([d_gamma[t][i][j] for t in range(T-1)]) / denominator

    # 6. Re-estimate B:
    for i in range(N):
        denominator = sum([gamma[t][i] for t in range(T)])
        for j in range(K):
            B[i][j] = sum([gamma[t][i] if seq[t] == j else 0.0 for t in range(T)]) / denominator

    # 7. Check if converged:
    logProb = -sum(map(math.log, C))
    # print(logProb)
    iterations += 1

    if  logProb - oldLogProb > 1e-5 and iterations < maxIterations:
        oldLogProb = logProb
    else:
        break

printMatrix(A)
printMatrix(B)
