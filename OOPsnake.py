import turtle
import time
import random

DELAY = .05
STEP = 20

window = turtle.Screen()
window.title("Snake by Johnson")
window.bgcolor('green')
window.setup(width=300, height=300)
window.tracer(0)

pen = turtle.Turtle()
pen.speed(1)
pen.shape('square')
pen.color('white')
pen.penup()
pen.hideturtle()
pen.goto(0, 240)


class Player(turtle.Turtle):
    player_instances = []
    def __init__(self, shape, color, x, y, multi):
        super().__init__()
        self.speed(0)
        self.shape(shape)
        self.color(color)
        self.penup()
        self.direction = 'stop'
        self.settiltangle(90)
        self.shapesize(2, 4)
        self.goto(x, y)
        self.segments = []
        self.multi = multi
        self.lives = 3
        Player.player_instances.append(self)
    def go_up(self):
        if self.direction != 'down' or len(self.segments) == 0:
            self.settiltangle(90)
            self.direction = 'up'
    def go_down(self):
        if self.direction != 'up' or len(self.segments) == 0:
            self.settiltangle(270)
            self.direction = 'down'
    def go_right(self):
        if self.direction != 'left' or len(self.segments) == 0:
            self.settiltangle(0)
            self.direction = 'right'
    def go_left(self):
        if self.direction != 'right' or len(self.segments) == 0:
            self.settiltangle(180)
            self.direction = 'left'
    def directions(self):
        if self.multi == 1:
            window.onkeypress(self.go_up, 'w')
            window.onkeypress(self.go_down, 's')
            window.onkeypress(self.go_right, 'd')
            window.onkeypress(self.go_left, 'a')
        elif self.multi == 2:
            window.onkeypress(self.go_up, 'o')
            window.onkeypress(self.go_down, 'l')
            window.onkeypress(self.go_right, ';')
            window.onkeypress(self.go_left, 'k')
    def move(self):
        if self.direction == 'up':
            y = self.ycor()
            self.sety(y + STEP)
        if self.direction == 'down':
            y = self.ycor()
            self.sety(y - STEP)
        if self.direction == 'right':
            x = self.xcor()
            self.setx(x + STEP)
        if self.direction == 'left':
            x = self.xcor()
            self.setx(x - STEP)


class Segment(turtle.Turtle):
    def __init__(self, player):
        super().__init__()
        self.speed(0)
        self.shape('circle')
        self.penup()
        self.shapesize(2, 2)
        if player.multi == 1:
            self.color('skyblue')
        elif player.multi == 2:
            self.color('yellow')
    def add(self, player):
        player.segments.append(self)


class Snack(turtle.Turtle):
    snack_instances = []
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.shape('square')
        self.color('red')
        self.penup()
        self.shapesize(2, 2)
        Snack.snack_instances.append(self)
    def snack_position(self):
        x_snack = random.randrange(-620, 620, 40)
        y_snack = random.randrange(-340, 340, 40)
        self.goto(x_snack, y_snack)


def stop():
    time.sleep(1)
    for player in Player.player_instances:
        player.direction = 'stop'
        for seg in player.segments:
            seg.goto(1000,1000)
        player.segments.clear()
    player1.goto(0, 80)
    player2.goto(0, -80)

player1 = Player('arrow', 'blue', 0, 80, 1)
player2 = Player('arrow', 'orange', 0, -80, 2)
game_snack = Snack()
game_snack2 = Snack()
game_snack.snack_position()
game_snack2.snack_position()

def scoreboard():
    pen.clear()
    pen.write(f'Blue lives: {player1.lives}  Yellow lives:  {player2.lives}', align='center', font=('Courier', 24, 'normal'))

window.listen()
player1.directions()
player2.directions()

while True:
    window.update()
    scoreboard()
    for player in Player.player_instances:
        for snack in Snack.snack_instances:
            if player.distance(snack) < STEP * 2:
                body_segment = Segment(player)
                player.segments.append(body_segment)
                snack.snack_position()
    for player in Player.player_instances:
        for index in range(len(player.segments)-1, 0, -1):
            x = player.segments[index - 1].xcor()
            y = player.segments[index - 1].ycor()
            player.segments[index].goto(x, y)
        if len(player.segments) > 0:
            x = player.xcor()  # .xcor() is a method that returns the current coordinate of the object class
            y = player.ycor()
            player.segments[0].goto(x, y)
    for player in Player.player_instances:  # move happens after segment so the segment goes to player head
        player.move()                       # then player moves, and then checks distance between the two
    for player in Player.player_instances:
        if player.xcor() > 640 or player.xcor() < -640 or player.ycor() > 340 or player.ycor() < -340:
            player.lives -= 1
            stop()
        for segment in player.segments:
            if segment.distance(player) < STEP:
                player.lives -= 1
                stop()
    for segment in player1.segments:
        if segment.distance(player2) < STEP * 2:
            player2.lives -= 1
            stop()
    for segment in player2.segments:
        if segment.distance(player1) < STEP * 2:
            player1.lives -= 1
            stop()
    time.sleep(DELAY)

window.mainloop()
