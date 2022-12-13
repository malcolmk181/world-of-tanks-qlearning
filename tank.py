class Tank:

    def __init__(self) -> None:
        # movement
        self.movement_speed: int = 1 # tiles per tick

        # health
        self.health: int = 10 # health points

        # gun handling
        self.reload_time: int = 3 # ticks
        self.damage_per_shot: int = 2 # health points

class TankState:

    def __init__(self, tank: Tank, position: "tuple[int, int]") -> None:
        self.tank: Tank = tank

        self.moving: bool = False
        self.in_light_cover: bool = False
        self.in_heavy_cover: bool = False

        self.time_to_reloaded: int = tank.reload_time
        self.position: tuple[int, int] = position

        self.remaining_health: int = tank.health
        self.damage_dealt_and_avoided: int = 0
        self.damage_taken: int = 0

    def ready_to_shoot(self) -> bool:
        return (not self.in_heavy_cover) and self.time_to_reloaded == 0

    def alive(self) -> bool:
        return self.remaining_health > 0

    