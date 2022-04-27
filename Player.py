

class Player:

    def __init__(self, player_details):
        self.name = player_details[0]
        self.color = player_details[1]
        self.count = 0


    def get_player_name(self):
        return self.name


    def get_player_color(self):
        return self.color



