from turtle import Turtle
import random as rand


class Ball(Turtle):
    """The ball that bounces between paddles and walls.

    Includes a simple difficulty system: every time a point is scored
    and the ball resets, its speed increases slightly (capped at
    MAX_SPEED) so rallies get progressively more challenging.
    """

    BASE_SPEED = 3        # starting speed magnitude on each axis
    MAX_SPEED = 9          # speed cap so the game stays playable
    SPEED_GROWTH = 1.08    # multiplier applied after every point

    def __init__(self):
        super().__init__()
        self.color("yellow")
        self.shape("circle")
        self.penup()
        self.increase_x = self.BASE_SPEED
        self.increase_y = self.BASE_SPEED

    def move(self):
        new_x = self.xcor() + self.increase_x
        new_y = self.ycor() + self.increase_y
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.increase_y *= -1

    def bounce_x(self):
        self.increase_x *= -1

    def increase_difficulty(self):
        """Speed the ball up a little, capped at MAX_SPEED."""
        if abs(self.increase_x) < self.MAX_SPEED:
            self.increase_x *= self.SPEED_GROWTH
            self.increase_y *= self.SPEED_GROWTH
            self.increase_x = max(-self.MAX_SPEED, min(self.MAX_SPEED, self.increase_x))
            self.increase_y = max(-self.MAX_SPEED, min(self.MAX_SPEED, self.increase_y))

    def reset(self):
        """Called after a point is scored: re-centers the ball and
        bumps the difficulty up a notch."""
        self.goto(0, 0)
        self.bounce_x()
        if rand.choice([True, False]):
            self.bounce_y()
        self.increase_difficulty()

    def reset_speed(self):
        """Used on a full game restart to bring difficulty back to the start,
        keeping whatever direction the ball currently happens to be facing."""
        sign_x = 1 if self.increase_x >= 0 else -1
        sign_y = 1 if self.increase_y >= 0 else -1
        self.increase_x = self.BASE_SPEED * sign_x
        self.increase_y = self.BASE_SPEED * sign_y
