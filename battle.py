from battlefield import Battlefield, Position
from tank import Tank, TankState
from enum import Enum

class ActionType(Enum):
    DO_NOTHING = 0
    MOVE = 1
    SHOOT = 2
    MOVE_AND_SHOOT = 3

Action = tuple[ActionType, Position, bool, int, int]
Team = list[Tank]

class Battle:

    def __init__(self, team0: Team, team1: Team, ticks_left: int = 60) -> None:
        self.team0: Team = team0
        self.team1: Team = team1
        self.ticks_left: int = ticks_left

        self.battlefield: Battlefield = Battlefield(len(team0), len(team1), (3,9))

        self.team0_states: list[TankState] = []
        self.team1_states: list[TankState] = []

        for i in range(len(self.battlefield.team0_starting_positions)):
            self.team0_states.append(TankState(self.team0[i], self.battlefield.team0_starting_positions[i], self.battlefield))

        for i in range(len(self.battlefield.team1_starting_positions)):
            self.team1_states.append(TankState(self.team1[i], self.battlefield.team1_starting_positions[i], self.battlefield))

            