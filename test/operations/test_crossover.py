"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random
import string
import sys
import unittest
from typing import Tuple

import pytest

from genyal.genotype import GeneFactory
from genyal.individuals import Individual
from genyal.operations.crossover import CrossoverError, single_point_crossover


@pytest.mark.repeat(16)
def test_not_matching_couples(ascii_gene_factory: GeneFactory[str],
                              random_generator: random.Random, seed: int):
    individual = Individual(gene_factory=ascii_gene_factory, random_generator=random_generator)
    individual.set(number_of_genes=random_generator.randint(1, 32))

    unmatching_size = random_generator.randint(1, 32)
    while len(individual) == unmatching_size:
        unmatching_size = random_generator.randint(1, 32)
    erroneous_individual = Individual(gene_factory=ascii_gene_factory,
                                      random_generator=random_generator)
    erroneous_individual.set(unmatching_size)
    with pytest.raises(CrossoverError) as error:
        single_point_crossover(individual, erroneous_individual)
        assert unmatching_error_msg(len(individual), len(
            erroneous_individual)) in error.value.cause, f"Test failed with seed: {seed}"


def test_random_picked_single_point_crossover(couple: Tuple[Individual, Individual], seed: int):
    expected_cut_point = random.Random(seed)
    couple[0].random_generator = random.Random(seed)
    offspring = single_point_crossover(couple[0], couple[1])
    assert False


@pytest.fixture
def couple(ascii_gene_factory: GeneFactory[str], random_generator: random.Random) \
        -> Tuple[Individual, Individual]:
    """A pair of individuals"""
    couple = (Individual(gene_factory=ascii_gene_factory, random_generator=random_generator),
              Individual(gene_factory=ascii_gene_factory, random_generator=random_generator))
    number_of_genes = random_generator.randint(1, 64)
    couple[0].set(number_of_genes)
    couple[1].set(number_of_genes)
    return couple


@pytest.fixture
def ascii_gene_factory(random_generator: random.Random) -> GeneFactory[str]:
    factory = GeneFactory[str]()
    factory.generator = lambda: random_generator.choice(string.ascii_lowercase)
    return factory


@pytest.fixture()
def random_generator(seed: int) -> random.Random:
    """The random number generator used in the tests."""
    return random.Random(seed)


@pytest.fixture
def seed() -> int:
    """The seed used by the tests."""
    return random.randint(-sys.maxsize, sys.maxsize)


def unmatching_error_msg(size_1: int, size_2) -> str:
    return f"Can't perform a crossover over individuals of different sizes. {size_1} != {size_2}."


if __name__ == '__main__':
    unittest.main()
