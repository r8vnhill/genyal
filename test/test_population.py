"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import string
import unittest
from random import Random

from genyal.genotype import GeneFactory
from genyal.population import Individual


def test_creation_with_characters():
    rng = Random(8000)
    gene_factory = GeneFactory[str]()
    gene_factory.generator = lambda: rng.choice(string.ascii_lowercase)
    individuals = Individual.create(number_of_individual=100, number_of_genes=10,
                                    gene_factory=gene_factory)
    assert len(individuals) == 100
    for individual in individuals:
        assert len(individual.genes) == 10
        for gene in individual.genes:
            assert gene in string.ascii_lowercase


if __name__ == '__main__':
    unittest.main()
