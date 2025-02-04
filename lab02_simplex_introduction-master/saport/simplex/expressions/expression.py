from . import constraint as constr
from . import atom
from itertools import groupby
from functools import reduce
import numpy as np

class Expression:
    """
        A class to represent a linear polynomial in the linear programming, i.e. a sum of atom (e.g. 4x + 5y - 0.4z)

        Attributes
        ----------
        atoms : list[Atom]
            list of the atoms in the polynomial

        Methods
        -------
        __init__(*atoms : *Atom) -> Expression:
            constructs an expression with atoms given in the paremeter list
        evaluate(assignment: list[float]) -> float:
            returns value of the expression for the given assignment
            assignment is just a list of values with order corresponding to the variables in the model
        simplify() -> Expression:
            returns a new expression with sorted and atoms and reduced factors 
        __add__(other: Expression) -> Expression:
            returns sum of the two polynomials
        __sub__(other: Expression) -> Expression:
            returns sum of the two polynomials, inverting the first atom in the second polynomial
            useful for expressions like 3*x - 4y, otherwise one would have to write 3*x + -4*y 
        __eq__(bound: float) -> Constraint:
            returns a new equality constraint
        __le__(bound: float) -> Constraint:
            returns a new "less than or equal" constraint
        __ge__(bound: float) -> Constraint:
            returns a new "greater than or equal" constraint
    """

    def __init__(self, *atoms):
        self.atoms = atoms 

    def evaluate(self, assignment):
        adder = lambda val, a: val + a.evaluate(assignment[a.var.index])
        return reduce(adder, self.atoms, 0) 

    def simplify(self):
        projection = lambda a: a.var.index
        reduce_atoms = lambda a1, a2: atom.Atom(a1.var, a1.factor + a2.factor)
        reduce_group = lambda g: reduce(reduce_atoms, g[1:], g[0])
    
        sorted_atoms = sorted(self.atoms, key=projection)
        grouped_atoms = [list(g[1]) for g in groupby(sorted_atoms, key=projection)]
 
        new_atoms = (reduce_group(g) for g in grouped_atoms) 
        return Expression(*new_atoms)

    def __contains__(self, variable):
        projection = lambda a: a.var.name
        return variable.name in map(projection, self.atoms)

    def factor_vector(self, variables):
        projection = lambda a: a.var.index
        simplified = self.simplify()
        for var in variables:
            if var not in simplified:
                simplified += 0 * var
        return np.array([atom.factor for atom in sorted(simplified.atoms, key=projection)])

    def __iter__(self):
        return iter(self.atoms)

    def __add__(self, other):
        new_atoms = list(self.atoms)
        new_atoms += other.atoms;
        return Expression(*new_atoms)

    def __sub__(self, other):
        return self.__add__(other._invert())

    def _invert(self):
        new_atoms = list(self.atoms)
        first_atom = new_atoms[0] 
        inverted_first_atom = atom.Atom(first_atom.var, -first_atom.factor)
        new_atoms[0] = inverted_first_atom
        return Expression(*new_atoms)

    def __neg__(self):
        return Expression(*[-atom for atom in self.atoms])

    def __eq__(self, bound):
        return constr.Constraint(self, bound, constr.ConstraintType.EQ)
    
    def __ge__(self, bound):
        return constr.Constraint(self, bound, constr.ConstraintType.GE)

    def __le__(self, bound):
        return constr.Constraint(self, bound, constr.ConstraintType.LE)

    def __str__(self):
        text = str(self.atoms[0])
        for atom in self.atoms[1:]:
            text += ' + ' if atom.factor >= 0 else ' - '
            text += f'{abs(atom.factor)}*{atom.var.name}'
        return text