from battlefield import Battlefield, Position
from tank import Tank, TankState
from enum import Enum

class ActionType(Enum):
    DO_NOTHING = 0
    MOVE = 1
    SHOOT = 2
    MOVE_AND_SHOOT = 3

# Action: type of action, new position, fired?, target (only valid if fired)
Action = tuple[ActionType, Position, bool, int]

# ActionResult: type of action, new position, fired?, target (only valid if fired), damage dealt and avoided, damage received
ActionResult = tuple[ActionType, Position, bool, int, int, int]

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

    def remaining_tanks(self, team: int) -> int:
        remaining: int = 0
        for tank_state in self.team_states[team]:
            remaining += 1 if tank_state.alive() else 0

        return remaining

    def battle_is_over(self) -> bool:
        if self.ticks_left == 0:
            return True

        # check remaining tanks of each team, if either one is zero, return True
        for team in range(2):
            if self.remaining_tanks(team) == 0:
                return True

        return False

    def win(self, team: int) -> bool:
        other_team: int = 1 if team == 0 else 0

        if (self.battle_is_over() and self.remaining_tanks(team) > 0 and self.remaining_tanks(other_team) == 0):
            return True
        else:
            return False


    def possible_targets(self, team: int, player: int) -> list[int]:
        # Doesn't check validity of team or player
        results: list[int] = []

        other_team: int = 1 if team == 0 else 0

        for other_player, other_player_state in enumerate(self.team_states[other_team]):
            if self.team_states[team][player].position_in_range(other_player_state.position):
                results.append(other_player)

        return results

    def get_actions(self, team: int, player: int) -> list[Action]:
        # Error checking
        if (team not in [0,1]):
            raise ValueError("Invalid team. Valid values are 0 or 1.")

        if (player not in list(range(len(self.teams[team])))):
            raise ValueError(f"Invalid player {player} for team {team}.")

        tank_state: TankState = self.team_states[team][player]

        # Building actions
        actions: list[Action] = []

        if tank_state.alive():
            actions.append((ActionType.DO_NOTHING, tank_state.position, False, -999))

            # possible movement positions
            for position in self.battlefield.possible_positions(tank_state.position):
                # if original position, only option is shooting
                if (position == tank_state.position):
                    # just shoot

                    for target in self.possible_targets(team, player):
                        actions.append((ActionType.SHOOT, tank_state.position, True, target))

                else:
                    # not original position - can just move, or move & shoot

                    # just move
                    actions.append((ActionType.MOVE, position, False, -999))

                    # move and shoot
                    for target in self.possible_targets(team, player):
                        actions.append((ActionType.MOVE_AND_SHOOT, tank_state.position, True, target))

        return actions