"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""

from copy import copy


def simple_mutation(original_individual, _):
    """
    Returns a new individual resulting from mutating the original with a given mutation rate.
    The second argument is a placeholder.
    """
    new_individual = copy(original_individual)
    new_individual.genes = [
        gene if new_individual.random_generator.random() <= new_individual.mutation_rate
        else new_individual.gene_factory.make(new_individual.random_generator)
        for gene in new_individual.genes]
    return new_individual
