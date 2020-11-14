import random


UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"

DIRECTIONS = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}

NEIGHBORS_POS = [(0,1), (0,-1), (1,0), (-1,0)]


class Snake:
    def __init__(self, brain, body, direction):
        self.size = 2
        self.alive = True
        self.history = []

        self.brain = brain
        self.body = body
        self.direction = direction

        for b in self.body:
            b.slither_in()

    def is_alive(self):
        return self.alive

    def think(self, surroundings):
        potential_dir = self.brain.think(self.body, surroundings)
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
        return add_pos(self.body[0].pos, self.direction)


    def change_dir(self, dir):
        if dir and dir != tuple(p * (-1) for p in self.direction):
            self.direction = dir
        else:
            logger("Trying to turn around but failed!")

    def die(self):
        self.alive = False


class RandomAI:
    def think(self, *args, **kwargs):
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

    def clone(self):
        return RandomAI()



class AI:
    def __init__(self):
        self.nn = None
    
    def think(self, body, surroundings):
        head = body[0]
        neighbors = self.gather_data(head, surroundings)
        conclusions = self.analyze(neighbors)
        new_direction = self.propose_new_direction(conclusions)
        return new_direction

    def gather_data(self, head, surroundings):
        pos = head.pos
        neighbors = self.get_neighbors(pos, surroundings)
        return neighbors

    def get_neighbors(self, pos, surroundings):
        neighbors = []
        for n_pos in NEIGHBORS_POS:
            n = add_pos(pos, n_pos)
            try:
                cell = surroundings[n]
                neighbors += [cell]
            except KeyError:
                continue
        return neighbors

    def analyze(self, neighbors):
        # feed neighbors trough the NN
        # and get the resultiong analysis
        conclusions = {d:random.random() for d in DIRECTIONS}
        return conclusions

    def propose_new_direction(self, conclusions):
        # based on results, process it to define new dir
        best_option = self.best_option(conclusions)
        print(best_option)
        return DIRECTIONS[best_option]

    def best_option(self, thoughts):
        def rank(item):
            return item[1]

        best = max(thoughts.values())
        choices = [c for c,v in thoughts.items() if v == best]
        return choices[0]


def add_pos(pos1, pos2):
    return tuple(p1 + p2 for p1, p2 in zip(pos1, pos2))

        
def logger(txt):
    # if __name__ == "__main__":
    print(txt)
