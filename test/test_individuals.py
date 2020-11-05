"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random
import string
import unittest
from random import Random
from typing import List, Tuple

import pytest

from genyal.genotype import GeneFactory
from genyal.individuals import Individual


def test_creation_with_characters(str_gene_factory: GeneFactory[str]):
    individuals = Individual.create(number_of_individuals=100, number_of_genes=10,
                                    gene_factory=str_gene_factory)
    assert len(individuals) == 100
    for individual in individuals:
        assert len(individual.genes) == 10
        for gene in individual.genes:
            assert gene in string.ascii_lowercase


def test_word_guess(str_gene_factory: GeneFactory[str]):
    individuals = Individual.create(number_of_individuals=100000, number_of_genes=3,
                                    gene_factory=str_gene_factory)

    def fitness_function(word: List[str]) -> float:
        return sum([1 if word[i] == "cat"[i] else 0 for i in range(0, 3)])

    fittest_individual = individuals[0]
    for individual in individuals:
        individual.compute_fitness_using(fitness_function)
        if individual.fitness > fittest_individual.fitness:
            fittest_individual = individual
    assert fittest_individual.fitness == 3


def test_crossover(couple: Tuple[Individual, Individual]):
    """"""
    assert couple[0].crossover(couple[1], 2).genes == list("abfg")
    assert couple[0].crossover(couple[1], 1).genes == list("aefg")
    assert couple[0].crossover(couple[1], 0).genes == list("defg")


def test_mutation():
    gene_factory = GeneFactory[str]()
    gene_factory.generator = lambda: Random(8000).choice(string.ascii_lowercase)
    individual = Individual()
    individual.random_generator = Random(8000)
    individual.genes = "abcd"
    individual.gene_factory = gene_factory
    individual.mutation_rate = 0.5
    mutated_i = individual.mutate()
    assert mutated_i.genes == list("sbsd")


@pytest.fixture()
def couple() -> Tuple[Individual, Individual]:
    c = (Individual(), Individual())
    c[0].genes = "abcd"
    c[1].genes = "defg"
    return c


@pytest.fixture()
def str_gene_factory(rng: Random) -> GeneFactory[str]:
    gene_factory = GeneFactory()
    gene_factory.generator = lambda: rng.choice(string.ascii_lowercase)
    return gene_factory


@pytest.fixture
def rng(seed: int) -> Random:
    return Random(seed)


@pytest.fixture
def seed() -> int:
    return random.randint(-8000, 8000)


if __name__ == '__main__':
    unittest.main()
