# setup
from setup.setup import *

# radar geometry
CX = W // 2
CY = H - 80
R  = 460

# data
trail = []

# helpers
def to_xy(a, d_px):
    rad = math.radians(a)
    return (int(CX - math.cos(rad) * d_px),
            int(CY - math.sin(rad) * d_px))

def d_to_px(d_cm):
    return (d_cm / MAX_DIST) * R

def draw_circle_alpha(surf, colour, centre, radius):
    s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(s, colour, (radius, radius), radius)
    surf.blit(s, (centre[0]-radius, centre[1]-radius))

def draw_line_alpha(surf, colour, p1, p2, width=1):
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    pygame.draw.line(s, colour, p1, p2, width)
    surf.blit(s, (0, 0))

# static grid
grid_surf = pygame.Surface((W, H), pygame.SRCALPHA)

# background semicircle
for step in range(R, 0, -1):
    t = step / R
    shade = int(t * 4)
    pygame.draw.arc(grid_surf, (0, shade, 0, 255),
                    (CX-step, CY-step, step*2, step*2),
                    0, math.pi, 1)

# range rings and labels
for i in range(1, 5):
    r = int(R * i / 4)
    pygame.draw.arc(grid_surf, (*G_DARK, 200),
                    (CX-r, CY-r, r*2, r*2), 0, math.pi, 1)
    dist_label = font_sm.render(f"{int(MAX_DIST*i/4)}cm", True, G_MID)
    lw = dist_label.get_width()
    lh = dist_label.get_height()
    # right side on baseline
    grid_surf.blit(dist_label, (CX + r + 3, CY + 4))
    # left side on baseline
    grid_surf.blit(dist_label, (CX - r - lw - 3, CY + 4))

# angle spokes every 15 degrees
for a in range(0, 181, 15):
    ex, ey = to_xy(a, R)
    pygame.draw.line(grid_surf, (*G_DARK, 160), (CX, CY), (ex, ey), 1)
    lx, ly = to_xy(a, R + 16)
    lbl = font_sm.render(f"{a}°", True, G_MID)
    grid_surf.blit(lbl, (lx - lbl.get_width()//2, ly - 6))

# outer arc
pygame.draw.arc(grid_surf, (*G_BRIGHT, 255),
                (CX-R, CY-R, R*2, R*2), 0, math.pi, 2)
# baseline
pygame.draw.line(grid_surf, G_BRIGHT, (CX-R, CY), (CX+R, CY), 2)
# centre dot
pygame.draw.circle(grid_surf, G_BRIGHT, (CX, CY), 4)

# allocate
trail_surf = pygame.Surface((W, H), pygame.SRCALPHA)

# main loop
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # read serial
    try:
        if ser.in_waiting:
            raw = ser.readline().decode('utf-8', errors='ignore').strip()
            if ',' in raw:
                parts = raw.split(',')
                angle = 180 - float(parts[0]) # invert
                distance = min(float(parts[1]), MAX_DIST)
                trail.append((angle, distance))
                if len(trail) > MAX_TRAIL:
                    trail.pop(0)
    except Exception:
        pass

    # draw
    screen.fill(BG)
    screen.blit(grid_surf, (0, 0))

    # detection lines
    trail_surf.fill((0, 0, 0, 0))

    for i, (ta, td) in enumerate(trail):
        age   = i / max(len(trail), 1)
        alpha = int(age ** 2 * 255)

        if td < 2 or td >= MAX_DIST:
            # no detection — draw full green line to edge
            ex, ey = to_xy(ta, R)
            pygame.draw.line(trail_surf, (0, 255, 70, alpha), (CX, CY), (ex, ey), 2)
        else:
            # detection — green to object, red beyond
            dpx    = d_to_px(td)
            x, y   = to_xy(ta, dpx)
            ex, ey = to_xy(ta, R)
            pygame.draw.line(trail_surf, (0, 255, 70, alpha), (CX, CY), (x, y), 2)
            pygame.draw.line(trail_surf, (255, 50, 50, alpha), (x, y), (ex, ey), 2)
            
    screen.blit(trail_surf, (0, 0))

    # sweep line
    ex, ey = to_xy(angle, R)
    for w, a in [(18, 8), (10, 20), (5, 50), (2, 120), (1, 220)]:
        draw_line_alpha(screen, (0, 255, 70, a), (CX, CY), (ex, ey), w)

    # hud
    title = font_lg.render(TITLE, True, G_BRIGHT)
    screen.blit(title, (W//2 - title.get_width()//2, 14))

    hud = [
        (f"ANGLE  : {int(angle):>3}°",  G_BRIGHT),
        (f"DIST   : {int(distance):>3} cm", G_BRIGHT),
    ]

    for i, (txt, col) in enumerate(hud):
        screen.blit(font_md.render(txt, True, col), (12, 14 + i*18))

    pygame.display.flip()

ser.close()
pygame.quit()