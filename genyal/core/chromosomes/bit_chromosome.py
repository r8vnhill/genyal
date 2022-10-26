"""
"genyal" (c) by Ignacio Slater M.
"genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
import secrets
from enum import Enum

from genyal.core.chromosomes.chromosome import Chromosome
from genyal.core.genes.bit_gene import BitGene
from genyal.genyal_exception import GenyalException


class BitChromosomeKwargs(str, Enum):
    """
    Keyword arguments for the BitChromosome class.
    """
    ONES_PROBABILITY = 'ones_probability'
    BITS = 'bits'
    LENGTH = 'length'


class BitChromosome(Chromosome[BitGene]):
    __ones_probability: float = 0.5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if BitChromosomeKwargs.LENGTH in kwargs.keys() \
                and BitChromosomeKwargs.ONES_PROBABILITY in kwargs.keys():
            self._genes, self.__ones_probability = self.__init_chromosome_of_length(
                length=kwargs[BitChromosomeKwargs.LENGTH],
                ones_probability=kwargs[BitChromosomeKwargs.ONES_PROBABILITY])

    def __init_chromosome_of_length(self, length: int, ones_probability: float) \
            -> tuple[list[BitGene], float]:
        if length <= 0:
            raise GenyalException(
                f"The length of a chromosome must be positive, but it was {length}")
        return [BitGene(dna=secrets.SystemRandom().random() < ones_probability) for _ in
                range(length)], self.__resolve_probability(ones_probability)

    @staticmethod
    def __resolve_probability(probability: float) -> float:
        if not 0 <= probability <= 1:
            raise GenyalException(
                f"The probability of ones must be between 0 and 1, but it was {probability}")
        return probability

    def ones_count(self) -> int:
        """
        Returns the number of ones in the chromosome.
        """
        return sum(gene.dna for gene in self._genes)
