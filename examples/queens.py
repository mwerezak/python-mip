from mip.model import *
from sys import stdout, argv
from time import process_time

n = 10

# can force a solver to be used with -solver=solverName option
solver = CBC

for arg in argv:
    if "-solver=" in arg:
        solver = arg.split('=')[1]
        print('trying to load {} solver'.format(solver))

if not solver:
    queens = Model('queens', MAXIMIZE)
else:
    queens = Model('queens', MAXIMIZE, solver)

x = [[queens.add_var('x({},{})'.format(i, j), var_type='B')
      for j in range(n)] for i in range(n)]

# objective function
queens += xsum(x[i][j] for i in range(n) for j in range(n))

# one per row
for i in range(n):
    queens += xsum(x[i][j] for j in range(n)) == 1, 'row({})'.format(i)

# one per column
for j in range(n):
    queens += xsum(x[i][j] for i in range(n)) == 1, 'col({})'.format(j)

# diagonal \
for p, k in enumerate(range(2 - n, n - 2 + 1)):
    queens += xsum(x[i][j] for i in range(n) for j in range(n) if i - j == k) <= 1, 'diag1({})'.format(p)

# diagonal /
for p, k in enumerate(range(3, n + n)):
    queens += xsum(x[i][j] for i in range(n) for j in range(n) if i + j == k) <= 1, 'diag2({})'.format(p)

queens.read('queens.lp')
queens.optimize()

stdout.write('\n')
for i, v in enumerate(queens.vars):
    if v.x >= 0.98:
        stdout.write('O ')
    else:
        stdout.write('. ')

    if i % n == n-1:
        stdout.write('\n')
stdout.write('\n')

stdout.write('Total process time: {:.3f}s\n'.format(process_time()))
