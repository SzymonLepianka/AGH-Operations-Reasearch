import logging
from saport.simplex.model import Model


def run():
    model = Model("example_02_solvable")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")

    model.add_constraint(x1 + 2 * x2 + x3 >= -100)
    model.add_constraint(2 * x1 + x2 + 3 * x3 >= -200)
    model.add_constraint(x1 + 2 * x2 + 4 * x3 <= 300)

    model.minimize(9 * x1 + 9 * x2 + 7 * x3)

    try:
        solution = model.solve()
    except:
        raise AssertionError(
            "This problem has a solution and your algorithm hasn't found it!")

    logging.info(solution)

    assert (solution.assignment == [0.0, 0.0, 0.0, 100.0, 200.0, 300.0]), "Your algorithm found an incorrect solution!"

    logging.info("Congratulations! This solution seems to be alright!")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
