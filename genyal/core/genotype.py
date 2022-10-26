"""
"genyal" (c) by Ignacio Slater M.
"genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
from typing import Generic, TypeVar

from genyal.core.chromosomes.bit_chromosome import BitChromosome
from genyal.core.chromosomes.chromosome import Chromosome
from genyal.core.genes.gene import Gene
from genyal.genyal_exception import GenyalException

GENE = TypeVar("GENE", bound=Gene)


class Genotype(Generic[GENE]):
    """
    Genotype of an individual.
    """
    __chromosomes: list[Chromosome[GENE]]

    def __init__(self, chromosomes: list[Chromosome[GENE]]):
        """
        Initializes a genotype with a list of chromosomes.
        """
        if not chromosomes:
            raise GenyalException("A genotype must have at least one chromosome.")
        self.__chromosomes = chromosomes

    @property
    def chromosomes(self) -> list[Chromosome[GENE]]:
        """
        Gets the chromosomes of the genotype.
        """
        return self.__chromosomes

    def __str__(self):
        return f'[{", ".join(str(chromosome) for chromosome in self.__chromosomes)}]'


if __name__ == '__main__':
    print(Genotype(chromosomes=[BitChromosome(length=10, ones_probability=0.5)]))
