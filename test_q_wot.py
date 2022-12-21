from policy import Policy, RandomPolicy, GreedyShooterRandomPolicy
from battle import Battle
from tank import Tank
from enum import Enum
from q_wot import q_learn_1v1
import sys

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

def simulate_n_battles(p0_policy: Policy, p1_policy: Policy, num_battles: int = 100000):
    wins, draws, losses = 0, 0, 0

    for i in range(num_battles):
        result: Result = simulate_1v1(p0_policy, p1_policy) # type: ignore

        if result == Result.DRAW:
            draws += 1
        elif result == Result.TEAM0_WIN:
            wins += 1
        else:
            losses += 1

    print(f"Out of {num_battles} battles, team 0 had:\n{wins} wins\n{draws} draws\n{losses} losses")

if (__name__ == "__main__"):

    

    if "--get-baselines" in sys.argv:
        print("Computes the baseline results of playing the greedy & random agents against each other or themselves for 100k games.")
        if "--random-v-random" in sys.argv:
            policy0, policy1 = RandomPolicy, RandomPolicy
        elif "--greedy-v-random" in sys.argv:
            policy0, policy1 = GreedyShooterRandomPolicy, RandomPolicy
        elif "--greedy-v-greedy" in sys.argv:
            policy0, policy1 = GreedyShooterRandomPolicy, GreedyShooterRandomPolicy
        else:
            print("When using the --get-baselines command, please also add --random-v-random, --greedy-v-random, or --greedy-v-greedy")
            exit(1)

        simulate_n_battles(policy0, policy1) # type: ignore


    elif "--train-q-learning" in sys.argv:
        print("This option trains the q-learning agent for 100k battles against the given agent, then simulates 100k battles.")
        if "--q-v-random" in sys.argv:
            policy1_str = "random"
            policy1 = RandomPolicy
        elif "--q-v-greedy" in sys.argv:
            policy1_str = "greedy"
            policy1 = GreedyShooterRandomPolicy
        else:
            print("When using the --train-qlearning command, please also add --q-v-random or --q-v-greedy")
            exit(1)

        print("Beginning q-learning training.")
        policy0 = q_learn_1v1(policy1_str, 100000)

        print("Beginning battle simulations.")
        simulate_n_battles(policy0, policy1, 100000) # type: ignore
    
    else:
        print("Please use the --get-baselines or --train-qlearning options.")
        exit(1)