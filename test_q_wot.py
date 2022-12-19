from policy import Policy, RandomPolicy, GreedyShooterRandomPolicy
from battle import Battle
from tank import Tank
from enum import Enum

class Result(Enum):
    TEAM0_WIN = 1
    DRAW = 0
    TEAM1_WIN = -1

def simulate_1v1(p0_policy: Policy, p1_policy: Policy, verbose: bool = False) -> Result:
    b = Battle([Tank()], [Tank()])

    p0_policy = p0_policy(b) # type: ignore
    p1_policy = p1_policy(b) # type: ignore
    
    if verbose:
        print(f"Ticks left: {b.ticks_left}")

    while(not b.battle_is_over()):

        team0_actions, team1_actions = b.generate_all_player_actions()
        player0_actions = team0_actions[0]
        player1_actions = team1_actions[0]

        b.apply_all_player_actions(([p0_policy.choose_action(0,0,player0_actions)], [p1_policy.choose_action(1,0,player1_actions)]), verbose)

    if verbose:
        print(f"\nGAME OVER. Ticks left: {b.ticks_left}")

    result: Result = Result.DRAW
    if b.win(0):
        if verbose:
            print("Win for team 0.")
        result = Result.TEAM0_WIN
    elif b.win(1):
        if verbose:
            print("Win for team 1.")
        result = Result.TEAM1_WIN
    else:
        if verbose:
            print("Draw.")

    if verbose:
        b.print_all_tank_stats()

    return result


if (__name__ == "__main__"):

    NUM_BATTLES = 100000

    wins, draws, losses = 0, 0, 0

    for i in range(NUM_BATTLES):
        result: Result = simulate_1v1(RandomPolicy, RandomPolicy) # type: ignore

        if result == Result.DRAW:
            draws += 1
        elif result == Result.TEAM0_WIN:
            wins += 1
        else:
            losses += 1

    print(f"Out of {NUM_BATTLES} battles, team 0 had:\n{wins} wins\n{draws} draws\n{losses} losses")