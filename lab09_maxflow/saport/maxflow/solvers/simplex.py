from .solver import AbstractSolver
from ...simplex.model import Model as LinearModel
from ...simplex.expressions.expression import Expression as LinearExpression
from ..model import Network


def _get_edge_variables_sum(node: int, get_edges):
    expression = LinearExpression()
    for _, _, data in get_edges(node, data=True):
        expression += data[SimplexSolver.var_attr_name]
    return expression


class SimplexSolver(AbstractSolver):
    var_attr_name = 'variable'

    def solve(self) -> int:
        m = LinearModel(self.network.name)
        self._create_variables(m)
        self._set_flow_constraints(m)
        solution = m.solve()
        return int(solution.objective_value())

    def _create_variables(self, model: LinearModel):
        digraph = self.network.digraph
        for i, edge in enumerate(digraph.edges):
            start, end = edge
            x = model.create_variable(f'x{i}')
            c = Network.capacity(digraph, start, end)
            model.add_constraint(x <= c)
            Network.set_attribute(digraph, start, end, SimplexSolver.var_attr_name, x)

    def _set_flow_constraints(self, model: LinearModel):
        digraph = self.network.digraph
        from_source = _get_edge_variables_sum(self.network.source_node, digraph.out_edges)
        to_sink = _get_edge_variables_sum(self.network.sink_node, digraph.in_edges)
        model.add_constraint(from_source + -1 * to_sink == 0)
        for node in digraph.nodes:
            incoming_sum = _get_edge_variables_sum(node, digraph.in_edges)
            outgoing_sum = _get_edge_variables_sum(node, digraph.out_edges)
            if node in [self.network.source_node, self.network.sink_node]:
                if node == self.network.source_node: model.maximize(outgoing_sum)
                continue
            model.add_constraint(incoming_sum + -1 * outgoing_sum == 0)
