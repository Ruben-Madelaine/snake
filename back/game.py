import time

import snake
from board import Board

try:
    import snake
    from board import Board
except ModuleNotFoundError:
    import back.snake as snake
    from back.board import Board


STARVING_THRESHOLD = 200


import os

clear = lambda: os.system("clear")


class Game:
    def __init__(self, size):
        self.board = Board(size)
        self.count = 0
        self.starving = 0

    def __str__(self):
        return str(self.board)

    # -------------- INIT --------------------

    def start(self, brain=snake.RandomAI):
        self.air_drop_fruit()
        self.hatch_from_egg(brain)

    def air_drop_fruit(self, i=None, j=None):
        if i and j:
            self.fruit = self.board.place_fruit(i, j)
        else:
            self.fruit = self.board.drop_fruit()

    def hatch_from_egg(self, brain):
        center = self.board.size // 2
        head = self.board.grid[center, center]
        tail = self.board.grid[center, center - 1]
        body = [head, tail]

        self.snake = snake.Snake(brain(), body, snake.DIRECTIONS[snake.RIGHT])

    def play(self, verbose=False):
        while self.snake.is_alive() and self.starving < STARVING_THRESHOLD:
            self.next()
            if verbose:
                print(self)
                time.sleep(0.1)
                clear()

        if verbose:
            print(
                f"> Our fellow Snake friend died at the age of {self.count}. What a pitty..."
            )

    def replay(self):
        pass

    # -------------- CONTROLLER --------------------

    def get_state(self):
        res = {
            "snake": [b.pos for b in self.snake.body],
            "fruit": self.fruit.pos if self.fruit else None,
            "moves": self.snake.history,
        }
        return res

    # -------------- CORE --------------------

    def next(self):
        self.count += 1
        self.starving += 1

        self.snake.think(self.board.grid)
        next_pos = self.snake.next_pos()
        cell = self.get_cell(next_pos)
        if cell:
            ate_a_fruit = self.snake.move(cell)
            if ate_a_fruit:
                self.starving = 0
                self.fruit = self.board.drop_fruit()
                logger("Air dropping a new fruit in 3...2..1.. *BOOM*")

    def get_cell(self, next_pos):
        if self.is_available(next_pos):
            cell = self.board.grid[next_pos]
            if cell.is_empty() or cell.have_fruit():
                return cell
        else:
            self.snake.die()

    def is_available(self, next_pos):
        i, j = next_pos
        return (0 <= i < self.board.size) and (0 <= j < self.board.size)


def logger(txt):
    if __name__ == "__main__":
        print(txt)


def test_game():
    g = Game(5)
    g.start()
    print(g)

    g2 = Game(10)
    g2.start()
    print(g2)

    g.play()

    print(g)
    print(g2)

    state = g.get_state()
    print(state)


def test_ai():
    g = Game(10)
    g.start(snake.AI)
    print(g)

    g.play()
    print(g)


def main():
    # test_game()
    test_ai()


if __name__ == "__main__":
    main()
