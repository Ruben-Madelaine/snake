import random


UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"

DIRECTIONS = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}


class Board:
    grid = {}
    size = 0

    def __init__(self, size):
        self.size = size
        self.create()

    def __str__(self):
        txt = ""

        for i in range(self.size):
            txt += "\n"
            line = " ".join(str(self.grid[(i, j)]) for j in range(self.size))
            txt += line

        return "The best Board!" + txt

    def create(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[(i, j)] = Cell(i, j)

    def place_fruit(self, i, j):
        if self.grid[(i, j)].is_empty():
            return self.grid[(i, j)].land_fruit()
        else:
            return self.drop_fruit()

    def drop_fruit(self):
        i = random.randint(0, self.size - 1)
        j = random.randint(0, self.size - 1)
        return self.place_fruit(i, j)


class Cell:
    empty = True
    fruit = False
    occupants = 0

    def __init__(self, i, j):
        self.pos = i, j

    def __str__(self):
        herb = '"' if self.empty else ""
        fruit = "@" if self.fruit else ""
        snake = "o" if self.occupants else ""

        return snake or fruit or herb

    def is_empty(self):
        return self.empty

    def have_fruit(self):
        return self.fruit

    def land_fruit(self):
        self.fruit = not self.fruit
        self.empty = not self.empty
        return self

    def consume_fruit(self):
        self.fruit = not self.fruit
        self.empty = not self.empty

    def slither_in(self):
        self.occupants += 1

        if self.occupants: 
            self.empty = False

    def slither_out(self):
        self.occupants -= 1
        if not self.occupants: 
            self.empty = True

class Snake:
    size = 2
    alive = True
    history = []

    def __init__(self, brain, body, direction):
        self.brain = brain
        self.body = body
        self.direction = direction

        for b in self.body:
            b.slither_in()

    def is_alive(self):
        return self.alive

    def think(self):
        potential_dir = self.brain.think()
        self.change_dir(potential_dir)

    def move(self, head):
        self.body = [head] + self.body
        self.history += [self.direction]

        if head.have_fruit():
            head.consume_fruit()
            head.slither_in()
            self.size += 1
            return "ate the fruit"
        else:
            head.slither_in()
            tail = self.body.pop()
            tail.slither_out()

    def next_pos(self):
        return self.add_pos(self.body[0].pos, self.direction)

    def add_pos(self, pos1, pos2):
        return tuple(p1 + p2 for p1, p2 in zip(pos1, pos2))

    def change_dir(self, dir):
        if dir and dir != tuple(p * (-1) for p in self.direction):
            self.direction = dir
        else:
            logger("Trying to turn around but failed!")

    def die(self):
        self.alive = False

    def clone(self):
        clone = Snake(self.brain, self.body, self.direction)
        return clone

class RandomAI:
    def think(self):
        if random.random() > 0.5:
            choice = random.choice(list(DIRECTIONS.keys()))
            txt = [f"Huum.. Let's go {choice}", f"What about goint {choice} ?"]
            potential_dir = DIRECTIONS[choice]
            logger(random.choice(txt))
            return potential_dir
        else:
            txt = [
                "Not in the mood for thinking...",
                "Let's keep going!",
                "I shouldn't think too much about it...",
            ]
            logger(random.choice(txt))

class Game:
    def __init__(self, size):
        self.board = Board(size)

    def __str__(self):
        return str(self.board)

    # -------------- INIT --------------------

    def start(self):
        self.count = 0
        self.air_drop_fruit()
        self.hatch_from_egg()

    def air_drop_fruit(self, i=None, j=None):
        if i and j:
            self.fruit = self.board.place_fruit(i, j)
        else:
            self.fruit = self.board.drop_fruit()

    def hatch_from_egg(self):
        center = self.board.size // 2
        head = self.board.grid[center, center]
        tail = self.board.grid[center, center - 1]
        body = [head, tail]

        self.snake = Snake(RandomAI(), body, DIRECTIONS[RIGHT])

    def play(self):
        while self.snake.is_alive():
            yield self.next()
        logger(
            f"\n> Our fellow Snake friend died at the age of {self.count}. What a pitty..."
        )

    # -------------- SET --------------------

    def hard_start(self, i, j):
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

        self.snake.think()
        next_pos = self.snake.next_pos()
        cell = self.get_cell(next_pos)
        if cell:
            ate_a_fruit = self.snake.move(cell)
            if ate_a_fruit:
                self.fruit = self.board.drop_fruit()
                logger("Air dropping a new fruit in 3...2..1.. *BOOM*")
        else:
            logger("End of game!")

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

    # -------------- POPULATION --------------------

class Population:

    def __init__(size):
        self.size = size

    def breed(self, snake):
        self.snakes = [snake.clone() for _ in range(self.size)]

    # live
    def live(self):
        pass
    # next gen
        # get best and breed


    # copy snake N times
    # isolate each snake in its world
    # go for the fruit !
    # success or fail:
    #  - Ate the fruit
    #  - Died


def logger(txt):
    if __name__ == "__main__":
        print(txt)


def main():
    g = Game(10)
    g.start()
    print(g)
    
    for _ in g.play():
        pass

    print(g)
    state = g.get_state()
    print(state)


if __name__ == "__main__":
    main()
