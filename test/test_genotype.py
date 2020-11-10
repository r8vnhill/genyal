"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import string
import sys
import unittest
from random import Random, randrange

import pytest

from genyal.genotype import GeneFactory


@pytest.mark.repeat(8)
def test_basic_factory(seed: int) -> None:
    factory = GeneFactory[float]()
    gene = Random(seed).random()
    assert factory.generator(gene) == id(gene), f"Test failed with seed: {seed}"


@pytest.mark.repeat(8)
def test_binary_factory(seed: int) -> None:
    rand_generator = Random(seed)
    factory = GeneFactory(generator=lambda rng: rng.random() > 0.5)
    factory.generator_args = (Random(seed),)
    assert factory.make() == (rand_generator.random() > 0.5), "Test failed with seed: {seed}"


@pytest.mark.repeat(32)
def test_ascii_factory(seed: int) -> None:
    gene = Random(seed).choice(string.ascii_lowercase)
    factory = GeneFactory()
    factory.generator_args = (gene,)
    assert factory.make() == id(gene), f"Test failed with seed: {seed}"
    factory.generator = lambda: Random(seed).choice(string.ascii_lowercase)
    factory.generator_args = ()
    assert factory.make() == gene, f"Test failed with seed: {seed}"


@pytest.fixture()
def seed() -> int:
    return randrange(-sys.maxsize, sys.maxsize)


if __name__ == '__main__':
    unittest.main()
