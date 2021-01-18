"""
"genyal" (c) by Ignacio Slater M.
"genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from genyal.individuals import Individual


class Generation:
    __fittest: Individual

    @property
    def fittest(self):
        return self.__fittest

    @fittest.setter
    def fittest(self, individual: Individual):
        self.__fittest = individual

    @property
    def best_fitness(self) -> float:
        return self.__fittest.fitness
