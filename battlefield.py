MAX_PLAYERS_PER_TEAM = 2

class Battlefield:
    
    def __init__(self, team1_size: int, team2_size: int, board_size: "tuple[int,int]" = (3,9)):
        if (team1_size > MAX_PLAYERS_PER_TEAM or team2_size > MAX_PLAYERS_PER_TEAM):
            raise ValueError(f"Too many players given. Max players per team: {MAX_PLAYERS_PER_TEAM}")

        if (team1_size == 0 or team2_size == 0):
            raise ValueError(f"Each team must have at least one player. Max players per team: {MAX_PLAYERS_PER_TEAM}")

        if (board_size != (3,9)):
            raise ValueError("Board sizes other than (3,9) are not yet implemented.")

        self.team1_size = team1_size
        self.team2_size = team2_size

        self.board_size = board_size

        self.light_cover_positions = ((0,2),(0,4),(1,2),(1,6),(2,4),(2,6))
        self.heavy_cover_positions = ((0,5),(1,4),(2,3))

        self.team1_starting_positions = ((1,0)) if team1_size == 1 else ((0,0),(2,0))
        self.team2_starting_positions = ((8,0)) if team2_size == 1 else ((0,8),(2,8))

    def position_is_in_bounds(self, position: "tuple[int,int]") -> bool:
        if (position[0] >= 0 and position[0] < self.board_size[0] and \
            position[1] >= 0 and position[1] < self.board_size[1]):
            return True
        else:
            return False
    
    def position_is_light_cover(self, position: "tuple[int,int]") -> bool:
        return position in self.light_cover_positions

    def position_is_heavy_cover(self, position: "tuple[int,int]") -> bool:
        return position in self.heavy_cover_positions