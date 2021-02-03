import logging
from saport.simplex.model import Model
from saport.simplex.solver import PositiveArtificialVariablesError


def run():

    # fill missing test based on the example_01_solvable.py
    # to make the test a bit more interesting:
    # * make the model unfeasible in a way detectable by the 2-phase simplex
    # 
    model = Model("example_05_unfeasible")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")

    model.maximize(x1)
    model.add_constraint(x1 + x2 == 150)
    model.add_constraint(x1 - x2 >= 250)

    try:
        solution = model.solve()
    except PositiveArtificialVariablesError:
        logging.info("Congratulations! You found an unfeasible solution detectable with artificial variables :)")
    else:
        raise AssertionError("This problem has no solution but your algorithm hasn't figured it out!")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
