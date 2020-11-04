"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""

from copy import copy
from random import Random
from typing import Callable, List, Optional

from genyal.core import DNA, GeneticsCore, GeneticsError
from genyal.genotype import GeneFactory
from genyal.operations.crossover import single_point_crossover
from genyal.operations.mutation import simple_mutation


class Individual(GeneticsCore):
    __mutation_rate: float
    __fitness: Optional[float]
    __genes: List

    def __init__(self):
        super(Individual, self).__init__(Random())
        self.__fitness = None
        self.__genes = []
        self.__mutation_rate = 0.01
        self.__crossover_strategy = single_point_crossover
        self.__mutation_strategy = simple_mutation

    def compute_fitness_using(self, fitness_function: Callable):
        """Computes this individual's fitness if it hasn't been computed yet."""
        if not self.__genes:
            raise GeneticsError("The individual should have genes.")
        if self.__fitness is not None:
            return self
        self.__fitness = fitness_function(self.__genes)

    def set(self, number_of_genes: int, gene_factory: GeneFactory):
        """Generate the genes of the individual."""
        for _ in range(0, number_of_genes):
            self.__genes.append(gene_factory.make())

    def crossover(self, partner: 'Individual', *args):
        return self.__crossover_strategy(self, partner, *args)

    def mutate(self, *args):
        return self.__mutation_strategy(self, *args)

    @property
    def fitness(self) -> float:
        """The fitness of this individual according to its fitness function."""
        return self.__fitness

    @property
    def genes(self) -> List[DNA]:
        """The genes of this individual"""
        return copy(self.__genes)

    @genes.setter
    def genes(self, new_genes):
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

    def __len__(self):
        """The number of genes of this individual"""
        return len(self.__genes)

    @classmethod
    def create(cls, number_of_individual: int, number_of_genes: int, gene_factory: GeneFactory) \
            -> List['Individual']:
        """
        Factory method to easily create a population of individuals.

        Args:
            number_of_individual:
                number of individuals to return.
            number_of_genes:
                the number of genes each individual should have.
            gene_factory:
                a one-argument factory to generate a gene.
        """
        individuals = []
        for _ in range(0, number_of_individual):
            individual = Individual()
            individual.set(number_of_genes, gene_factory)
            individuals.append(individual)
        return individuals
