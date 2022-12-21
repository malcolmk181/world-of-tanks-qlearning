from battlefield import Battlefield, Position
from math import floor

class Tank:

    def __init__(self) -> None:
        # movement
        self.movement_speed: int = 1 # tiles per tick - functionally ignored

        # health
        self.health: int = 10 # health points

        # gun handling
        self.reload_time: int = 3 # ticks
        self.damage_per_shot: int = 2 # health points
        self.range: int = 4 # blocks

class TankState:

    def __init__(self, tank: Tank, position: Position, battlefield: Battlefield) -> None:
        self.tank: Tank = tank
        self.battlefield: Battlefield = battlefield

        self.time_until_reloaded: int = tank.reload_time
        self.position: Position = position
        self.last_position: Position = position

        self.remaining_health: int = tank.health
        self.damage_dealt_and_avoided: int = 0
        self.damage_taken: int = 0
        self.shots_fired: int = 0

        self.last_damage_stats: tuple[int,int] = (0,0) # Damage dealt & avoided, damage taken - from last turn

    def in_heavy_cover(self) -> bool:
        return self.battlefield.position_is_heavy_cover(self.position)

    def in_light_cover(self) -> bool:
        return self.battlefield.position_is_light_cover(self.position)

    def moving(self) -> bool:
        return self.position != self.last_position

    def ready_to_shoot(self) -> bool:
        return (not self.in_heavy_cover()) and self.time_until_reloaded == 0

    def alive(self) -> bool:
        return self.remaining_health > 0

    def position_in_range(self, position: Position) -> bool:
        # Doesn't check if position is valid.
        # Range checking is pretty inelegant, too small a board for otherwise

        distance: float = ((abs(self.position[0] - position[0]))**2 + (abs(self.position[1] - position[1]))**2)**0.5

        return int(floor(distance)) <= self.tank.range


    def take_action(self, new_position: Position, fired: bool, damage_dealt_and_avoided: int, damage_taken: int) -> None:
        self.last_position = self.position
        self.position = new_position

        if (fired):
            self.time_until_reloaded = self.tank.reload_time
            self.shots_fired += 1
        else:
            self.time_until_reloaded = max(0, self.time_until_reloaded - 1)

        self.damage_dealt_and_avoided += damage_dealt_and_avoided

        self.damage_taken += damage_taken
        self.remaining_health = max(0, self.remaining_health - damage_taken)

        self.last_damage_stats = (damage_dealt_and_avoided, damage_taken)

    def print_stats(self) -> None:
        print(f"Shots fired: {self.shots_fired}")
        print(f"Damage dealt & avoided: {self.damage_dealt_and_avoided}")
        print(f"Damage taken: {self.damage_taken}")
