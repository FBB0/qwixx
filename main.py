from copy import deepcopy
from random import choice

from qwixx.game import Color, compete
from qwixx.player import Player


class RandomPlayer(Player):
    def move(self, actions, is_main, scoreboard, scoreboards):
        return choice(actions)


class ImprovedPlayer(Player):
    """
    An improved agent that no longer picks a random move, but who picks a move that leaves the fewest open squares
    """
    def cost(self, scoreboard, actions):
        """
        Measures the cost of a set of actions. Formally, it's the number of squares left empty by playing a move
        """
        # arbitrarily decide that the cost for taking no action is 10
        if len(actions) == 0:
            return 10
        scoreboard = deepcopy(scoreboard)
        c = 0
        for action in actions:
            if len(scoreboard[action.color]) != 0:
                c += abs(scoreboard[action.color][-1] - action.n) - 1
            else:
                if action.color in [Color.RED, Color.YELLOW]:
                    c += abs(action.n - 1) - 1
                else:
                    c += abs(action.n - 13) - 1
        return c / len(actions)

    def move(self, actions, is_main, scoreboard, scoreboards):
        best_action = []
        cost = float('inf')
        if not is_main:
            for action in actions:
                new_c = self.cost(scoreboard, action)
                if new_c < cost:
                    cost = new_c
                    best_action = action

        else:
            for action in actions:
                new_c = self.cost(scoreboard, action)
                if new_c < cost:
                    cost = new_c
                    best_action = action
        return best_action


if __name__ == '__main__':
    print(compete(ImprovedPlayer(), RandomPlayer()))
