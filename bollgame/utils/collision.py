from entities.ball import create_ball

def merge_balls(space, ball1, ball2, balls, score):
    new_radius = ball1.radius + 10
    x, y = ball1.body.position
    space.remove(ball1.body, ball1, ball2.body, ball2)
    balls.remove(ball1)
    balls.remove(ball2)
    new_ball = create_ball(space, x, y, new_radius)
    balls.append(new_ball)
    score += 10  # スコアを増加
    return score

def check_collisions(space, balls, score):
    for ball in balls:
        for other in balls:
            if ball != other and ball.body.position.get_distance(other.body.position) < (ball.radius + other.radius):
                if ball.radius == other.radius:
                    score = merge_balls(space, ball, other, balls, score)
    return score

def check_game_over(balls):
    for ball in balls:
        if ball.body.position.y > 600:
            return True
    return False
