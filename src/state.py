class System():
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.time = 90
        self.points_per_gum = 10
        self.points_per_super_pacgum = 50
        self.points_per_ghost = 200
        self.highscore_filename = "highscore.json"

    def update_score(self, object):
        if object == "normal":
            self.score += self.points_per_gum
        elif object == "super":
            self.score += self.points_per_super_pacgum
        elif object == "ghost":
            self.score += self.points_per_ghost

    def lose_life(self):
        self.lives -= 1

    def is_game_over(self):
        return self.lives <= 0
