MAX_PLAYERS_PER_TEAM = 2

Position = tuple[int,int]

class Battlefield:
    
    def __init__(self, team0_size: int, team1_size: int, board_size: Position = (3,9)):
        if (team0_size > MAX_PLAYERS_PER_TEAM or team1_size > MAX_PLAYERS_PER_TEAM):
            raise ValueError(f"Too many players given. Max players per team: {MAX_PLAYERS_PER_TEAM}")

        if (team0_size == 0 or team1_size == 0):
            raise ValueError(f"Each team must have at least one player. Max players per team: {MAX_PLAYERS_PER_TEAM}")

        if (board_size != (3,9)):
            raise ValueError("Board sizes other than (3,9) are not yet implemented.")

        self.team_sizes: tuple[int,int] = (team0_size, team1_size)

        self.board_size = board_size

        self.light_cover_positions: list[Position] = [(0,2),(0,4),(1,2),(1,6),(2,4),(2,6)]
        self.heavy_cover_positions: list[Position] = [(0,5),(1,4),(2,3)]

        team0_starting_positions: list[Position] = [(1,0)] if team0_size == 1 else [(0,0),(2,0)]
        team1_starting_positions: list[Position] = [(0,8)] if team1_size == 1 else [(0,8),(2,8)]
        self.team_starting_positions: tuple[list[Position], list[Position]] = (team0_starting_positions, team1_starting_positions)

    def position_is_in_bounds(self, position: Position) -> bool:
        if (position[0] >= 0 and position[0] < self.board_size[0] and \
            position[1] >= 0 and position[1] < self.board_size[1]):
            return True
        else:
            return False
    
    def position_is_light_cover(self, position: Position) -> bool:
        return position in self.light_cover_positions

    def position_is_heavy_cover(self, position: Position) -> bool:
        return position in self.heavy_cover_positions

    def possible_positions(self, position: Position) -> list[Position]:
        if (not self.position_is_in_bounds(position)):
            raise ValueError("Illegal position.")

        positions: list[Position] = []

        for x in range(-1,2):
            for y in range(-1,2):
                potential_position: Position = (position[0] + x,position[1] + y)
                if self.position_is_in_bounds(potential_position):
                    positions.append(potential_position)

        return positions