from saport.knapsack import model
from saport.integer.model import Model

m = Model("Sense of Life")

dania = ["moules_mariniers", "pate_de_foie_gras", "beluga_caivar", "egg_benedictine", "water-thin_mint", "salmon_mousse"]
x_i = [m.create_variable(d) for d in dania]

cost_constraint = 2.15 * x_i[0] + 2.75 * x_i[1] + 3.35 * x_i[2] + 3.55 * x_i[3] + 4.20 * x_i[4] + 5.8*x_i[5] <= 50
m.add_constraint(cost_constraint)
dishes_amount = [5, 6, 7, 5, 1, 1]
for x, amount in zip(x_i, dishes_amount):
    m.add_constraint(x <= amount)

objective = 3.0 * x_i[0] + 4.0 * x_i[1] + 4.5 * x_i[2] + 4.65 * x_i[3] + 8.0 * x_i[4] + 9.0 * x_i[5]
m.maximize(objective)
solution = m.solve()
print(m)
print(solution)
