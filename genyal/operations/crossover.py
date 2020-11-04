"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""


def single_point_crossover(individual, partner, cut_point: int = -1):
    """
    Returns a new child from mixing this individual with another using a single-point crossover
    strategy.
    """
    from genyal.population import Individual
    if cut_point == -1:
        cut_point = individual.rng.randrange(0, len(individual.genes))
    child = Individual()
    child.rng = individual.rng
    crossover_genes = individual.genes[:cut_point] + partner.genes[cut_point:]
    child.genes = crossover_genes
    return child
