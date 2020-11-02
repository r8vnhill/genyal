"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from typing import Callable, Generic

from genyal.core import DNA


class GeneFactory(Generic[DNA]):
    """Factory class for creating genes of type DNA."""
    __generator: Callable

    def __init__(self, *args):
        self.__generator = lambda x: x  # identity function by default
        self.__args = args

    @property
    def generator(self) -> Callable:
        return self.__generator

    @generator.setter
    def generator(self, generator_function: Callable) -> None:
        self.__generator = generator_function

    def make(self) -> DNA:
        return self.__generator(*self.__args)
