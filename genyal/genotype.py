"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from typing import Callable, Generic, Tuple

from genyal.core import DNA


class GeneFactory(Generic[DNA]):
    """Factory class for creating genes of type DNA."""
    __generator: Callable

    def __init__(self, generator=id, *args):
        """
        Creates a new factory to make genes.
        Args:
            *args:
                In case that the generator function of this factory needs arguments they can be
                supplied by using the constructor.
        """
        self.__generator = generator
        self.__args = args

    @property
    def generator(self) -> Callable[..., DNA]:
        """The generator is the function that the factory is going to use to create new genes."""
        return self.__generator

    @generator.setter
    def generator(self, generator_function: Callable[..., DNA]) -> None:
        """Gives a new generator function to the factory."""
        self.__generator = generator_function

    @property
    def generator_args(self) -> Tuple:
        return self.__args

    @generator_args.setter
    def generator_args(self, args: Tuple):
        self.__args = args

    def make(self) -> DNA:
        """
        Creates a new gene using the factory's generator function and (if present) the arguments
        given on the constructor.
        """
        return self.__generator(*self.__args)
