"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random
import string
from random import Random
from typing import Any, Callable, Optional

from genyal.core import GenyalCore
from genyal.genotype import GeneFactory
from genyal.individuals import Individual
from genyal.operations.evolution import default_terminating_function, tournament_selection


class GenyalEngine(GenyalCore):
    __crossover_args: list[Any]
    __fitness_function: Callable[[list[Any]], float]
    __fittest: Optional[Individual]
    __generations: int
    __mutation_args: list[Any]
    __population: list[Individual]
    __selection_args: list[Any]
    __selection_strategy: Callable[..., Individual]
    __terminating_function: Callable[..., bool]

    def __init__(self, random_generator: Random = Random(),
                 fitness_function: Callable[..., float] = lambda _: 0,
                 selection_strategy=tournament_selection,
                 terminating_function=default_terminating_function):
        super(GenyalEngine, self).__init__(random_generator)
        self.__population = []
        self.__fitness_function = fitness_function
        self.__fittest = None
        self.__selection_strategy = selection_strategy
        self.__selection_args = []
        self.__crossover_args = []
        self.__mutation_args = []
        self.__terminating_function = terminating_function
        self.__generations = 0

    def create_population(self, population_size: int, individual_size: int,
                          gene_factory: GeneFactory, mutation_rate=0.01):
        """
        Creates a new population for the engine.
        The new population is then sorted according to the individual's fitness

        Args:
            mutation_rate:
            population_size:
                The number of individuals of the population.
            individual_size:
                The number of genes of each member.
            gene_factory:
                The factory to create the genes of each individual
        """
        self.__population = Individual.create(population_size, individual_size, gene_factory,
                                              mutation_rate)
        for member in self.__population:
            member.compute_fitness_using(self.__fitness_function)
        self.__population.sort()
        self.__fittest = self.__population[-1]

    def evolve(self, *args):
        """
        Evolves the population until the condition given by the terminating function is met.
        By default, the population will evolve until it reaches 100 generations.

        Args:
            *args:
                The arguments passed to the terminating function.
        """
        while not self.__terminating_function(self, *args):
            print(str(self.fittest.genes) if self.fittest is not None else "")
            new_population = []
            for _ in range(0, len(self.__population)):
                partner_a = self.__selection_strategy(self.__population, self._random_generator,
                                                      *self.__selection_args)
                partner_b = self.__selection_strategy(self.__population, self._random_generator,
                                                      *self.__selection_args)
                child = self.mutate(self.crossover(partner_a, partner_b, *self.__crossover_args),
                                    *self.__mutation_args)
                child.compute_fitness_using(self.__fitness_function)
                new_population.append(child)
            new_population.sort()
            self.__population = new_population
            self.__generations += 1

    def crossover(self, partner_a: Individual, partner_b: Individual, *args) -> Individual:
        partner_a.random_generator = self._random_generator
        return partner_a.crossover(partner_b, *args)

    def mutate(self, individual: Individual, *args) -> Individual:
        individual.random_generator = self.random_generator
        return individual.mutate(*args)

    @property
    def generation(self) -> int:
        return self.__generations

    @property
    def fittest(self):
        return self.__fittest


def fitness_function(genes) -> float:
    return sum([1 if genes[i] == "cat"[i] else 0 for i in range(0, 3)])


def terminating_function(engine, _):
    return engine.fittest.genes[0] == "c" and engine.fittest.genes[1] == "a" and \
           engine.fittest.genes[2] == "t"


if __name__ == '__main__':
    gene_factory = GeneFactory[str]()
    gene_factory.generator = lambda: random.choice(string.ascii_lowercase)
    engine = GenyalEngine(fitness_function=fitness_function,
                          terminating_function=terminating_function)
    engine.create_population(15, 3, gene_factory, 0.1)
    engine.evolve(5000)
    print(engine.fittest.genes)
