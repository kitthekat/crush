"""Main module."""
from typing import NoReturn, Iterable, Union, Optional, Annotated
import numpy as np
from dataclasses import dataclass, field


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


@dataclass
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
        self.shapes = [i * [ActiveTile()] if isinstance(i, int) else DeadTile() for i in size]

    def __repr__(self):
        print(self.shapes)


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
        sizes: Union[Iterable[Iterable[Optional[int]]], Annotated[Iterable[int], 2]] = (5, 5),
        extras: bool = True
    ):
        try:
            assert isinstance(sizes, Iterable)
        except AssertionError:
            raise()
