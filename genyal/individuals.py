"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""

from copy import copy
from random import Random
from typing import Any, Callable, Generic, List, Optional, Tuple, get_args

from genyal.core.commons import DNA, GeneticsError, GenyalCore
from genyal.genotype import GeneFactory
from genyal.operations.crossover import single_point_crossover
from genyal.operations.mutation import simple_mutation


class Individual(GenyalCore, Generic[DNA]):
    """
    Individuals are the basic members of a population.
    On the context of the genetic algorithm engine, a population is a list of individuals from which
    it should be able to pick the fittest one.

    Every individual must have a way to perform a crossover with a partner to give birth to a new
    child; and to mutate according to a given mutation rate.

    Most of the handling process of the individuals will be done by the engine (see:
    genyal.engine.GenyalEngine).
    """
    __factory_args: Tuple
    __fitness: Optional[float]
    __genes: List[DNA]
    __gene_factory: GeneFactory[DNA]
    __mutation_rate: float
    __crossover_strategy: Callable[..., 'Individual[DNA]']
    __mutation_strategy: Callable[..., 'Individual[DNA]']

    def __init__(self, genes=None, mutation_rate=0.01, gene_factory=GeneFactory(),
                 crossover_strategy=single_point_crossover, mutation_strategy=simple_mutation,
                 random_generator=Random()):
        """
        Initializes an individual.
        If no parameters are given to the constructor the individual is created with default
        parameters.

        Args:
            genes:
                A sequence representing the genes of this individual.
                This value defaults to an empty list.
                Genes can be any type of sequence that can be accessed by its index; e.g.,
                strings, lists.
            mutation_rate:
                The probability used by the mutation function to generate a new individual.
            gene_factory:
                A factory to produce the genes of this individual using a generator function (refer
                to: genyal.genotype.GeneFactory).
            crossover_strategy:
                The function to perform the crossover operation.
                Defaults to single_point_crossover (see: genyal.operations.crossover).
            mutation_strategy:
                The function to perform the mutation operation.
                Defaults to simple_mutation (see: genyal.operations.mutation).
            random_generator:
                The random number generator used in the algorithm's operations.
        """
        super(Individual, self).__init__(random_generator)
        self.__fitness = None
        self.__genes = genes if genes is not None else []
        self.__mutation_rate = mutation_rate
        self.__crossover_strategy = crossover_strategy
        self.__mutation_strategy = mutation_strategy
        self.__gene_factory = gene_factory
        self.__factory_args = ()

    @classmethod
    def create(cls, number_of_individuals: int, number_of_genes: int,
               gene_factory: GeneFactory[DNA], mutation_rate: float = 0.01, *args) \
            -> List['Individual[DNA]']:
        """
        Factory method to easily create a population of individuals.

        Args:
            number_of_individuals:
                number of individuals to return.
            number_of_genes:
                the number of genes each individual should have.
            gene_factory:
                a one-argument factory to generate a gene.
            mutation_rate:
                the probability —a number in [0, 1)—  with which an individual will mutate.
        """
        individuals = []
        for _ in range(0, number_of_individuals):
            individual = Individual(gene_factory=gene_factory, mutation_rate=mutation_rate)
            individual.set(number_of_genes, *args)
            individuals.append(individual)
        return individuals

    def compute_fitness_using(self, fitness_function: Callable[..., float], *args):
        """Computes this individual's fitness if it hasn't been computed yet."""
        if not self.__genes:
            raise GeneticsError("The individual should have genes.")
        if self.__fitness is None:
            self.__fitness = fitness_function(self.__genes, *args)

    def set(self, number_of_genes: int, *args):
        """Generate the genes of the individual."""
        self.__factory_args = args
        for _ in range(0, number_of_genes):
            self.__genes.append(self.__gene_factory.make())

    def crossover(self, partner: 'Individual[DNA]', *args):
        return self.__crossover_strategy(self, partner, *args)

    def mutate(self, *args) -> 'Individual[DNA]':
        return self.__mutation_strategy(self, *args)

    # region : Properties
    @property
    def fitness(self) -> float:
        """The fitness of this individual according to its fitness function."""
        return self.__fitness

    @property
    def genes(self) -> List[DNA]:
        """The genes of this individual"""
        return copy(self.__genes)

    @genes.setter
    def genes(self, new_genes: List[DNA]):
        """Assigns a new set of genes to this individual"""
        self.__genes = list(new_genes)

    @property
    def mutation_rate(self) -> float:
        """The probability with which the genes of the individual will mutate."""
        return self.__mutation_rate

    @mutation_rate.setter
    def mutation_rate(self, rate: float) -> None:
        """The probability with which the genes of the individual will mutate."""
        self.__mutation_rate = rate

    @property
    def crossover_strategy(self) -> Callable[..., 'Individual[DNA]']:
        """The strategy to perform a crossover between two individuals."""
        return self.__crossover_strategy

    @crossover_strategy.setter
    def crossover_strategy(self, strategy: Callable[..., 'Individual[DNA]']):
        """
        The strategy to perform a crossover between two individuals.
        If not set, the strategy is a single-point crossover with a randomly chosen cut point.
        """
        self.__crossover_strategy = strategy

    @property
    def mutation_strategy(self) -> Callable[..., 'Individual[DNA]']:
        """The strategy to perform a mutation over this individual."""
        return self.__mutation_strategy

    @mutation_strategy.setter
    def mutation_strategy(self, strategy: Callable[..., DNA]):
        """The strategy to perform a mutation over this individual."""
        self.__mutation_strategy = strategy

    @property
    def gene_factory(self) -> GeneFactory[DNA]:
        """A factory to generate the genes of this individual."""
        return self.__gene_factory

    @gene_factory.setter
    def gene_factory(self, factory: GeneFactory[DNA]):
        """Sets the factory that generates the genes of this individual."""
        self.__gene_factory = factory

    @property
    def factory_args(self) -> Tuple:
        return self.__factory_args

    # endregion

    def __len__(self):
        """The number of genes of this individual"""
        return len(self.__genes)

    def __repr__(self) -> str:
        """An individual is represented by its fitness and its genes."""
        return f"{self.__fitness} - {self.__genes}"

    def __eq__(self, other: Any) -> bool:
        """Two individuals are equal if they have the same fitness"""
        return isinstance(other, Individual) and get_args(self) == get_args(
            other) and self.__fitness == other.__fitness

    def __lt__(self, other: Any) -> bool:
        """Individuals are sorted according to their fitness."""
        return isinstance(other, Individual) and get_args(self) == get_args(
            other) and self.__fitness < other.__fitness

    def __le__(self, other):
        """Individuals are sorted according to their fitness."""
        return isinstance(other, Individual) and get_args(self) == get_args(
            other) and self.__fitness <= other.__fitness

    def __gt__(self, other) -> bool:
        """Individuals are sorted according to their fitness."""
        return isinstance(other, Individual) and get_args(self) == get_args(
            other) and self.__fitness > other.__fitness

    def __ge__(self, other) -> bool:
        """Individuals are sorted according to their fitness."""
        return isinstance(other, Individual) and get_args(self) == get_args(
            other) and self.__fitness >= other.__fitness

    def __copy__(self) -> 'Individual[DNA]':
        """Returns a copy of this individual."""
        return Individual(self.__genes, self.__mutation_rate, self.__gene_factory,
                          self.__crossover_strategy, self.__mutation_strategy,
                          self._random_generator)
