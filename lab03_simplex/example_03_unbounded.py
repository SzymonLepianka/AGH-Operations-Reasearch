import logging
from saport.simplex.solver import UnboundeLinearProgramException
from saport.simplex.model import Model


def run():
    model = Model("example_03_unbounded")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")

    model.add_constraint(x1 + x2 >= -100)
    model.add_constraint(x1 - 2 * x3 >= -200)
    model.add_constraint(5 * x2 + 3 * x3 >= -300)

    model.maximize(9 * x1 + 9 * x2 + 7 * x3)

    try:
        solution = model.solve()
    except UnboundeLinearProgramException:
        logging.info("Congratulations! You found an infeasible solution!")
    else:
        raise AssertionError("This problem has no solution but your algorithm hasn't figured it out!")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
