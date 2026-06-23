from turtle import Turtle


class scoreboard(Turtle):
    """Tracks and displays the score for both players."""

    def __init__(self):
        super().__init__()
        self.color("black")
        self.penup()
        self.hideturtle()
        self.player_left = 0
        self.player_right = 0
        self.update_score()

    def update_score(self):
        self.clear()
        # Left player score
        self.goto(-100, 200)
        self.write(self.player_left, align="center", font=("Courier", 24, "normal"))
        # Right player score
        self.goto(100, 200)
        self.write(self.player_right, align="center", font=("Courier", 24, "normal"))

    def left_point(self):
        self.player_left += 1
        self.update_score()

    def right_point(self):
        self.player_right += 1
        self.update_score()

    def reset_score(self):
        """Used when restarting the game."""
        self.player_left = 0
        self.player_right = 0
        self.update_score()
