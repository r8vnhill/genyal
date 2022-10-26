"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from random import Random
from typing import TypeVar

DNA = TypeVar("DNA")


class GenyalCore:
    """Base for the elements involved in a genetic algorithm's population."""
    _random_generator: Random

    def __init__(self, random_generator: Random):
        """Initializes a genetic algorithm element with a random number generator."""
        self._random_generator = random_generator

    @property
    def random_generator(self) -> Random:
        """The random number generator of this element."""
        return self._random_generator

    @random_generator.setter
    def random_generator(self, new_generator: Random):
        """Sets a new random number generator."""
        self._random_generator = new_generator


class GeneticsError(Exception):
    """When there's an error on the genetic configuration of an element."""
    _cause: str

    def __init__(self, cause):
        super(GeneticsError, self).__init__(cause)
        self._cause = cause

    @property
    def cause(self):
        return self._cause
