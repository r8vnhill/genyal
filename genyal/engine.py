"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from random import Random
from typing import Any, Callable, Optional, Tuple

from genyal.core import GenyalCore
from genyal.genotype import GeneFactory
from genyal.individuals import Individual
from genyal.operations.evolution import default_terminating_function, tournament_selection


class GenyalEngine(GenyalCore):
    """
    The engine is the main component of Genyal.
    This class is in charge of creating, maintaining and evolving a population.
    """
    __crossover_args: Tuple
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
        """
        Initializes the values of the engine.

        Args:
            random_generator:
                The random number generator used by the engine.
            fitness_function:
                The function to calculate the fitness of the population's individuals.
                If none given, the default function returns 0 for any individual.
            selection_strategy:
                The strategy to select the individuals that will participate in the crossover.
            terminating_function:
                The function that will decide when to stop the evolution.
        """
        super(GenyalEngine, self).__init__(random_generator)
        self.__population = []
        self.__fitness_function = fitness_function
        self.__fittest = None
        self.__selection_strategy = selection_strategy
        self.__selection_args = []
        self.__crossover_args = ()
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
            new_population = []
            for _ in range(0, int(0.75 * len(self.__population))):
                child = self.__create_offspring()
                new_population.append(child)
            for i in range(int(0.75 * len(self.__population)), len(self.__population)):
                new_population.append(self.__population[i])
            new_population.sort()
            self.__population = new_population
            self.__fittest = new_population[-1]
            self.__generations += 1

    def crossover(self, partner_a: Individual, partner_b: Individual, *args) -> Individual:
        """Performs a crossover between two individuals and returns the offspring."""
        partner_a.random_generator = self._random_generator
        return partner_a.crossover(partner_b, *args)

    def mutate(self, individual: Individual, *args) -> Individual:
        """Mutates an individual and returns the result of the mutation."""
        individual.random_generator = self.random_generator
        return individual.mutate(*args)

    def __create_offspring(self):
        """
        Creates an offspring from a couple.
        The partners are selected from the population and the offspring is obtained via crossover
        and mutation.
        """
        partner_a = self.__selection_strategy(self.__population, self._random_generator,
                                              *self.__selection_args)
        partner_b = self.__selection_strategy(self.__population, self._random_generator,
                                              *self.__selection_args)
        child = self.mutate(self.crossover(partner_a, partner_b, *self.__crossover_args),
                            *self.__mutation_args)
        child.compute_fitness_using(self.__fitness_function)
        return child

    @property
    def generation(self) -> int:
        """The number of generations the population has evolved."""
        return self.__generations

    @property
    def fittest(self):
        """The individual with the greatest fitness from the population"""
        return self.__fittest

    @property
    def crossover_args(self) -> Tuple:
        """A tuple with extra arguments to be passed to the crossover operation."""
        return self.__crossover_args

    @crossover_args.setter
    def crossover_args(self, args):
        """Sets the arguments needed by the crossover operation."""
        self.__crossover_args = args
