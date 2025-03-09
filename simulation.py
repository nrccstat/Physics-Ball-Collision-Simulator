import pygame
import math
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)  
RADIUS = 290  
FPS = 60  

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Collision Simulation")

font = pygame.font.SysFont(None, 24)

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.handle_rect = pygame.Rect(x, y - 10, 10, height + 20)
        self.set_value(initial_val)
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)  
        pygame.draw.rect(screen, RED, self.handle_rect)  

    def get_value(self):
        range_width = self.rect.width - self.handle_rect.width
        if range_width > 0:
            fraction = (self.handle_rect.x - self.rect.x) / range_width
        else:
            fraction = 0
        return self.min_val + fraction * (self.max_val - self.min_val)

    def set_value(self, value):
        fraction = (value - self.min_val) / (self.max_val - self.min_val)
        self.handle_rect.x = self.rect.x + fraction * (self.rect.width - self.handle_rect.width)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_x = event.pos[0] - self.handle_rect.width / 2
            self.handle_rect.x = max(self.rect.x, min(new_x, self.rect.x + self.rect.width - self.handle_rect.width))

class Ball:
    def __init__(self, x, y, vx, vy, r, color, e):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.r = float(r)
        self.color = color
        self.e = float(e)
        self.m = r ** 2  


def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def normalize(v):
    mag = math.hypot(v[0], v[1])
    return (v[0] / mag, v[1] / mag) if mag != 0 else (0, 0)

def get_random_position(ball_radius):
    angle = random.uniform(0, 2 * math.pi)
    dist = math.sqrt(random.uniform(0, 1)) * (RADIUS - ball_radius)
    x = CENTER[0] + dist * math.cos(angle)
    y = CENTER[1] + dist * math.sin(angle)
    return x, y


radius_slider = Slider(10, 10, 200, 10, 1, 25, 10)  
vx_slider = Slider(10, 50, 200, 10, -30, 30, 0)     
vy_slider = Slider(10, 90, 200, 10, -30, 30, 0)     
e_slider = Slider(10, 130, 200, 10, 0.8, 1, 0.9)   

color_buttons = [pygame.Rect(10, 170, 30, 30), pygame.Rect(50, 170, 30, 30), pygame.Rect(90, 170, 30, 30)]
colors = [RED, GREEN, BLUE]
current_color = RED
selected_color_index = 0

add_ball_button = pygame.Rect(10, 210, 100, 30)


balls = []

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for slider in [radius_slider, vx_slider, vy_slider, e_slider]:
                slider.handle_event(event)
            for i, button in enumerate(color_buttons):
                if button.collidepoint(event.pos):
                    current_color = colors[i]
                    selected_color_index = i
                    break
            else:
                if add_ball_button.collidepoint(event.pos):
                    current_radius = radius_slider.get_value()
                    current_vx = vx_slider.get_value()
                    current_vy = vy_slider.get_value()
                    current_e = e_slider.get_value()
                    x, y = get_random_position(current_radius)
                    ball = Ball(x, y, current_vx, current_vy, current_radius, current_color, current_e)
                    balls.append(ball)
                else:
                    for ball in balls[:]:
                        if distance(event.pos, (ball.x, ball.y)) < ball.r:
                            balls.remove(ball)
                            break
        elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
            for slider in [radius_slider, vx_slider, vy_slider, e_slider]:
                slider.handle_event(event)

    for ball in balls:
        ball.x += ball.vx
        ball.y += ball.vy
       

    for ball in balls:
        dist = distance((ball.x, ball.y), CENTER)
        if dist >= RADIUS - ball.r:
            n = normalize((ball.x - CENTER[0], ball.y - CENTER[1]))
            v_dot_n = ball.vx * n[0] + ball.vy * n[1]
            ball.vx -= (1 + ball.e) * v_dot_n * n[0]
            ball.vy -= (1 + ball.e) * v_dot_n * n[1]

    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            ball1 = balls[i]
            ball2 = balls[j]
            dx = ball2.x - ball1.x
            dy = ball2.y - ball1.y
            dist = math.hypot(dx, dy)
            if dist <= ball1.r + ball2.r:
                n = (dx / dist, dy / dist) if dist != 0 else (1, 0)
                v_rel_x = ball2.vx - ball1.vx
                v_rel_y = ball2.vy - ball1.vy
                v_rel_n = v_rel_x * n[0] + v_rel_y * n[1]
                if v_rel_n < 0:  
                    e = (ball1.e + ball2.e) / 2  
                    J = (1 + e) * v_rel_n / (1 / ball1.m + 1 / ball2.m)
                    ball1.vx += (J / ball1.m) * n[0]
                    ball1.vy += (J / ball1.m) * n[1]
                    ball2.vx -= (J / ball2.m) * n[0]
                    ball2.vy -= (J / ball2.m) * n[1]

    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, CENTER, RADIUS, 1)  
    for slider in [radius_slider, vx_slider, vy_slider, e_slider]:
        slider.draw(screen)

    for i, button in enumerate(color_buttons):
        pygame.draw.rect(screen, colors[i], button)
        if i == selected_color_index:
            pygame.draw.rect(screen, WHITE, button, 2)  

    pygame.draw.rect(screen, WHITE, add_ball_button)
    text = font.render("Add Ball", True, BLACK)
    screen.blit(text, (20, 215))

   
    labels = ["Radius:", "Vx:", "Vy:", "Bounciness:"]
    sliders = [radius_slider, vx_slider, vy_slider, e_slider]
    for i, label in enumerate(labels):
        text = font.render(label, True, WHITE)
        screen.blit(text, (220, 10 + i * 40))
        value = sliders[i].get_value()
        value_text = font.render(f"{value:.2f}", True, WHITE)
        screen.blit(value_text, (300, 10 + i * 40))


    for ball in balls:
        pygame.draw.circle(screen, ball.color, (int(ball.x), int(ball.y)), int(ball.r))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
