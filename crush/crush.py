"""Main module."""
from typing import NoReturn, Iterable, Union, Optional, Annotated
import numpy as np
from dataclasses import dataclass, field
from toolz import pipe
from operator import add, sub, truediv


def main() -> NoReturn:
    """
    Executes single Crush game
    :return:
    """
    return


class Game:
    """
    Singleton for running and managing crush game. Not currently used. If implemented,
    should contain "menu", "new game", etc. features
    """
    pass


@dataclass(order=False)
class GameBoardObject:
    movable: bool = True
    disposable: bool = False


@dataclass(order=False)
class Tile:
    playable: bool = field(init=False)


class ActiveTile(Tile):
    contents: GameBoardObject = None
    playable = True


class DeadTile(Tile):
    playable = False


class Row:
    """
    A row object representing a single gameboard row.

    Used primarily as a device for human construction
    of game boards.

    Rows are constructed from n-length iterable objects
    containing integers, None/np.nan objects, and other
    game board objects, like Obstacles.

    Integers are interpreted similar to how Python would execute the
    statement:
        >>> i * [ActiveTile()]

    Where i is an Integer value representing consecutive playable tiles.

    np.nan and None values are converted to non-playable,
    non-interactable blocked tiles.

    For instance, (2, np.nan, 2, np.nan, 2) will export a game row which
    visually resembles:
     ________________________________
    |___|___|_X_|___|___|_X_|___|___|

    Where |___| are playable tiles (ActiveTile) and |_X_| are
    blocked/unplayable (DeadTile) tiles.

    In reality, a Row iterable object is created containing objects
    [ActiveTile, ActiveTile, DeadTile, ActiveTile, ActiveTile, DeadTile, ...].

    Examples
    --------
        a = Row(size=(5, np.nan, np.nan, 5))
        len(a)
        >>> 12

    """
    def __init__(self, size: Iterable[Optional[int]]):
        self.tiles = pipe(
            size,
            self._make_tiles,
            np.array,
            lambda x: x.flatten()
        )

    def __repr__(self):
        return str(self.shapes)




class GameBoard:
    """
    A geometric grid which serves as the playing space for a Crush game.

    Intakes a series of (n_1, ..., n_i) Iterable objects (Iterable[Iterable])
    which are converted to Row objects and then "stacked"
    (treating first passed element as the "bottom" gameboard row)
    to create a gameboard.

    See Row class for acceptable formats.

    Alternatively, accepts a 2-element (n, m) (Iterable[int, int]) Iterable
    representing the n x m rectangular shape of the gameboard.

    Leveraging the Row-wise construction allows for more "interesting" gameboard
    setups.

    Parameters
    -----------
    """
    def __init__(
        self,
        rows: Union[Iterable[Iterable[Optional[int]]], Annotated[Iterable[int], 2]] = (5, 5),
        include_extras: bool = True
    ):
        try:
            assert isinstance(rows, Iterable)
        except AssertionError:
            raise(
                TypeError,
                f"Unable to parse object type {type(rows)} into game pieces"
            )
        # Determine if user is inputting rows line-by-line or as an X, Y grid
        # and assign global width, height accordingly
        match isinstance(rows[0], int):
            case True:
                self.global_width, self.global_height = rows[0], rows[1]
            case False:
                self.widths = self._get_row_widths(rows)
                # Check that row widths are valid
                try:
                    assert all([i % 2 == 0 for i in self.widths])
                except AssertionError:
                    raise(
                        ValueError,
                        "Row widths must be entirely odd or entirely even"
                    )
                self.global_width = max(self.widths)
                self.global_height = len(rows)

        self.board = self.initialize_board(rows, include_extras)

    def initialize_board(self, rows, include_extras):
        for i, v in enumerate(self.widths):
            padding = int(truediv(sub(self.global_width, v), 2))
            for tile_placeholder in rows[i]:
                tiles = np.array(
                    add(
                        padding * [DeadTile()],
                        self._make_tiles(rows),
                        padding * [DeadTile()]
                    )
                )
        pass

    @staticmethod
    def _make_tiles(some_list: Iterable(Optional[int])):
        return [i * [ActiveTile()] if isinstance(i, int) else DeadTile() for i in some_list]

    @staticmethod
    def _get_row_widths(
        rows: Union[Iterable[Iterable[Optional[int]]], Annotated[Iterable[int], 2]]
    ) -> list:
        """
        Calculates maximum row width and returns as overall game board width

        Parameters
        ----------
        rows
            An iterable matching the __init__ rows typing

        Returns
        -------
        List of row lengths
        """
        return list(
            map(
                lambda row:  # Calculates len(non-integers) + sum(integers)
                add(
                    sum(  # The sum of valid integers
                        valid_ints := list(
                            filter(  # Remove non-integers
                                lambda x: isinstance(x, int), row
                            )
                        )
                    ),
                    sub(len(row), len(valid_ints))  # The length of non-integers
                ),
                rows
            )
        )
