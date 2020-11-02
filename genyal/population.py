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


class Individual(GeneticsCore):
    __fitness: Optional[float]
    __genes: List

    def __init__(self):
        super(Individual, self).__init__(Random())
        self.__fitness = None
        self.__genes = []

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

    def single_point_crossover(self, partner: 'Individual', cut_point: int = -1) -> 'Individual':
        """
        Returns a new child from mixing this individual with another using a single-point crossover
        strategy.
        """
        if cut_point == -1:
            cut_point = self._rng.randrange(0, len(self.__genes))
        child = Individual()
        child.rng = self._rng
        crossover_genes = self.__genes[:cut_point].append(partner.__genes[cut_point:])
        child.__genes = crossover_genes
        return child

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
