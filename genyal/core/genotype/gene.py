"""
"genyal" (c) by Ignacio Slater M.
"genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
from typing import Generic, TypeVar

DNA = TypeVar("DNA")


class Gene(Generic[DNA]):
    _dna: DNA

    @property
    def dna(self):
        return self._dna

    @dna.setter
    def dna(self, value):
        pass
