"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""


def simple_mutation(original_individual, _=None):
    """
    Returns a new individual resulting from mutating the original with a given mutation rate.
    The second argument is a placeholder.
    """
    from genyal.population import Individual
    new_individual = Individual()
    new_individual.rng = original_individual.rng
    new_individual.genes = [original_individual.genes[i]
                            if new_individual.rng.random() <= new_individual.mutation_rate
                            else new_individual.gene_factory.make()
                            for i in range(0, len(original_individual.genes))]
    return new_individual
