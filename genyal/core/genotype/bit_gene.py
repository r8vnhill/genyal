"""
"genyal" (c) by Ignacio Slater M.
"genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
import secrets
from enum import Enum

from genyal.core.genotype.gene import Gene


class BitGene(Gene[bool], Enum):
    """
    Binary gene.
    """
    TRUE = ONE = True
    FALSE = ZERO = False

    def bit(self):
        """
        Returns the bit value of this gene.
        """
        return self == BitGene.TRUE

    def to_bool(self):
        """
        Returns the boolean value of this gene.
        """
        return self.bit()

    def allele(self):
        """
        Returns the allele value of this gene.
        """
        return self.bit()

    @staticmethod
    def is_valid():
        """
        Returns whether this gene is valid.
        This method always returns True.
        """
        return True

    @staticmethod
    def make_gene(dna: bool = None):
        """
        Creates a new gene with the given DNA, or a random one if not given.
        """
        if dna is None:
            return BitGene.TRUE if secrets.choice([True, False]) else BitGene.FALSE
        return BitGene.TRUE if dna else BitGene.FALSE

    def __str__(self):
        return "True" if self.bit() else "False"
