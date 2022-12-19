from battlefield import Battlefield, Position
from tank import Tank, TankState
from enum import Enum
from random import random
from policy import Policy

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

    def validate_team(self, team: int) -> None:
        if (team not in [0,1]):
            raise ValueError("Invalid team. Valid values are 0 or 1.")

    def validate_team_and_player(self, team: int, player: int) -> None:
        self.validate_team(team)

        if (player not in list(range(len(self.teams[team])))):
            raise ValueError(f"Invalid player {player} for team {team}.")

    def remaining_tanks(self, team: int) -> int:
        self.validate_team(team)

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
        self.validate_team(team)

        other_team: int = 1 if team == 0 else 0

        if (self.battle_is_over() and self.remaining_tanks(team) > 0 and self.remaining_tanks(other_team) == 0):
            return True
        else:
            return False


    def possible_targets(self, team: int, player: int) -> list[int]:
        self.validate_team_and_player(team, player)
        
        # Does check that tank is ready to shoot.
        results: list[int] = []

        other_team: int = 1 if team == 0 else 0

        for other_player, other_player_state in enumerate(self.team_states[other_team]):
            # check that
            # - players are in range
            # - attacking player is reloaded and not in heavy cover
            # - target player is not in heavy cover
            if self.team_states[team][player].position_in_range(other_player_state.position) \
                and self.team_states[team][player].ready_to_shoot() \
                and not other_player_state.in_heavy_cover():
                results.append(other_player)

        return results

    def get_actions(self, team: int, player: int) -> list[Action]:
        self.validate_team_and_player(team, player)

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

    def calculate_shot_damage(self, team: int, player: int, enemy_player: int) -> int:
        # return the damage done by player on team shooting at enemy player on the other team
        # doesn't consider distance :shrug:

        self.validate_team_and_player(team, player)

        enemy_team: int = 0 if team == 1 else 1

        self.validate_team_and_player(enemy_team, enemy_player)

        attacker_state: TankState = self.team_states[team][player]
        target_state: TankState = self.team_states[enemy_team][enemy_player]
        
        landing_probability: float = 0.9

        if attacker_state.moving():
            landing_probability -= 0.2

        if target_state.moving():
            landing_probability -= 0.1

        if target_state.in_light_cover():
            landing_probability -= 0.2

        return attacker_state.tank.damage_per_shot if random() <= landing_probability else 0

    def generate_all_player_actions(self) -> tuple[list[list[Action]],list[list[Action]]]:
        actions = ([],[])

        for team in range(2):
            for player, player_state in enumerate(self.team_states[team]):
                actions[team].append(self.get_actions(team, player))

        return actions

    def apply_all_player_actions(self, chosen_actions: tuple[list[Action], list[Action]]) -> None:
        damage_dealt_and_avoided_log: tuple[list[int],list[int]] = ([0 for i in range(len(self.team_states[0]))],[0 for i in range(len(self.team_states[1]))])
        damage_taken_log: tuple[list[int],list[int]] = ([0 for i in range(len(self.team_states[0]))],[0 for i in range(len(self.team_states[1]))])

        # calculate damage
        for team in range(2):
            for player, player_state in enumerate(self.team_states[team]):
                if chosen_actions[team][player][0] == ActionType.SHOOT or chosen_actions[team][player][0] == ActionType.MOVE_AND_SHOOT:
                    target_player: int = chosen_actions[team][player][3]
                    enemy_team: int = 0 if team == 1 else 1
                    damage: int = self.calculate_shot_damage(team, player, target_player)

                    if damage == 0:
                        damage_dealt_and_avoided_log[enemy_team][target_player] += player_state.tank.damage_per_shot
                    else:
                        damage_dealt_and_avoided_log[team][player] += player_state.tank.damage_per_shot
                        damage_taken_log[enemy_team][target_player] += player_state.tank.damage_per_shot

        # Apply actions
        for team in range(2):
            for player, player_state in enumerate(self.team_states[team]):
                #type of action, new position, fired?, target
                action_type, new_pos, fired, target = chosen_actions[team][player]
                player_state.take_action(new_pos, fired, damage_dealt_and_avoided_log[team][player], damage_taken_log[team][player])

        # Update time left
        self.ticks_left = max(0, self.ticks_left - 1)