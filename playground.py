import random
import string

from genyal.engine import GenyalEngine
from genyal.genotype import GeneFactory


def random_char():
    return random.choice(string.ascii_lowercase)


gene_factory = GeneFactory[str]()
gene_factory.generator = random_char


# This is how the engine will select the fittest individuals
def fitness_fun(word: list[str]) -> float:
    return sum([word[i] == "owo"[i] for i in range(0, 3)])


# This is the condition to stop the evolution
def target(genyal_engine: GenyalEngine) -> bool:
    return "".join(genyal_engine.fittest.genes) == "owo"


if __name__ == '__main__':
    engine = GenyalEngine(fitness_function=fitness_fun, terminating_function=target)
    # We create an initial population of 16 words (Individuals) of 3 characters (genes)
    # using our previously defined gene factory.
    engine.create_population(16, 3, gene_factory)
    engine.evolve()
    print(engine.evolution_logs)
