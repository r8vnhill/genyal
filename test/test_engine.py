import string
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
    population_size = random_generator.randint(1, 300)
    individual_size = random_generator.randint(1, 100)
    basic_engine.create_population(population_size, individual_size, gene_factory=factory)
    assert basic_engine.fittest is not None
    assert len(basic_engine.population) == population_size
    for individual in basic_engine.population:
        assert len(individual) == individual_size
        assert individual.fitness == 0


@pytest.mark.repeat(32)
def test_word_match_engine(match_word_engine: GenyalEngine, population_size: int,
                           ascii_gene_factory: GeneFactory[str], random_word: str,
                           mutation_rate: float, random_generator: Random, seed: int) -> None:
    ascii_gene_factory.generator_args = (random_generator,)
    match_word_engine.fitness_function_args = (random_word,)
    match_word_engine.create_population(population_size, len(random_word), ascii_gene_factory,
                                        mutation_rate)
    match_word_engine.evolve(random_word)
    assert "".join(match_word_engine.fittest.genes) == random_word, f"Test failed with seed: {seed}"


@pytest.fixture
def match_word_engine(random_generator: Random) -> GenyalEngine:
    return GenyalEngine(random_generator, match_word_fitness, terminating_function=exact_match)


@pytest.fixture()
def ascii_gene_factory() -> GeneFactory[str]:
    return GeneFactory(generator=lambda r: r.choice(string.ascii_lowercase))


@pytest.fixture()
def random_word(random_generator: Random) -> str:
    word = ""
    for _ in range(0, random_generator.randint(3, 5)):
        word += random_generator.choice(string.ascii_lowercase)
    return word


@pytest.fixture()
def population_size(random_generator: Random) -> int:
    return random_generator.randint(4, 64)


@pytest.fixture()
def mutation_rate(random_generator: Random) -> float:
    return random_generator.random()


@pytest.fixture()
def random_generator(seed: int) -> Random:
    return Random(seed)


@pytest.fixture()
def seed() -> int:
    return randrange(-sys.maxsize, sys.maxsize)


if __name__ == '__main__':
    unittest.main()
