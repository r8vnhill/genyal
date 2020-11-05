"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""

from copy import copy
from random import Random
from typing import Any, Callable, Generic, List, Optional, Sequence

from genyal.core import DNA, GeneticsCore, GeneticsError
from genyal.genotype import GeneFactory
from genyal.operations.crossover import single_point_crossover
from genyal.operations.mutation import simple_mutation


class Individual(GeneticsCore, Generic[DNA]):
    __fitness: Optional[float]
    __genes: Sequence[DNA]
    __gene_factory: GeneFactory[Any]
    __mutation_rate: float
    __crossover_strategy: Callable[..., 'Individual']
    __mutation_strategy: Callable[..., 'Individual']

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

    @classmethod
    def create(cls, number_of_individuals: int, number_of_genes: int, gene_factory: GeneFactory) \
            -> List['Individual']:
        """
        Factory method to easily create a population of individuals.

        Args:
            number_of_individuals:
                number of individuals to return.
            number_of_genes:
                the number of genes each individual should have.
            gene_factory:
                a one-argument factory to generate a gene.
        """
        individuals = []
        for _ in range(0, number_of_individuals):
            individual = Individual()
            individual.set(number_of_genes, gene_factory)
            individuals.append(individual)
        return individuals

    def compute_fitness_using(self, fitness_function: Callable):
        """Computes this individual's fitness if it hasn't been computed yet."""
        if not self.__genes:
            raise GeneticsError("The individual should have genes.")
        if self.__fitness is None:
            self.__fitness = fitness_function(self.__genes)

    def set(self, number_of_genes: int, gene_factory: GeneFactory):
        """Generate the genes of the individual."""
        for _ in range(0, number_of_genes):
            self.__genes.append(gene_factory.make())

    def crossover(self, partner: 'Individual', *args):
        return self.__crossover_strategy(self, partner, *args)

    def mutate(self, *args) -> 'Individual':
        return self.__mutation_strategy(self, *args)

    # region : Properties
    @property
    def fitness(self) -> float:
        """The fitness of this individual according to its fitness function."""
        return self.__fitness

    @property
    def genes(self) -> Sequence[DNA]:
        """The genes of this individual"""
        return copy(self.__genes)

    @genes.setter
    def genes(self, new_genes: Sequence[DNA]):
        """Assigns a new set of genes to this individual"""
        self.__genes = new_genes

    @property
    def mutation_rate(self) -> float:
        return self.__mutation_rate

    @mutation_rate.setter
    def mutation_rate(self, rate: float) -> None:
        self.__mutation_rate = rate

    @property
    def crossover_strategy(self):
        return self.__crossover_strategy

    @crossover_strategy.setter
    def crossover_strategy(self, strategy):
        self.__crossover_strategy = strategy

    @property
    def mutation_strategy(self):
        return self.__mutation_strategy

    @mutation_strategy.setter
    def mutation_strategy(self, strategy):
        self.__mutation_strategy = strategy

    @property
    def gene_factory(self) -> GeneFactory:
        """A factory to generate the genes of this individual."""
        return self.__gene_factory

    @gene_factory.setter
    def gene_factory(self, factory: GeneFactory):
        """Sets the factory that generates the genes of this individual."""
        self.__gene_factory = factory

    # endregion

    def __len__(self):
        """The number of genes of this individual"""
        return len(self.__genes)

    def __copy__(self):
        """Returns a copy of this individual."""
        cp = Individual()
