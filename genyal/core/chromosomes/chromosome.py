"""
"genyal" (c) by Ignacio Slater M.
"genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
import abc
from enum import Enum
from typing import Generic, TypeVar

from overrides import override

from genyal.core.genes.gene import Gene
from genyal.genyal_exception import GenyalException
from genyal.utils.verifiable import Verifiable

GENE = TypeVar("GENE", bound=Gene)


class ChromosomeKwargs(str, Enum):
    """
    Keyword arguments for the Chromosome class.
    """
    GENES = 'genes'


class Chromosome(Generic[GENE], Verifiable, abc.ABC):
    """
    Set of genes that are related to each other.
    """
    _genes: list[GENE]

    def __init__(self, **kwargs):
        """
        Initializes a chromosome with a list of genes.
        """
        if ChromosomeKwargs.GENES in kwargs.keys():
            genes = kwargs[ChromosomeKwargs.GENES]
            if not genes:
                raise GenyalException("A chromosome must have at least one gene.")
            self._genes = genes

    @override
    def is_valid(self) -> bool:
        return all(gene.is_valid() for gene in self._genes)

    def __str__(self):
        return f'[{", ".join(str(gene) for gene in self._genes)}]'
