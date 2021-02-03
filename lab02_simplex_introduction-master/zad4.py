from saport.simplex.solver import Solver
from saport.simplex.model import Model
from saport.simplex.expressions.expression import Expression

model = Model("zadanie 4")

x_i = [model.create_variable(f'x{i}') for i in range(14)]
# constraints
model.add_constraint(x_i[0] + x_i[1] + x_i[2] + x_i[3] >= 150)
model.add_constraint(x_i[1] + x_i[4] + x_i[5] + x_i[6] + x_i[7] + 2 * x_i[8] + 2 * x_i[9] >= 200)
model.add_constraint(x_i[2] + 2 * x_i[3] + x_i[5] + 2*x_i[6] + 3*x_i[7] + 1*x_i[9] + 2 * x_i[10] + 3*x_i[11] + 4*x_i[12] + 5*x_i[13] >= 150)

model.minimize(sum(x_i, start=Expression()))

model.solve(Solver())
