from turtle import Turtle, Screen
from paddles import paddles
from ball import Ball
import time
from scoreboard import scoreboard
from draw_table import Table
from sound_manager import SoundManager

m = 800
n = 600

# Screen Setup
screen = Screen()
screen.bgcolor("green")  # table tennis surface
screen.setup(width=m, height=n)
screen.title("Ping Pong Game by NSHL")
screen.tracer(0)

# Draw table tennis background
table = Table(m, n)
table.draw_table()

left_pads = paddles(-350, 0)    # human-controlled (W / S)
right_pads = paddles(350, 0)    # AI-controlled
playing_ball = Ball()
scoreboard = scoreboard()       # create scoreboard object
sound = SoundManager()

# Small turtle used to show "PAUSED" / instructions in the middle of the table
status = Turtle()
status.hideturtle()
status.penup()
status.color("white")

game_paused = False


def show_status(message):
    status.clear()
    status.goto(0, 0)
    status.write(message, align="center", font=("Courier", 22, "bold"))


def toggle_pause():
    global game_paused
    game_paused = not game_paused
    if game_paused:
        show_status("PAUSED\n\nspace = resume   r = restart")
        sound.pause_music()
    else:
        status.clear()
        sound.unpause_music()


def restart_game():
    global game_paused
    game_paused = False
    status.clear()
    scoreboard.reset_score()
    playing_ball.goto(0, 0)
    playing_ball.reset_speed()
    left_pads.reset_position()
    right_pads.reset_position()
    sound.stop_music()
    sound.play_music()


# Keyboard Bindings
screen.listen()

# Left Paddle Controls (W and S Keys) - the right paddle is now AI-controlled
screen.onkey(left_pads.go_up, "w")
screen.onkey(left_pads.go_down, "s")

# Game controls
screen.onkey(toggle_pause, "space")
screen.onkey(restart_game, "r")

sound.play_music()

# Game Loop
while True:
    time.sleep(0.02)
    screen.update()

    if game_paused:
        continue

    playing_ball.move()
    right_pads.ai_move(playing_ball)

    # Bounce off top/bottom walls
    if playing_ball.ycor() > 280 or playing_ball.ycor() < -280:
        playing_ball.bounce_y()
        sound.play_wall()

    # Paddle collisions
    if playing_ball.xcor() > 340 and playing_ball.distance(right_pads) < 50:
        playing_ball.bounce_x()
        sound.play_hit()

    if playing_ball.xcor() < -340 and playing_ball.distance(left_pads) < 50:
        playing_ball.bounce_x()
        sound.play_hit()

    # Ball goes past left paddle: right player scores
    if playing_ball.xcor() < -380:
        playing_ball.reset()
        scoreboard.right_point()
        sound.play_score()

    # Ball goes past right paddle: left player scores
    if playing_ball.xcor() > 380:
        playing_ball.reset()
        scoreboard.left_point()
        sound.play_score()

screen.exitonclick()
