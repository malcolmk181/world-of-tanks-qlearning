from battlefield import Battlefield
from tank import Tank, TankState

class Battle:

    def __init__(self, team1: "list[Tank]", team2: "list[Tank]", ticks_left: int = 60) -> None:
        self.team1 = team1
        self.team2 = team2
        self.ticks_left = ticks_left

        self.battlefield = Battlefield(len(team1), len(team2), (3,9))

        self.team1_states = []
        self.team2_states = []

        for i in range(len(self.battlefield.team1_starting_positions)):
            self.team1_states.append(TankState(self.team1[i], self.battlefield.team1_starting_positions[i])) # type: ignore

        for i in range(len(self.battlefield.team2_starting_positions)):
            self.team2_states.append(TankState(self.team2[i], self.battlefield.team2_starting_positions[i])) # type: ignore

        