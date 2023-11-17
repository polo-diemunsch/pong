import pygame
import math
import random


class Button(object):
    def __init__(self, x, y, text):
        self.text = text
        self.col = (255, 255, 255)
        self.rect = pygame.Rect((0, 0), buttons_font.size(self.text))
        self.rect.center = (x, y)

    def get_clicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.col = (180, 180, 180)
            if click:
                return True
        else:
            self.col = (255, 255, 255)

        return False

    def draw(self):
        win.blit(buttons_font.render(self.text, True, self.col), self.rect)


class PressedButton(Button):
    def __init__(self, x, y, text, action):
        super().__init__(x, y, text)
        self.action = action

    def get_clicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.col = (180, 180, 180)
            if click:
                global colors_selection_scene
                colors_selection_scene = self.action
        else:
            self.col = (255, 255, 255)

        if colors_selection_scene == self.action:
            self.col = (120, 120, 120)


class Player(object):
    def __init__(self):
        self.rect = pygame.Rect((0, 0), (25, 150))
        self.col = (255, 255, 255)
        self.score = 0

    def draw(self):
        pygame.draw.rect(win, self.col, self.rect)


class Ball(object):
    def __init__(self):
        self.x, self.y = 0, 0
        self.radius = 25
        self.vel_x, self.vel_y = 0, 0
        self.col = (255, 255, 255)

    def draw(self):
        pygame.draw.circle(win, self.col, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def collide_wall(self):
        if self.y < self.radius:
            self.vel_y *= -1
            self.increase_speed()
            self.y = self.radius
        elif self.y > height - self.radius:
            self.vel_y *= -1
            self.increase_speed()
            self.y = height - self.radius

    def collide_player(self, p):
        test_x, test_y = self.x, self.y
        left, right, top, bottom = False, False, False, False

        if self.x < p.rect.left:
            test_x = p.rect.left
            left = True
        elif self.x > p.rect.right:
            test_x = p.rect.right
            right = True

        if self.y < p.rect.top:
            test_y = p.rect.top
            top = True
        elif self.y > p.rect.bottom:
            test_y = p.rect.bottom
            bottom = True

        dist_x = self.x - test_x
        dist_y = self.y - test_y
        dist = math.sqrt(dist_x**2 + dist_y**2)

        if dist < self.radius:
            if left:
                if not top and not bottom:
                    self.x = p.rect.left - self.radius
                self.vel_x = -abs(self.vel_x)
            elif right:
                if not top and not bottom:
                    self.x = p.rect.right + self.radius
                self.vel_x = abs(self.vel_x)

            if top:
                if not left and not right:
                    self.y = p.rect.top - self.radius
                self.vel_y = -abs(self.vel_y)
            elif bottom:
                if not left and not right:
                    self.y = p.rect.bottom + self.radius
                self.vel_y = abs(self.vel_y)

            self.increase_speed()

    def increase_speed(self):
        if 0 < self.vel_x < 20:
            self.vel_x += increase_speed_ball
        elif 0 > self.vel_x > -20:
            self.vel_x -= increase_speed_ball

        if 0 < self.vel_y < 20:
            self.vel_y += increase_speed_ball
        elif 0 > self.vel_y > -20:
            self.vel_y -= increase_speed_ball


def move_players():
    if not(keys[pygame.K_w] and keys[pygame.K_s]):
        if keys[pygame.K_w] and p1.rect.top >= 0:
            p1.rect.y -= player_speed
            if p1.rect.top < 0:
                p1.rect.top = 0
        elif keys[pygame.K_s] and p1.rect.bottom <= height:
            p1.rect.y += player_speed
            if p1.rect.bottom > height:
                p1.rect.bottom = height

    if not(keys[pygame.K_UP] and keys[pygame.K_DOWN]):
        if keys[pygame.K_UP] and p2.rect.top >= 0:
            p2.rect.y -= player_speed
            if p2.rect.top < 0:
                p2.rect.top = 0
        elif keys[pygame.K_DOWN] and p2.rect.bottom <= height:
            p2.rect.y += player_speed
            if p2.rect.bottom > height:
                p2.rect.bottom = height


def game_initialization():
    p1.rect.center = (50, height // 2)
    p2.rect.center = (width - 50, height // 2)
    ball.x, ball.y = width // 2, height // 2
    ball.vel_x = 0
    ball.vel_y = 0
    while -7 < abs(ball.vel_x) + abs(ball.vel_y) < 7:
        ball.vel_x = random.randint(-6, 6)
        ball.vel_y = random.randint(-6, 6)


def update_scores():
    if ball.x < -ball.radius:
        p2.score += 1
        game_initialization()
    elif ball.x > width + ball.radius:
        p1.score += 1
        game_initialization()

    if p1.score == 10 or p2.score == 10:
        global scene
        scene = 'end'
        pygame.mouse.set_visible(True)
        p1.rect.center = (175, 375)
        p2.rect.center = (width - 175, 375)
        global count
        count = 1


def draw_scores():
    temp = pygame.Rect((0, 0), scores_font.size(str(p1.score)))
    temp.center = (width // 5, 50)
    win.blit(scores_font.render(str(p1.score), True, p1.col), temp)

    temp = pygame.Rect((0, 0), scores_font.size(str(p2.score)))
    temp.center = (4 * width // 5, 50)
    win.blit(scores_font.render(str(p2.score), True, p2.col), temp)


pygame.init()

icon = pygame.image.load('pictures/icon.png')
pygame.display.set_icon(icon)

win = pygame.display.set_mode([1080, 620])

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

pygame.display.set_caption('Pong')

pygame.mouse.set_cursor((16, 19), (0, 0), (128, 0, 192, 0, 160, 0, 144, 0, 136, 0, 132, 0, 130, 0, 129, 0, 128, 128,
                                           128, 64, 128, 32, 128, 16, 129, 240, 137, 0, 148, 128, 164, 128, 194, 64, 2,
                                           64, 1, 128), (128, 0, 192, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255,
                                                         0, 255, 128, 255, 192, 255, 224, 255, 240, 255, 240, 255, 0,
                                                         247, 128, 231, 128, 195, 192, 3, 192, 1, 128))

clock = pygame.time.Clock()

buttons_font = pygame.font.Font('fonts/arialbd.ttf', 60)
scores_font = pygame.font.Font('fonts/arialbd.ttf', 75)
title_font = pygame.font.Font('fonts/Volter__28Goldfish_29.ttf', 111)

play_button = Button(width//2, 250, 'Play')
colors_selection_button = Button(width//2, 335, 'Choose colors')
controls_button = Button(width//2, 420, 'Controls')
exit_button = Button(width//2, 505, 'Exit')
menu_button = Button(width//2, 505, 'Menu')

menu_button_bis = Button(425, 550, 'Menu')
play_button_bis = Button(width-425, 550, 'Play')

all_button = PressedButton(150, 450, 'All', 'all')
ball_button = PressedButton(325, 450, 'Ball', 'ball')
p1_button = PressedButton(575, 450, 'Player 1', 'player1')
p2_button = PressedButton(850, 450, 'Player 2', 'player2')

pong_rect = pygame.Rect((0, 0), title_font.size('Pong'))
pong_rect.center = (width//2, 111)

p1_wins_rect = pygame.Rect((0, 0), title_font.size('Player 1 wins !'))
p1_wins_rect.center = (width//2, 135)
p2_wins_rect = pygame.Rect((0, 0), title_font.size('Player 2 wins !'))
p2_wins_rect.center = (width//2, 135)

p1_controls = pygame.image.load('pictures/p1_controls.png').convert_alpha()
p1_controls_rect = p1_controls.get_rect()
p1_controls_rect.center = (270, 125)
p2_controls = pygame.image.load('pictures/p2_controls.png').convert_alpha()
p2_controls_rect = p2_controls.get_rect()
p2_controls_rect.center = (750, 400)

color_picker = pygame.image.load('pictures/color_picker.png').convert_alpha()
color_picker = pygame.transform.scale(color_picker, (round(234*1.4), round(199*1.4)))
color_picker_rect = color_picker.get_rect()
color_picker_rect.center = (325, 225)

p1 = Player()
p2 = Player()

ball = Ball()

player_speed = 10
increase_speed_ball = 1

scene = 'menu'
colors_selection_scene = 'all'

running = True

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # or keys[pygame.K_ESCAPE]:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True
        else:
            click = False

    win.fill((0, 0, 0))

    if scene == 'menu':
        if play_button.get_clicked():
            scene = 'game'
            game_initialization()
            p1.score = 0
            p2.score = 0
            pygame.mouse.set_visible(False)
        if colors_selection_button.get_clicked():
            scene = 'colors selection'
            p1.rect.center = (640, 225)
            p2.rect.center = (940, 225)
            ball.x, ball.y = 790, 225
            colors_selection_scene = 'all'
            click = False
        if controls_button.get_clicked():
            scene = 'controls'
            p1.rect.center = (50, height // 2)
            p2.rect.center = (width - 50, height // 2)
        if exit_button.get_clicked():
            running = False

        play_button.draw()
        colors_selection_button.draw()
        controls_button.draw()
        exit_button.draw()

        win.blit(title_font.render('Pong', True, (255, 255, 255)), pong_rect)

    elif scene == 'colors selection':
        if menu_button_bis.get_clicked():
            scene = 'menu'
            click = False
        if play_button_bis.get_clicked():
            scene = 'game'
            game_initialization()
            p1.score = 0
            p2.score = 0
            pygame.mouse.set_visible(False)

        all_button.get_clicked()
        ball_button.get_clicked()
        p1_button.get_clicked()
        p2_button.get_clicked()

        menu_button_bis.draw()
        play_button_bis.draw()
        all_button.draw()
        ball_button.draw()
        p1_button.draw()
        p2_button.draw()

        win.blit(color_picker, color_picker_rect)

        if colors_selection_scene == 'all':
            if color_picker_rect.collidepoint(pygame.mouse.get_pos()) and click:
                color = win.get_at(pygame.mouse.get_pos())
                if color != (0, 0, 0):
                    p1.col = color
                    p2.col = color
                    ball.col = color

            p1.draw()
            p2.draw()
            ball.draw()

        elif colors_selection_scene == 'ball':
            if color_picker_rect.collidepoint(pygame.mouse.get_pos()) and click:
                color = win.get_at(pygame.mouse.get_pos())
                if color != (0, 0, 0):
                    ball.col = color

            ball.draw()

        elif colors_selection_scene == 'player1':
            if color_picker_rect.collidepoint(pygame.mouse.get_pos()) and click:
                color = win.get_at(pygame.mouse.get_pos())
                if color != (0, 0, 0):
                    p1.col = color

            p1.draw()

        elif colors_selection_scene == 'player2':
            if color_picker_rect.collidepoint(pygame.mouse.get_pos()) and click:
                color = win.get_at(pygame.mouse.get_pos())
                if color != (0, 0, 0):
                    p2.col = color

            p2.draw()

    elif scene == 'controls':
        move_players()

        if menu_button_bis.get_clicked():
            scene = 'menu'
            click = False
        if play_button_bis.get_clicked():
            scene = 'game'
            game_initialization()
            p1.score = 0
            p2.score = 0
            pygame.mouse.set_visible(False)

        p1.draw()
        p2.draw()
        menu_button_bis.draw()
        play_button_bis.draw()
        win.blit(p1_controls, p1_controls_rect)
        win.blit(p2_controls, p2_controls_rect)

    elif scene == 'game':
        move_players()
        ball.move()

        ball.collide_wall()
        ball.collide_player(p1)
        ball.collide_player(p2)

        update_scores()

        draw_scores()
        p1.draw()
        p2.draw()
        ball.draw()

    elif scene == 'end':
        if play_button.get_clicked():
            scene = 'game'
            game_initialization()
            p1.score = 0
            p2.score = 0
            pygame.mouse.set_visible(False)
        if colors_selection_button.get_clicked():
            scene = 'colors selection'
            p1.rect.center = (640, 225)
            p2.rect.center = (940, 225)
            ball.x, ball.y = 790, 225
            colors_selection_scene = 'all'
            click = False
        if controls_button.get_clicked():
            scene = 'controls'
            p1.rect.center = (50, height // 2)
            p2.rect.center = (width - 50, height // 2)
        if menu_button.get_clicked():
            scene = 'menu'
            click = False

        play_button.draw()
        colors_selection_button.draw()
        controls_button.draw()
        menu_button.draw()

        draw_scores()

        if p1.score == 10:
            p1.draw()
            if count <= 50:
                win.blit(title_font.render('Player 1 wins !', True, p1.col), p1_wins_rect)
        elif p2.score == 10:
            p2.draw()
            if count <= 50:
                win.blit(title_font.render('Player 2 wins !', True, p2.col), p2_wins_rect)

        if count == 100:
            count = 0

        count += 1

    pygame.display.update()
    clock.tick(60)

pygame.quit()
