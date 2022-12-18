from battlefield import Battlefield, Position

class Tank:

    def __init__(self) -> None:
        # movement
        self.movement_speed: int = 1 # tiles per tick - functionally ignored

        # health
        self.health: int = 10 # health points

        # gun handling
        self.reload_time: int = 3 # ticks
        self.damage_per_shot: int = 2 # health points

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

    def take_action(self, new_position: Position, fired: bool, damage_dealt_and_avoided: int, damage_taken: int):
        self.last_position = self.position
        self.position = new_position

        if (fired):
            self.time_until_reloaded = self.tank.reload_time
        else:
            self.time_until_reloaded = max(0, self.time_until_reloaded - 1)

        self.damage_dealt_and_avoided += damage_dealt_and_avoided

        self.damage_taken += damage_taken
        self.remaining_health = max(0, self.remaining_health - damage_taken)