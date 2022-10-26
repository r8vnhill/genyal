"""
"genyal" (c) by Ignacio Slater M.
"genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
import random

from genyal.genotype import GeneFactory
from genyal.individuals import Individual

if __name__ == '__main__':
    factory = GeneFactory(generator=lambda: random.choice([b'0', b'1']))
    i = Individual.__init__(gene_factory=factory)
