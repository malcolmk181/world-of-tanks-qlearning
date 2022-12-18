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
        self.teams: tuple[Team, Team] = (team0, team1)
        self.ticks_left: int = ticks_left

        self.battlefield: Battlefield = Battlefield(len(team0), len(team1), (3,9))

        self.team_states: tuple[list[TankState], list[TankState]] = ([],[])

        for team in range(2):
            for i, pos in enumerate(self.battlefield.team_starting_positions[team]):
                self.team_states[team].append(TankState(self.teams[team][i], pos, self.battlefield))

    def possible_targets(self, team: int, player: int) -> list[int]:
        # Doesn't check validity of team or player
        results: list[int] = []

        other_team: int = 1 if team == 0 else 0

        for other_player, other_player_state in enumerate(self.team_states[other_team]):
            if self.team_states[team][player].position_in_range(other_player_state.position):
                results.append(other_player)

        return results

    def get_actions(self, team: int, player: int):
        # Error checking
        if (team not in [0,1]):
            raise ValueError("Invalid team. Valid values are 0 or 1.")

        if (player not in list(range(len(self.teams[team])))):
            raise ValueError(f"Invalid player {player} for team {team}.")

        tank_state: TankState = self.team_states[team][player]

        # Building actions
        actions: list[Action] = []

        if tank_state.alive():
            actions.append((ActionType.DO_NOTHING, tank_state.position, False, 0, 0))

            # possible movement positions
            # for position in 