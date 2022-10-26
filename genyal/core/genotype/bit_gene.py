"""
"genyal" (c) by Ignacio Slater M.
"genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
import secrets

from genyal.core.genotype.gene import Gene


class BitGene(Gene[bool]):
    """
    Binary gene.
    """

    def __init__(self, dna: bool = None):
        """
        Initializes a binary gene.
        """
        if dna is None:
            dna = secrets.choice([True, False])
        self._dna = dna

    def bit(self):
        """
        Returns the bit value of this gene.
        """
        return self._dna

    def to_bool(self):
        """
        Returns the boolean value of this gene.
        """
        return self._dna

    @staticmethod
    def is_valid():
        """
        Returns whether this gene is valid.
        This method always returns True.
        """
        return True

    def __str__(self):
        return "True" if self.bit() else "False"
