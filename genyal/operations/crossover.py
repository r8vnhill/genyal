"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from copy import copy


def single_point_crossover(individual, partner, cut_point: int = -1):
    """
    Returns a new child from mixing two individuals using a single-point crossover strategy.
    By default the cut point is selected at random.
    """
    if cut_point == -1:
        cut_point = individual.random_generator.randrange(0, len(individual.genes))
    child = copy(individual)
    child.random_generator = individual.random_generator
    crossover_genes = individual.genes[:cut_point] + partner.genes[cut_point:]
    child.genes = crossover_genes
    return child
