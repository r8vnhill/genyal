"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""


class GeneticsCore:
    """Base for the elements involved in a genetic algorithm's population."""
    pass


class GeneticsError(Exception):
    def __init__(self, cause: str):
        super(GeneticsError, self).__init__(cause)
