from battlefield import Battlefield
from tank import Tank, TankState

class Battle:

    def __init__(self, team0: "list[Tank]", team1: "list[Tank]", ticks_left: int = 60) -> None:
        self.team0 = team0
        self.team1 = team1
        self.ticks_left = ticks_left

        self.battlefield = Battlefield(len(team0), len(team1), (3,9))

        self.team0_states = []
        self.team1_states = []

        for i in range(len(self.battlefield.team0_starting_positions)):
            self.team0_states.append(TankState(self.team0[i], self.battlefield.team0_starting_positions[i])) # type: ignore

        for i in range(len(self.battlefield.team1_starting_positions)):
            self.team1_states.append(TankState(self.team1[i], self.battlefield.team1_starting_positions[i])) # type: ignore
