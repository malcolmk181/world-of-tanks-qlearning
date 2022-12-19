from abc import ABC, abstractmethod
from tank import TankState
from battle import Action, ActionType, Battle
from random import choice

class Policy(ABC):

    def __init__(self, battle: Battle):
        self.battle = battle

    @abstractmethod
    def choose_action(self, team: int, player: int, team_states: "tuple[list[TankState],list[TankState]]", actions: list[Action]) -> Action:
        pass

class RandomPolicy(Policy):

    def choose_action(self, team: int, player: int, team_states: "tuple[list[TankState],list[TankState]]", actions: list[Action]) -> Action:
        return choice(actions)

class GreedyShooterRandomPolicy(Policy):

    def choose_action(self, team: int, player: int, team_states: "tuple[list[TankState],list[TankState]]", actions: list[Action]) -> Action:
        """
            When available, chooses a shooting action. Otherwise moves randomly.
        """
        
        shoot_plays: list[Action] = list(filter(lambda a : a[0] in [ActionType.MOVE_AND_SHOOT, ActionType.SHOOT], actions))

        if len(shoot_plays) > 0:
            return choice(shoot_plays)
        else:
            return choice(actions)