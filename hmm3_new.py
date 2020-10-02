import sys
import math
   
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
    # result = ' '.join(map(str, [round(element, 6) for row in M for element in row]))
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

    for i in range(N):
        alpha[0][i] = pi[0][i]*B[i][seq[0]]
        C[0] += alpha[0][i]
    
    C[0] = 1/C[0]
    # Scale all alpha[0]:
    for i in range(N):
        alpha[0][i] = C[0]*alpha[0][i]

    # Now we can calculate all steps up to T for alpha:
    for t in range(1, T):
        for i in range(N):
            for j in range(N):
                alpha[t][i] += alpha[t-1][j] * A[j][i]
            
            alpha[t][i] = alpha[t][i] * B[i][seq[t]]
            C[t] += alpha[t][i]

        C[t] = 1/C[t]
        for i in range(N):
            alpha[t][i] = C[t] * alpha[t][i]

    return alpha, C


def calcBeta(A, B, C, pi, seq):
    # beta is a TxN matrix
    # T = number of steps in the sequence
    # N = number of states in the model
    beta = initializeMatrix(T, N)

    # Calculate last value of beta (base-case)
    for i in range(N):
        beta[T-1][i] = C[T-1]

    # Now we can calculate all steps down to 0 for beta (backwards)
    for t in range(T-2, -1, -1):
        for i in range(N):
            for j in range(N):
                beta[t][i] += A[i][j] * B[j][seq[t+1]] * beta[t+1][j]
            
            beta[t][i] = C[t]*beta[t][i]
    
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

    # Special case for last gamma element:
    for i in range(N):
        gamma[-1][i] = alpha[-1][i]


    return d_gamma, gamma


read = sys.stdin.read().split("\n")

A = readMatrix(read[0])
B = readMatrix(read[1])
pi = readMatrix(read[2])

N = len(A)
M = len(B[0])

# The sequence of emissions given
# seq = [int(x) for x in read[3].strip()[2:].split(" ")]
seq = [int(x) for x in read[3].strip().split(" ")[1:]]

T = len(seq)

maxIterations = 200
iterations = 0
oldLogProb = -float("inf")

# Run learning algorithm until max iterations is not reached
while True:

    # 1. Forward-pass: calculate  alpha
    alpha, C = calcAlpha(A, B, pi, seq)

    # 2. Backward-pass: calculate beta
    beta = calcBeta(A, B, C, pi, seq)
    # 3. Compute d-gamma
    d_gamma, gamma = calcGammas(A, B, seq, alpha, beta)

    # 4. Re-estimate pi:

    for i in range(N):
        pi[0][i] = gamma[0][i]

    # 5. Re-estimate A:
    for i in range(N):
        denominator = 0
        for t in range(T-1):
            denominator += gamma[t][i]
        for j in range(N):
            numerator = 0 
            for t in range(T-1):
                numerator+= d_gamma[t][i][j]

            A[i][j] = numerator / denominator

    # 6. Re-estimate B:
    for i in range(N):
        denominator = 0
        for t in range(T):
            denominator += gamma[t][i]

        for j in range(M):
            numerator = 0
            for t in range(T):
                if seq[t] == j:
                    numerator += gamma[t][i]
            
            B[i][j] = numerator / denominator

    # 7. Check if converged:
    logProb = 0

    for i in range(T):
        logProb += math.log(C[t])
    logProb = -logProb

    iterations += 1

    if  logProb - oldLogProb > 1e-5 and iterations < maxIterations:
        oldLogProb = logProb
    else:
        break


printMatrix(A)
printMatrix(B)
