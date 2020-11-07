import sys
import unittest
from random import Random, random, randrange

import pytest

from genyal.engine import GenyalEngine
from genyal.genotype import GeneFactory


def match_word_fitness(predicted: list[str], target: str) -> float:
    return sum([predicted[i] == target[i] for i in range(0, len(target))])


def exact_match(engine: GenyalEngine, target: str) -> bool:
    return "".join(engine.fittest.genes) == target


@pytest.mark.repeat(16)
def test_basic_engine(seed: int) -> None:
    basic_engine = GenyalEngine()
    assert basic_engine.fittest is None
    assert basic_engine.generation == 0
    assert len(basic_engine.crossover_args) == 0
    factory = GeneFactory()
    factory.generator = lambda: random()
    random_generator = Random(seed)
    population_size = random_generator.randint(0, 300)
    individual_size = random_generator.randint(0, 100)
    basic_engine.create_population(population_size, individual_size, gene_factory=factory)
    assert basic_engine.fittest is not None
    assert len(basic_engine.population) == population_size
    for individual in basic_engine.population:
        assert len(individual) == individual_size
        assert individual.fitness == 0


def test_word_match_engine(match_word_engine: GenyalEngine) -> None:
    pass


@pytest.fixture
def match_word_engine(random_generator: Random) -> GenyalEngine:
    return GenyalEngine(random_generator, match_word_fitness, terminating_function=exact_match)


@pytest.fixture()
def random_generator(seed: int) -> Random:
    return Random(seed)


@pytest.fixture()
def seed() -> int:
    return randrange(-sys.maxsize, sys.maxsize)


if __name__ == '__main__':
    unittest.main()
