"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random

from genyal.engine import GenyalEngine
from genyal.genotype import GeneFactory


def create_candidate_factors() -> list[int]:
    """
    Creates a list with 1 and the prime numbers from 2 to 500 computed using the sieve of
    Eratosthenes.
    """
    is_prime = [True] * 500
    p = 2
    while p ** 2 < 500:
        if is_prime[p]:
            for i in range(p ** 2, 500, p):
                is_prime[i] = False
        p += 1
    primes = []
    for n in range(2, 500):
        if is_prime[n]:
            primes.append(n)
    return primes


def stale_for():
    """"""


if __name__ == '__main__':
    candidate_factors = create_candidate_factors()
    factory = GeneFactory(generator=lambda: random.choice(candidate_factors))
    engine = GenyalEngine(minimize_fitness=True)
    engine.create_population(10000, 10, factory)
