import logging
from saport.simplex.model import Model


def run():
    # fill missing test based on the example_01_solvable.py
    # to make the test a bit more interesting:
    # * make the solver use artificial variables!
    model = Model("example_04")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")

    model.add_constraint(2 * x1 - x2 <= -2)
    model.add_constraint(x1 + x2 == 5)

    model.maximize(x1 + 3 * x2)

    try:
        solution = model.solve()
    except:
        raise AssertionError(
            "This problem has a solution and your algorithm hasn't found it!")

    logging.info(solution)
    assert (solution.assignment == [0.0, 5.0]), "Your algorithm found an incorrect solution!"
    logging.info("Congratulations! This solution seems to be alright :)")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
