"""
"genyal" (c) by Ignacio Slater M.
"genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""


def cum_difference(numbers: list[float]) -> float:
    """
    Calculates the absolute cummulative difference between the numbers of a list
    """
    diff = 0
    for n in numbers:
        diff *= -1
        diff += n
    return abs(diff)
