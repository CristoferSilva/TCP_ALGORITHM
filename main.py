from pulp import *
import numpy as np

graph = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

vertexLength = graph.__len__()
edges = [(i, j) for i in range(vertexLength) for j in range(vertexLength) if graph[i][j] != 0]

print(vertexLength)
print(edges)

# inicializando o problema
# Colocamos LpMinimize porque queremos dizer que é um problema de minimização para a bilbioteca.

tsp = LpProblem("Caixeiro_Viajante", LpMinimize)

# Variáveis de decisão (dicionários)

# x é binário, se o arco está no caminho do caixeiro -> true, caso contrário -> false.
x = LpVariable.dicts("x", edges, cat="Binary")
# u é continua, contém indices mapeados para os vértices.
u = LpVariable.dicts("u", [i for i in range(vertexLength)], lowBound=1, upBound=vertexLength, cat="Continuos")

# Restrições de i e j que não permite que o caixeiro fique "preso" em um único caminho.
for j in range(vertexLength):
    tsp += lpSum([x[i, j] for (i, m) in edges if m == j]) == 1

for i in range(vertexLength):
    tsp += lpSum([x[i, j] for (m, j) in edges if m == i]) == 1

# Restrição que permite que o caixeiro percorra apenas rotas contínuas
for (i, j) in edges:
    if i > 0 and i != j:
        tsp += u[i] - u[j] + vertexLength * x[i, j] <= vertexLength - 1

solveModel = tsp.solve()
print(f"Status do Problema: {LpStatus[solveModel]}")

# Display variaveis
for var in tsp.variables():
    if type(var.varValue) is not type(None):
        if var.varValue > 0:
            print(f"{var.name} = {var.varValue}")