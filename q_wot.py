from policy import Policy
from battle import Action, ActionType, Battle
from tank import Tank

TYPES_OF_ACTIONS = 4

# (in_light_cover, in_heavy_cover, ready_to_fire, moving, enemy_moving, enemy_light_cover)
State = tuple[bool, bool, bool, bool, bool, bool]

Q = tuple[State, ActionType]

def get_weight(weights: dict[Q, float], state: State, action_type: ActionType) -> float:
    if (state, action_type) in weights:
        return weights[(state, action_type)]
    else:
        weights[(state, action_type)] = 0.0
        return 0.0

def set_weight(weights: dict[Q, float], state: State, action_type: ActionType, new_weight: float) -> None:
    weights[(state, action_type)] = new_weight

def q_learn_1v1(enemy_policy: Policy, num_simulations: int = 1000, pickled_weights: None | dict[Q, float] = None) -> Policy:

    if pickled_weights:
        raise NotImplementedError("Hold on pal, we haven't built the pickle stuff yet.")

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
    weights: dict[Q, float] = {}

    # simulate num_simulations battles against the enemy policy
    for i in range(num_simulations):

        b = Battle([Tank()],[Tank()])

        while(not b.battle_is_over()):
            team0_actions, team1_actions = b.generate_all_player_actions()
            player0_actions = team0_actions[0]
            player1_actions = team1_actions[0]
            

            # replace p0_policy choice with q-learning choice
            # b.apply_all_player_actions(([p0_policy.choose_action(0,0,player0_actions)], [enemy_policy.choose_action(1,0,player1_actions)]))

        pass

    class QPolicy(Policy):
        def choose_action(self, team: int, player: int, actions: list[Action]) -> Action:
            return actions[0]

    return QPolicy # type: ignore
