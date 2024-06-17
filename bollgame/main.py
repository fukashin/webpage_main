import pygame
import pymunk
import random
import os

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# Pymunkのスペース（物理ワールド）の設定
space = pymunk.Space()
space.gravity = (0, 900)


# 背景画像のパスを設定
background_image_path = os.path.join('assets\images', 'background2.png')
background_image = pygame.image.load(background_image_path)

# ゲームの設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 900
# 10種類のボールの色を定義
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0),
    (255, 192, 203), (75, 0, 130), (238, 130, 238), (0, 255, 255), (255, 69, 0)
]
# 10種類のボールの大きさを定義
BALL_SIZES = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65]

# ゲーム変数
balls = []
score = 0
game_over = False

# ボールを生成する関数
class Ball:
    def __init__(self, space, x, y, radius, color):
        self.radius = radius
        self.color = color
        self.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, radius))
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 0.8
        space.add(self.body, self.shape)

def create_ball(space, x, y, radius):
    color = COLORS[BALL_SIZES.index(radius)]
    return Ball(space, x, y, radius, color)

def drop_ball(space, balls, x, y):
    radius = random.choice(BALL_SIZES)
    ball = create_ball(space, x, y, radius)
    balls.append(ball)

# ボールを合体させる関数
def merge_balls(space, ball1, ball2, balls):
    global score
    new_radius = ball1.radius + 10
    if new_radius in BALL_SIZES:
        color = COLORS[BALL_SIZES.index(new_radius)]
    else:
        color = (255, 255, 255)  # デフォルト色（範囲外の大きさのボールが生成された場合）
    x, y = ball1.body.position
    space.remove(ball1.body, ball1.shape, ball2.body, ball2.shape)
    balls.remove(ball1)
    balls.remove(ball2)
    new_ball = Ball(space, x, y, new_radius, color)
    balls.append(new_ball)
    score += 10  # スコアを増加

# 衝突をチェックする関数
def check_collisions(space, balls):
    for ball in balls:
        for other in balls:
            if ball != other and ball.body.position.get_distance(other.body.position) < (ball.radius + other.radius):
                if ball.radius == other.radius:
                    merge_balls(space, ball, other, balls)

# ゲームオーバーをチェックする関数
def check_game_over(balls):
    global game_over
    for ball in balls:
        if ball.body.position.y > 600:
            game_over = True
            break

# スコアを表示する関数
def display_score(screen, score):
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

# ゲームオーバー画面を表示する関数
def display_game_over(screen):
    screen.fill((255, 255, 255))
    game_over_text = font.render('Game Over', True, (255, 0, 0))
    screen.blit(game_over_text, (300, 250))
    pygame.display.flip()

# 枠を作成する関数
def create_static_boundaries(space):
    static_lines = [
        pymunk.Segment(space.static_body, (130, 550), (660, 550), 10),  # 底辺
        pymunk.Segment(space.static_body, (140, 150), (140, 550), 10),  # 左の線
        pymunk.Segment(space.static_body, (650, 150), (650, 550), 10)   # 右の線
    ]
    for line in static_lines:
        line.elasticity = 0.8
        space.add(line)

# メインループ
create_static_boundaries(space)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            drop_ball(space, balls, x, 0)  # クリック位置のX座標からボールを落とす

    if not game_over:
        screen.blit(background_image, (0, 0))  # 背景画像を描画
        space.step(1/50.0)

        check_collisions(space, balls)
        check_game_over(balls)

        # 枠の描画
        # 底辺の線
        pygame.draw.line(screen, (0, 0, 0), (130, 550), (660, 550), 20)
        # 左の線
        pygame.draw.line(screen, (0, 0, 0), (140, 150), (140, 550), 20)
        # 右の線
        pygame.draw.line(screen, (0, 0, 0), (650, 150), (650, 550), 20)

        # ボールの描画
        for ball in balls:
            pygame.draw.circle(screen, ball.color, (int(ball.body.position.x), int(ball.body.position.y)), int(ball.radius))

        display_score(screen, score)

        pygame.display.flip()
        clock.tick(50)
    else:
        display_game_over(screen)
        pygame.time.wait(2000)
        running = False

pygame.quit()
