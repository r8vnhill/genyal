"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from enum import Enum
from random import Random
from time import time
from typing import Any, Callable, List, Optional, Tuple

import pandas

from genyal.core import GenyalCore
from genyal.genotype import GeneFactory
from genyal.individuals import Individual
from genyal.operations.evolution import default_terminating_function, tournament_selection


class Logs(str, Enum):
    FITTEST = "FITTEST"
    BEST_FITNESS = "BEST_FITNESS"
    AVG_FITNESS = "AVG_FITNESS"
    WORST_FITNESS = "WORST_FITNESS"
    GENERATION = "GENERATION"
    DELTA_T = "DELTA_T"


class GenyalEngine(GenyalCore):
    """
    The engine is the main component of Genyal.
    This class is in charge of creating, maintaining and evolving a population.
    """
    __fitness_function_args: Tuple
    __factory_generator_args: Tuple
    __crossover_args: Tuple
    __fitness_function: Callable[[List[Any]], float]
    __fittest: Optional[Individual]
    __generations: int
    __mutation_args: List[Any]
    __population: List[Individual]
    __selection_args: List[Any]
    __selection_strategy: Callable[..., Individual]
    __terminating_function: Callable[..., bool]
    __evolution_logs: pandas.DataFrame

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
        self.__fitness_function_args = ()
        self.__fittest = None
        self.__selection_strategy = selection_strategy
        self.__selection_args = []
        self.__crossover_args = ()
        self.__mutation_args = []
        self.__terminating_function = terminating_function
        self.__generations = 0
        self.__factory_generator_args = ()
        self.__evolution_logs = pandas.DataFrame(
            columns=[Logs.FITTEST, Logs.AVG_FITNESS, Logs.BEST_FITNESS, Logs.WORST_FITNESS,
                     Logs.GENERATION, Logs.DELTA_T])

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
                                              mutation_rate, *self.__factory_generator_args)
        for member in self.__population:
            member.compute_fitness_using(self.__fitness_function, *self.__fitness_function_args)
        self.__population.sort()
        self.__fittest = self.__population[-1]

    def evolve(self, logging: bool = False, *args):
        """
        Evolves the population until the condition given by the terminating function is met.
        By default, the population will evolve until it reaches 100 generations.

        Args:
            logging:
                if true the information of each generation is going to be stored on a data frame.
            *args:
                The arguments passed to the terminating function.
        """
        while not self.__terminating_function(self, *args):
            start = time()
            new_population = []
            cum_fitness = 0
            for _ in range(0, len(self.__population)):
                child = self.__create_offspring()
                cum_fitness += child.fitness
                new_population.append(child)
            new_population.sort()
            self.__population = new_population
            self.__fittest = new_population[-1]
            self.__generations += 1
            if logging:
                dt = time() - start
                self.__evolution_logs = self.__evolution_logs.append(
                    { Logs.FITTEST: str(self.__fittest), Logs.BEST_FITNESS: self.__fittest.fitness,
                      Logs.AVG_FITNESS: cum_fitness / len(new_population),
                      Logs.WORST_FITNESS: new_population[0].fitness,
                      Logs.GENERATION: self.__generations, Logs.DELTA_T: dt }, ignore_index=True)

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
                            self._random_generator,
                            *self.__mutation_args)
        child.compute_fitness_using(self.__fitness_function, *self.__fitness_function_args)
        return child

    @property
    def population(self) -> List[Individual]:
        """The individuals of the current generation."""
        return self.__population

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

    @property
    def factory_generator_args(self) -> Tuple:
        return self.__factory_generator_args

    @factory_generator_args.setter
    def factory_generator_args(self, args: Tuple) -> None:
        self.__factory_generator_args = args

    @property
    def fitness_function_args(self) -> Tuple:
        return self.__fitness_function_args

    @fitness_function_args.setter
    def fitness_function_args(self, args: Tuple) -> None:
        self.__fitness_function_args = args

    @property
    def evolution_logs(self) -> pandas.DataFrame:
        return self.__evolution_logs
