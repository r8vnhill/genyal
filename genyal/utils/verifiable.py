"""
"genyal" (c) by Ignacio Slater M.
"genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
from abc import ABC, abstractmethod


class Verifiable(ABC):
    """A verifiable object is an object that can be verified."""

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Checks if the object is valid.
        """
        pass
