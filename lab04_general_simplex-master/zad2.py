from saport.simplex.model import Model

model = Model("zadanie 2")

x1 = model.create_variable("x1")
x2 = model.create_variable("x2")
x3 = model.create_variable("x3")
x4 = model.create_variable("x4")

model.add_constraint(0.8 * x1 + 2.4 * x2 + 0.9 * x3 + 0.4 * x4 >= 1200)
model.add_constraint(0.6 * x1 + 0.6 * x2 + 0.3 * x3 + 0.3 * x4 >= 600)

model.minimize(9.6 * x1 + 14.4 * x2 + 10.8 * x3 + 7.2 * x4)

solution = model.solve()
print(solution)
