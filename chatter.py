import random
from collections import defaultdict
from collections import Counter
import itertools
import json
import toolz
import operator
import bisect

def sample_from_counter(counter):
    choices, weights = zip(*counter.items())
    cumdist = list(itertools.accumulate(weights))
    dice_roll = random.randrange(toolz.last(cumdist))
    return choices[bisect.bisect(cumdist, dice_roll)]


class Chatter:

    def __init__(self):
        self.brain = {}

    def teach(self, texts):
        for text in texts:
            unigrams = ['__START__'] + text.split() + ['__END__']
            for left, right in toolz.sliding_window(2, unigrams):
                # using defaultdict and counter directly didn't always work
                if left not in self.brain:
                    self.brain[left] = {}
                if right not in self.brain[left]:
                    self.brain[left][right] = 0
                self.brain[left][right] += 1

    def say(self):
        def tokens(max_len=50):
            length = 0

            current_word = sample_from_counter(self.brain['__START__'])
            while current_word != '__END__':
                yield current_word
                length += 1
                if length > max_len:
                    return

                current_word = sample_from_counter(self.brain[current_word])

        return ' '.join(tokens())

    def dump(self, filename):
        json.dump(self.brain, open(filename, 'w'))

    def load(self, filename):
        self.brain = json.load(open(filename))
