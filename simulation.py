import pygame
import math
import random
import sys
import numpy as np

GRAVITY = 0.5  
FRICTION = 0.995  

pygame.init()

WIDTH, HEIGHT = 800, 600
RADIUS = 220  
CENTER = (WIDTH - RADIUS - 5, HEIGHT - RADIUS - 5)  
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
        self.trail = []  
        self.flash_timer = 0 

    def update_trail(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 15:
            self.trail.pop(0)

    def flash(self):
        self.flash_timer = 5 

    def draw(self, screen):
       
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i + 1) / len(self.trail)) if self.trail else 0
            trail_color = (*self.color, alpha)
            s = pygame.Surface((self.r*2, self.r*2), pygame.SRCALPHA)
            pygame.draw.circle(s, trail_color, (int(self.r), int(self.r)), int(self.r))
            screen.blit(s, (pos[0] - self.r, pos[1] - self.r))
        
        if self.flash_timer > 0:
            color = WHITE
            self.flash_timer -= 1
        else:
            color = self.color
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.r))
        
        speed = math.hypot(self.vx, self.vy)
        if not math.isfinite(speed) or speed > 1e4:
            speed = 0.0
        label = font.render(f"{speed:.1f}", True, WHITE)
        screen.blit(label, (int(self.x) - label.get_width() // 2, int(self.y) - int(self.r) - 15))

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
e_slider = Slider(10, 130, 200, 10, 0.8, 1.01, 0.98)   

color_buttons = [pygame.Rect(10, 170, 30, 30), pygame.Rect(50, 170, 30, 30), pygame.Rect(90, 170, 30, 30)]
colors = [RED, GREEN, BLUE]
current_color = RED
selected_color_index = 0

add_ball_button = pygame.Rect(10, 210, 100, 30)


balls = []

clock = pygame.time.Clock()
running = True

while running:
    
   
    if balls:
        positions = np.array([[ball.x, ball.y] for ball in balls])
        velocities = np.array([[ball.vx, ball.vy] for ball in balls])
        velocities[:, 1] += GRAVITY  
        velocities *= FRICTION       
        positions += velocities     
        for i, ball in enumerate(balls):
            ball.x, ball.y = positions[i]
            ball.vx, ball.vy = velocities[i]
        speeds = np.linalg.norm(velocities, axis=1)
        avg_speed = np.mean(speeds)
    else:
        avg_speed = 0.0

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
        ball.update_trail()
        dist_to_center = distance((ball.x, ball.y), CENTER)
        if dist_to_center > RADIUS - ball.r:
            n = normalize((ball.x - CENTER[0], ball.y - CENTER[1]))
            ball.x = CENTER[0] + n[0] * (RADIUS - ball.r)
            ball.y = CENTER[1] + n[1] * (RADIUS - ball.r)
            v_dot_n = ball.vx * n[0] + ball.vy * n[1]
            ball.vx -= (1 + ball.e) * v_dot_n * n[0]
            ball.vy -= (1 + ball.e) * v_dot_n * n[1]
        dist_to_center = distance((ball.x, ball.y), CENTER)
        if dist_to_center > RADIUS - ball.r:
            n = normalize((ball.x - CENTER[0], ball.y - CENTER[1]))
            ball.x = CENTER[0] + n[0] * (RADIUS - ball.r)
            ball.y = CENTER[1] + n[1] * (RADIUS - ball.r)

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
                n = (dx / dist, dy / dist) if dist > 1e-8 else (1, 0) 
                v_rel_x = ball2.vx - ball1.vx
                v_rel_y = ball2.vy - ball1.vy
                v_rel_n = v_rel_x * n[0] + v_rel_y * n[1]
                if v_rel_n < 0:  
                    e = (ball1.e + ball2.e) / 2  
                    denom = (1 / ball1.m + 1 / ball2.m)
                    if denom < 1e-8:
                        denom = 1e-8
                    J = (1 + e) * v_rel_n / denom
                    ball1.vx += (J / ball1.m) * n[0]
                    ball1.vy += (J / ball1.m) * n[1]
                    ball2.vx -= (J / ball2.m) * n[0]
                    ball2.vy -= (J / ball2.m) * n[1]
                    ball1.flash()
                    ball2.flash()

    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, CENTER, RADIUS, 1)  
    panel_width = 370
    panel_height = 260
    panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
    pygame.draw.rect(screen, (30, 30, 30), panel_rect, border_radius=12)
    pygame.draw.rect(screen, WHITE, panel_rect, 2, border_radius=12)

    labels = ["Radius:", "Vx:", "Vy:", "Bounciness:"]
    sliders = [radius_slider, vx_slider, vy_slider, e_slider]
    for i, (label, slider) in enumerate(zip(labels, sliders)):
        y = 25 + i * 50
        slider.rect.y = y
        slider.handle_rect.y = y - 10
        slider.draw(screen)
        text = font.render(label, True, WHITE)
        screen.blit(text, (slider.rect.right + 15, y - 2))
        value = slider.get_value()
        value_text = font.render(f"{value:.2f}", True, WHITE)
        screen.blit(value_text, (slider.rect.right + 120, y - 2))

    color_buttons_y = 25 + 4 * 50 - 5  
    for i, button in enumerate(color_buttons):
        button.y = color_buttons_y
        button.x = 10 + i * 40
        pygame.draw.rect(screen, colors[i], button, border_radius=6)
        if i == selected_color_index:
            pygame.draw.rect(screen, WHITE, button, 3, border_radius=6)
        else:
            pygame.draw.rect(screen, (80, 80, 80), button, 1, border_radius=6)

    add_ball_button.x = 10
    add_ball_button.y = color_buttons_y + 45
    pygame.draw.rect(screen, WHITE, add_ball_button, border_radius=8)
    text = font.render("Add Ball", True, BLACK)
    text_rect = text.get_rect(center=add_ball_button.center)
    screen.blit(text, text_rect)

    stats_font = pygame.font.SysFont(None, 32, bold=True)
    stats_text = stats_font.render(f"Balls: {len(balls)}", True, WHITE)
    screen.blit(stats_text, (WIDTH - 160, 15))

    avg_speed_text = font.render(f"Avg Speed: {avg_speed:.2f}", True, WHITE)
    screen.blit(avg_speed_text, (WIDTH - 200, 50))

    for ball in balls:
        ball.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
