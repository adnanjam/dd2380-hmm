# Assignment 1

## Question 1

The initial probabilities are given by $\pi$
$\pi = [0.5 \ 0.5]$

The transition matrix is given by $A$.

$A = \begin{bmatrix} 0.5 & 0.5\\ 0.5 & 0.5 \end{bmatrix}$

Since the probability of selecting any coin is 0.5 it is the same regardless of which state we are already in.

The Observation probability matrix, $B$ is given below:

$B = \begin{bmatrix} 0.9 & 0.1\\ 0.5 & 0.5 \end{bmatrix}$
For coin **$c_2$**, the probability of head and tails is equally distributed, while for **$c_1$** it is not.

## Question 2 & 3

The output of multiplying the state transition matrix with the initial state matrix is the following row vector: $res = [0.2 \ 0.3 \ 0.0 \ 0.5]$. By multiplying this result with the observation matrix, we get the following result: $dist = [0 \ 0.3 \ 0.6 \ 0.1]$

<!-- The vector represents the probability of the different emissions ("seeing" given observation) in the next state. -->

## Question 4

We have substituted $\bold{O}_{1:t} = \bold{o}_{1:t}$ with $\bold{O}_{t} = \bold{o}_{t} $ when we condition on the state $\bold{X_t}= \bold{x_i}$ because we used the markovian property, i.e. the state at a time step is only dependant on the previous state (for a first order HMM).
