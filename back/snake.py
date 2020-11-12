import random


UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"

DIRECTIONS = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}


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


def logger(txt):
    # if __name__ == "__main__":
    print(txt)