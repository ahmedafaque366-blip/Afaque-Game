import pygame
import sys
import random
import math

# Pygame initialize karna
pygame.init()

# Screen dimensions (Flappy bird style vertical screen)
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - GTA Style")

clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont('Impact', 26)
message_font = pygame.font.SysFont('Impact', 22)

# Bird variables
bird_x = 80
bird_y = 300
bird_vel = 0
gravity = 0.5
jump = -8
bird_width = 55
bird_height = 45

# Pipe (Pillar) variables
pipe_width = 70
pipe_gap = 180
pipe_speed = 3
pipes = []

# Timer for spawning pipes
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1400)

score = 0
high_score = 0
game_over = False
message_text = ""
message_timer = 0  # Pop-up message ke time ko track karne ke liye

# --- IMAGES LOAD KARNA ---
bg_img = None
bird_img = None
pipe_img = None

try:
    bg_img = pygame.image.load('pics/background.png').convert()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
except Exception as e:
    print("Background image load nahi ho saki:", e)

try:
    bird_img = pygame.image.load('pics/bird.png').convert()
    bird_img.set_colorkey((255, 255, 255)) # White background remove
    bird_img = pygame.transform.scale(bird_img, (bird_width, bird_height))
except Exception as e:
    print("Bird image load nahi ho saki:", e)

try:
    pipe_img = pygame.image.load('pics/pillar.png').convert_alpha()
except Exception as e:
    print("Pillar image load nahi ho saki:", e)

while True:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_vel = jump
            if event.key == pygame.K_r and game_over:
                bird_y = 300
                bird_vel = 0
                pipes.clear()
                score = 0
                message_text = ""
                message_timer = 0
                game_over = False

        if event.type == SPAWNPIPE and not game_over:
            pipe_height = random.randint(200, 450)
            bottom_pipe = pygame.Rect(WIDTH, pipe_height, pipe_width, HEIGHT - pipe_height)
            top_pipe = pygame.Rect(WIDTH, 0, pipe_width, pipe_height - pipe_gap)
            pipes.append((bottom_pipe, top_pipe))

    if not game_over:
        bird_vel += gravity
        bird_y += bird_vel
        
        # --- PERFECT HITBOXES ---
        bird_rect = pygame.Rect(bird_x + 14, bird_y + 10, bird_width - 28, bird_height - 20)

        for pipe_tuple in pipes[:]:
            bottom_pipe, top_pipe = pipe_tuple
            bottom_pipe.x -= pipe_speed
            top_pipe.x -= pipe_speed

            if bottom_pipe.x + pipe_width < 0:
                pipes.remove(pipe_tuple)
                score += 1
                
                # High score update karna
                if score > high_score:
                    high_score = score
                
                # Score 20 hone par pop-up message sirf 3 seconds (3000 ms) ke liye aayega
                if score == 20:
                    message_text = "Bhala Bhala Jawan Ja put!"
                    message_timer = current_time + 3000

            # Pipes ke hitboxes
            bottom_hitbox = pygame.Rect(bottom_pipe.x + 10, bottom_pipe.y, pipe_width - 20, bottom_pipe.height)
            top_hitbox = pygame.Rect(top_pipe.x + 10, top_pipe.y, pipe_width - 20, top_pipe.height)

            if bird_rect.colliderect(bottom_hitbox) or bird_rect.colliderect(top_hitbox):
                game_over = True
                if score < 10:
                    message_text = "Hal ta hawa lage"
                else:
                    message_text = "Hal ta hawa lage"

        if bird_y > HEIGHT - bird_height or bird_y < 0:
            game_over = True
            if score < 10:
                message_text = "Hal ta hawa lage"
            else:
                message_text = "Hal ta hawa lage"

    # Agar message ka time khatam ho jaye, toh message hata dein (jab tak game over na ho)
    if message_timer > 0 and current_time > message_timer and not game_over:
        message_text = ""
        message_timer = 0

    # --- DRAWING OBJECTS ---
    if bg_img:
        screen.blit(bg_img, (0, 0))
    else:
        screen.fill((135, 206, 235))

    for bottom_pipe, top_pipe in pipes:
        if pipe_img:
            scaled_bottom = pygame.transform.scale(pipe_img, (pipe_width, bottom_pipe.height))
            scaled_top = pygame.transform.scale(pipe_img, (pipe_width, top_pipe.height))
            screen.blit(scaled_bottom, (bottom_pipe.x, bottom_pipe.y))
            screen.blit(scaled_top, (top_pipe.x, top_pipe.y))
        else:
            pygame.draw.rect(screen, (34, 139, 34), bottom_pipe)
            pygame.draw.rect(screen, (34, 139, 34), top_pipe)

    if bird_img:
        screen.blit(bird_img, (bird_x, bird_y))
    else:
        pygame.draw.ellipse(screen, (255, 215, 0), bird_rect)

    # Score & High Score Display
    score_text = font.render(f"SCORE: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"HIGH SCORE: {high_score}", True, (255, 255, 0))
    screen.blit(score_text, (20, 20))
    screen.blit(high_score_text, (20, 50))

    # GTA Style Multi-color / Flashing Text effect for Pop-up Messages
    if message_text:
        r = int(math.sin(pygame.time.get_ticks() * 0.01) * 127 + 128)
        g = int(math.sin(pygame.time.get_ticks() * 0.01 + 2) * 127 + 128)
        b = int(math.sin(pygame.time.get_ticks() * 0.01 + 4) * 127 + 128)
        gta_color = (r, g, b)

        msg_render = message_font.render(message_text, True, gta_color)
        text_x = WIDTH // 2 - msg_render.get_width() // 2
        screen.blit(msg_render, (max(10, min(text_x, WIDTH - msg_render.get_width() - 10)), 90))

    # Game Over Screen
    if game_over:
        over_text = font.render("GAME OVER! Press 'R' to Restart", True, (255, 0, 0))
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 20))

    pygame.display.flip()
    clock.tick(60)