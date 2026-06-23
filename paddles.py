from turtle import Turtle

MAX_Y = 280  # keep the paddle inside the table boundary drawn in draw_table.py


class paddles(Turtle):
    """A paddle, controllable either by keyboard or by the simple AI
    in ai_move()."""

    def __init__(self, x, y):
        super().__init__()

        self.color("red")
        self.shape("square")
        self.shapesize(stretch_wid=6, stretch_len=1)
        self.penup()
        self.goto(x, y)
        self.start_x = x

    def go_up(self, step=50):
        new_y = min(self.ycor() + step, MAX_Y)
        self.goto(self.xcor(), new_y)

    def go_down(self, step=50):
        new_y = max(self.ycor() - step, -MAX_Y)
        self.goto(self.xcor(), new_y)

    def ai_move(self, ball, speed=20, deadzone=15):
        """Very simple AI: chase the ball's y-position at a limited
        speed, with a small deadzone so it doesn't jitter. Tune `speed`
        up for a harder opponent, down for an easier one.
        """
        diff = ball.ycor() - self.ycor()
        if diff > deadzone:
            self.go_up(speed)
        elif diff < -deadzone:
            self.go_down(speed)

    def reset_position(self):
        """Used when restarting the game."""
        self.goto(self.start_x, 0)
