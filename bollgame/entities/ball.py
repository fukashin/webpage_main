import random
import pymunk
from settings import COLORS, BALL_SIZES

def create_ball(space, x, y, radius):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, radius))
    body.position = x, y
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.8
    shape.color = random.choice(COLORS)
    space.add(body, shape)
    return shape

def drop_ball(space, balls):
    radius = random.choice(BALL_SIZES)
    x = random.randint(radius, 800 - radius)
    ball = create_ball(space, x, 0, radius)
    balls.append(ball)
