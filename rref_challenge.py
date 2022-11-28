import numpy as np


def gaussJordan(a):
    rrefMatrix = np.array(a, float)
    numRows = len(rrefMatrix)
    numCols = len(rrefMatrix[0])

    # main loop
    for k in range(numRows):
        e = 0

        if k < numCols:
            if np.fabs(rrefMatrix[k,k]) < 1e-12:
                for i in range(k+1, numRows):
                    if np.fabs(rrefMatrix[i,k]) > np.fabs(rrefMatrix[k,k]):
                        for j in range(k,numCols):
                            rrefMatrix[k, j], rrefMatrix[i, j] = rrefMatrix[i, j], rrefMatrix[k, j]
                        break

            # division of the pivot row
            pivot = rrefMatrix[k][k]
            if pivot == 0:
                e = k
                while e < numCols and rrefMatrix[k][e] == 0:
                    e += 1

                if e < numCols: pivot = rrefMatrix[k][e]
                else: return rrefMatrix

            for j in range(k, numCols):
                rrefMatrix[k][j] /= pivot

            # elimination loop
            for i in range(numRows):
                if i == k or rrefMatrix[i, k] == 0: continue
                factor = rrefMatrix[i, k]

                if e != 0: factor = rrefMatrix[i][e]

                for j in range(k,numCols):
                    rrefMatrix[i, j]-= factor * rrefMatrix[k, j]

    return rrefMatrix

#a = ["2","4","8","<>","6","12","14"]
a = ["2","2","4","<>","1","1","8","<>","7","6","5"]
matrix = []
row = []

for element in a:
    if element == "<>":
        matrix.append(row)
        row = []
    else:
        row.append(int(element))

matrix.append(row)
print(matrix)
print(gaussJordan(matrix))

#Test cases
test_cases = [[[0,2,0,1],[2,2,3,2],[4,-3,0,1],[6,1,-6,-5]],
              [[0,1,5],[1,4,3],[2,7,1]],
              [[2,4,8], [6,12,14]],
              [[-1, 1, 0, 1], [-2, -3, -1, -2],[-3, -1, -2, -1]],
              [[2,2,4],[1,1,8],[7,6,5]],
              [[1,3,2,1],[2,-3,0,-2]],
              [[-1,1],[-1,0],[0,-1],[-1,-2]],
              [[-1,-3],[3,-3],[-3,-3],[2,0]],
              [[3,-2,-3,3],[2,3,3,2]],
              [[1,-2,-3],[-2,3,-1]],
              [[0,-3,1,-1],[-2,1,0,3]]]

for test_case in test_cases:
    print("Matrix: ", test_case, "\nSolution: \n", gaussJordan(test_case), "\n")



