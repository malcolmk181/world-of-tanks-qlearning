from policy import Policy, RandomPolicy, GreedyShooterRandomPolicy
from battle import Action, ActionType, Battle
from tank import Tank, TankState
from random import shuffle, random, choice
from itertools import repeat

# exploration value
EPSILON = 0.25

DISCOUNT_FACTOR = 0.6

INITIAL_LEARNING_RATE = 0.2

# (in_light_cover, in_heavy_cover, ready_to_shoot, moving, possible_target, enemy_moving, enemy_light_cover)
State = tuple[bool, bool, bool, bool, bool, bool, bool]

Q = tuple[State, ActionType]


def get_weight_and_learning_rate(weights: dict[Q, tuple[float, float]], state: State, action_type: ActionType) -> tuple[float, float]:
    if (state, action_type) in weights:
        return weights[(state, action_type)]
    else:
        weights[(state, action_type)] = 0.0, INITIAL_LEARNING_RATE
        return 0.0, INITIAL_LEARNING_RATE


def set_weight(weights: dict[Q, tuple[float, float]], state: State, action_type: ActionType, new_weight: float) -> None:
    # ALSO DECAYS LEARNING RATE
    _, learning_rate = weights[(state, action_type)]
    weights[(state, action_type)] = new_weight, learning_rate ** 0.99


def best_action_type(weights: dict[Q, tuple[float, float]], state: State, allowed_action_types: list[ActionType]) -> ActionType:
    shuffle(allowed_action_types)

    best_found_action_type: ActionType = allowed_action_types[0]
    best_found_reward: float = 0.0

    for action_type in allowed_action_types:
        reward, _ = get_weight_and_learning_rate(weights, state, action_type)

        if reward > best_found_reward:
            best_found_reward = reward
            best_found_action_type = action_type

    return best_found_action_type

def best_action_value(weights: dict[Q, tuple[float, float]], state: State, allowed_action_types: list[ActionType]) -> float:

    best_found_reward: float = 0.0

    for action_type in allowed_action_types:
        reward, _ = get_weight_and_learning_rate(weights, state, action_type)

        if reward > best_found_reward:
            best_found_reward = reward

    return best_found_reward

def epsilon_greedy(weights: dict[Q, tuple[float, float]], state: State, allowed_action_types: list[ActionType]) -> ActionType:
    if random() <= EPSILON:
        return choice(allowed_action_types)
    else:
        return best_action_type(weights, state, allowed_action_types)


def choose_qaction(weights: dict[Q, tuple[float, float]], state: State, actions: list[Action]) -> Action:
    allowed_action_types: list[ActionType] = list(
        set(map(lambda x: x[0], actions)))

    chosen_action_type: ActionType = epsilon_greedy(
        weights, state, allowed_action_types)

    return choice(list(filter(lambda x: x[0] == chosen_action_type, actions)))


def compute_state_from_tank_state(battle: Battle, team: int, player: int, player_state: TankState) -> State:
    # I am realizing too late that this will not scale for more than one enemy lol

    in_light_cover, in_heavy_cover, ready_to_shoot, moving, possible_target, enemy_moving, enemy_light_cover = False, False, False, False, False, False, False
    enemy_team: int = 1 if team == 0 else 0

    possible_targets = battle.possible_targets(team, player)
    if len(possible_targets) > 0:
        possible_target = True

        # just going to grab the first one - doesn't work for more than one enemy
        target_state: TankState = battle.team_states[enemy_team][possible_targets[0]]

        if target_state.moving():
            enemy_moving = True

        if target_state.in_light_cover():
            enemy_light_cover = True

    if player_state.in_light_cover():
        in_light_cover = True
    elif player_state.in_heavy_cover():
        in_heavy_cover = True

    if player_state.ready_to_shoot():
        ready_to_shoot = True

    if player_state.moving():
        moving = True

    return in_light_cover, in_heavy_cover, ready_to_shoot, moving, possible_target, enemy_moving, enemy_light_cover


def q_learn_1v1(enemy_strategy: str, num_simulations: int = 1000) -> Policy:

    # if pickled_weights:
    #     raise NotImplementedError(
    #         "Hold on pal, we haven't built the pickle stuff yet.")

    """
        what should my functional approximators be?
        - in light cover
        - in heavy cover
        - ready to fire
        - moving
        - enemy moving
        - enemy in light cover

        actions should probably just be their type:
        - move
        - move and shoot
        - shoot
        - do nothing

        this gives 64 buckets with the 4 action types each

        but not every bucket is necessarily valid, so will be less.
        since it's sparse can use a dictionary instead of a many-dimensional array
    """
    weights: dict[Q, tuple[float, float]] = {}

    # simulate num_simulations battles against the enemy policy
    for _ in repeat(None, num_simulations):

        b = Battle([Tank()], [Tank()])

        if enemy_strategy == "greedy":
            enemy_policy = GreedyShooterRandomPolicy(b)
        elif enemy_strategy == "random":
            enemy_policy = RandomPolicy(b)
        else:
            raise ValueError("Invalid policy: use 'greedy' or 'random'.")

        while (not b.battle_is_over()):
            team0_actions, team1_actions = b.generate_all_player_actions()
            player0_actions = team0_actions[0]
            player1_actions = team1_actions[0]

            player_state: TankState = b.team_states[0][0]

            # Choose & apply action
            state = compute_state_from_tank_state(b, 0, 0, player_state)
            action = choose_qaction(weights, state, player0_actions)
            b.apply_all_player_actions(([action], [enemy_policy.choose_action(1,0,player1_actions)]))

            # Observe result
            damage_dealt_and_avoided, damage_taken = player_state.last_damage_stats
            reward: int = damage_dealt_and_avoided - damage_taken

            # Update Q-values
            value, learning_rate = get_weight_and_learning_rate(weights, state, action[0])
            next_state = compute_state_from_tank_state(b, 0, 0, player_state)
            next_state_value = best_action_value(weights, next_state, list(set(map(lambda x: x[0], b.generate_all_player_actions()[0][0]))))

            new_weight: float = (1 - learning_rate) * value + learning_rate * (reward + DISCOUNT_FACTOR * next_state_value)
            set_weight(weights, state, action[0], new_weight)

    class QPolicy(Policy):
        def choose_action(self, team: int, player: int, actions: list[Action]) -> Action:
            player_state: TankState = self.battle.team_states[team][player]
            state = compute_state_from_tank_state(
                self.battle, team, player, player_state)

            return choose_qaction(weights, state, actions)

    return QPolicy  # type: ignore
