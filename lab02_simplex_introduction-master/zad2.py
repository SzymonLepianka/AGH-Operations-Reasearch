# 1. Import the library
from saport.simplex.model import Model
from saport.simplex.solver import Solver

# 2. Create a model
model = Model("zad2")

# 3. Add variables
p1 = model.create_variable("p1")
p2 = model.create_variable("p2")
p3 = model.create_variable("p3")
p4 = model.create_variable("p4")

# 4. FYI: You can create expression and evaluate them
# expr1 = 0.16 * x1 - 0.94 * x2 + 0.9 * x3
# print(f"Value of the expression for the specified assignment is  {expr1.evaluate([1, 1, 2])}\n")

# 5. Then add constraints to the model
model.add_constraint(0.8 * p1 + 2.4 * p2 + 0.9 * p3 + 0.4 * p4 >= 1200)
model.add_constraint(0.6 * p1 + 0.6 * p2 + 0.3 * p3 + 0.3 * p4 >= 600)

# 6. Set the objective!
model.minimize(9.6 * p1 + 14.4 * p2 + 10.8 * p3 + 7.2 * p4)

# 7. You can print the model
print("Before solving:")
print(model)

# 8. And finally solve it!
solution = model.solve(Solver())

# 9. Model is being simplified before being solver
# print("After solving:")
# print(model)

# 10. Print solution (uncomment after finishing assignment)
# print("Solution: ")
# print(solution)