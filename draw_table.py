from turtle import Turtle


class Table(Turtle):
    """Draws the static green table background: outer boundary and a
    dashed center line, like a table-tennis table viewed from above."""

    def __init__(self, m, n):
        super().__init__()
        self.hideturtle()
        self.speed(0)
        self.color("white")
        self.pensize(3)
        self.m = m
        self.n = n

    def draw_table(self):
        # Draw outer rectangle (table boundary)
        self.penup()
        self.goto(-self.m // 2, -self.n // 2)
        self.pendown()
        for _ in range(2):
            self.forward(self.m)
            self.left(90)
            self.forward(self.n)
            self.left(90)

        # Draw center dividing line (net effect)
        self.penup()
        self.goto(0, -self.n // 2)
        self.pendown()
        self.setheading(90)
        for _ in range(self.n // 20):  # dashed line
            self.forward(10)
            self.penup()
            self.forward(10)
            self.pendown()
