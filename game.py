import pygame
import space_ship
import enemy_space_ship
import sprites
import random

# initialize pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# create a game displayadd
pygame.display.set_icon(sprites.icon)
display_width = 800
display_height = 600
game_display = pygame.display.set_mode((display_width, display_height))

# 8 bit font
font = "8-Bit-Madness.ttf"


# text rendering function
def message_to_screen(message, textfont, size, color):
    my_font = pygame.font.Font(textfont, size)
    my_message = my_font.render(message, 0, color)

    return my_message


# colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# sprite pixel format converting
for convert_sprites in sprites.all_sprites:
    convert_sprites.convert_alpha()

# framerate
clock = pygame.time.Clock()
FPS = 30

# player variables
player = space_ship.SpaceShip(100, display_height / 2 - 40)
moving = True
godmode = False

# score variables
score = 0
highscore_file = open('highscore.dat', "r")
highscore_int = int(highscore_file.read())

# enemy space ship variables
enemy_space_ship = enemy_space_ship.EnemySpaceShip(-100, display_height / 2 - 40)
enemy_space_ship_alive = False

#  missile variables
missile_x = 800
missile_y = random.randint(0, 400)
missile_alive = False
missile_hit_player = False
warning_once = True
warning = False
warning_counter = 0
warning_message = message_to_screen("!", font, 200, red)

# asteroid variables
asteroid_x = 800
asteroid_y = random.randint(0, 400)

# bullet variables
bullets = []


# sounds
shoot = pygame.mixer.Sound('sounds/shoot.wav')
pop = pygame.mixer.Sound('sounds/pop.wav')
explosion = pygame.mixer.Sound('sounds/explosion.wav')
explosion2 = pygame.mixer.Sound('sounds/explosion2.wav')
select = pygame.mixer.Sound('sounds/select.wav')
select2 = pygame.mixer.Sound('sounds/select2.wav')
alert = pygame.mixer.Sound('sounds/alert.wav')
whoosh = pygame.mixer.Sound('sounds/whoosh.wav')


# main menu
def main_menu():

    menu = True

    selected = "play"

    while menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(select)
                    selected = "play"
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    pygame.mixer.Sound.play(select)
                    selected = "quit"
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(select2)
                    if selected == "play":
                        menu = False
                    if selected == "quit":
                        pygame.quit()
                        quit()

        # drawing background
        game_display.blit(sprites.background, (0, 0))

        if godmode:
            title = message_to_screen("SPACE SHIP (GODMODE)", font, 80, yellow)
        else:
            title = message_to_screen("SPACE SHIP", font, 100, white)
        controls_1 = message_to_screen("use WASD to move, SPACE to shoot,", font, 30, white)
        controls_2 = message_to_screen("P to toggle pause", font, 30, white)
        if selected == "play":
            play = message_to_screen("PLAY", font, 75, red)
        else:
            play = message_to_screen("PLAY", font, 75, white)
        if selected == "quit":
            game_quit = message_to_screen("QUIT", font, 75, red)
        else:
            game_quit = message_to_screen("QUIT", font, 75, white)

        title_rect = title.get_rect()
        controls_1_rect = controls_1.get_rect()
        controls_2_rect = controls_2.get_rect()
        play_rect = play.get_rect()
        quit_rect = game_quit.get_rect()

        # drawing text
        game_display.blit(title, (display_width/2 - (title_rect[2]/2), 40))
        game_display.blit(controls_1, (display_width/2 - (controls_1_rect[2]/2), 120))
        game_display.blit(controls_2, (display_width/2 - (controls_2_rect[2]/2), 140))
        game_display.blit(play, (display_width/2 - (play_rect[2]/2), 200))
        game_display.blit(game_quit, (display_width/2 - (quit_rect[2]/2), 260))
        # drawing planet
        pygame.draw.rect(game_display, gray, (0, 500, 800, 100))

        pygame.display.update()
        pygame.display.set_caption("SPACE SHIP running at " + str(int(clock.get_fps())) + " frames per second.")
        clock.tick(FPS)


def pause():

    global highscore_file
    global highscore_int

    paused = True

    player.moving_up = False
    player.moving_left = False
    player.moving_down = False
    player.moving_right = False

    paused_text = message_to_screen("PAUSED", font, 100, white)
    paused_text_rect = paused_text.get_rect()

    game_display.blit(paused_text, (display_width/2 - (paused_text_rect[2]/2), 40))

    pygame.display.update()
    clock.tick(15)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > highscore_int:
                    highscore_file = open('highscore.dat', "w")
                    highscore_file.write(str(score))
                    highscore_file.close()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mixer.Sound.play(select)
                    paused = False


# create a game loop
def game_loop():

    global missile_x
    global missile_y
    global missile_alive
    global missile_hit_player
    global warning
    global warning_counter
    global warning_once

    global bullets
    global moving

    global highscore_file
    global highscore_int
    global score

    global asteroid_x
    global asteroid_y

    global enemy_space_ship_alive

    game_exit = False
    game_over = False

    game_over_selected = "play again"

    while not game_exit:

        while game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if score > highscore_int:
                        highscore_file = open('highscore.dat', "w")
                        highscore_file.write(str(score))
                        highscore_file.close()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        pygame.mixer.Sound.play(select)
                        game_over_selected = "play again"
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        pygame.mixer.Sound.play(select)
                        game_over_selected = "quit"
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        pygame.mixer.Sound.play(select2)
                        if game_over_selected == "play again":
                            if score > highscore_int:
                                highscore_file = open('highscore.dat', "w")
                                highscore_file.write(str(score))
                                highscore_file.close()
                            game_over = False

                            score = 0

                            asteroid_x = 800

                            enemy_space_ship.x = -100
                            enemy_space_ship_alive = False
                            enemy_space_ship.bullets = []

                            missile_x = 800
                            missile_alive = False
                            warning = False
                            warning_counter = 0
                            warning_counter = 0

                            player.wreck_start = False
                            player.y = display_height/2-40
                            player.x = 100
                            player.wrecked = False
                            player.health = 3
                            bullets = []

                            game_loop()
                        if game_over_selected == "quit":
                            pygame.quit()
                            quit()

            game_over_text = message_to_screen("GAME OVER", font, 100, white)
            your_score = message_to_screen("YOUR SCORE WAS: " + str(score), font, 50, black)
            if game_over_selected == "play again":
                play_again = message_to_screen("PLAY AGAIN", font, 75, white)
            else:
                play_again = message_to_screen("PLAY AGAIN", font, 75, white)
            if game_over_selected == "quit":
                game_quit = message_to_screen("QUIT", font, 75, white)
            else:
                game_quit = message_to_screen("QUIT", font, 75, white)

            game_over_rect = game_over_text.get_rect()
            your_score_rect = your_score.get_rect()
            play_again_rect = play_again.get_rect()
            game_quit_rect = game_quit.get_rect()

            game_display.blit(game_over_text, (display_width/2 - game_over_rect[2]/2, 40))
            game_display.blit(your_score, (display_width/2 - (your_score_rect[2]/2+5), 100))
            game_display.blit(play_again, (display_width/2 - play_again_rect[2]/2, 200))
            game_display.blit(game_quit, (display_width/2 - game_quit_rect[2]/2, 260))

            pygame.display.update()
            pygame.display.set_caption("SPACE SHIP running at " + str(int(clock.get_fps())) + " frames per second.")
            clock.tick(10)

        # event handler
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                if score > highscore_int:
                    highscore_file = open('highscore.dat', "w")
                    highscore_file.write(str(score))
                    highscore_file.close()
                pygame.quit()
                quit()

            if moving:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        player.moving_up = True
                    if event.key == pygame.K_a:
                        player.moving_left = True
                    if event.key == pygame.K_s:
                        player.moving_down = True
                    if event.key == pygame.K_d:
                        player.moving_right = True
                    if event.key == pygame.K_SPACE:
                        if not player.wreck_start:
                            pygame.mixer.Sound.play(shoot)
                            bullets.append([player.x, player.y])

                    if event.key == pygame.K_p:
                        pygame.mixer.Sound.play(select)
                        pause()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        player.moving_up = False
                    if event.key == pygame.K_a:
                        player.moving_left = False
                    if event.key == pygame.K_s:
                        player.moving_down = False
                    if event.key == pygame.K_d:
                        player.moving_right = False

        if player.health < 1:
            pygame.mixer.Sound.play(explosion)
            player.wreck()

        if player.wrecked:
            game_over = True


        game_display.blit(sprites.background, (0, 0))


        # drawing player
        game_display.blit(player.current, (player.x, player.y))

        # drawing enemy space ship
        game_display.blit(enemy_space_ship.current, (enemy_space_ship.x, enemy_space_ship.y))

        # drawing missile
        game_display.blit(sprites.missile, (missile_x, missile_y))

        # enabling movement and animations
        player.player_init()
        enemy_space_ship.init()

        # rendering bullets
        if not player.wreck_start and not player.wrecked:
            for draw_bullet in bullets:
                pygame.draw.rect(game_display, yellow, (draw_bullet[0]+90, draw_bullet[1]+40, 10, 10))
            for move_bullet in range(len(bullets)):
                bullets[move_bullet][0] += 40
            for del_bullet in bullets:
                if del_bullet[0] >= 800:
                    bullets.remove(del_bullet)

        # rendering enemy bullets
        if not player.wreck_start and not player.wrecked and not game_over:
            for draw_bullet in enemy_space_ship.bullets:
                pygame.draw.rect(game_display, gray, (draw_bullet[0], draw_bullet[1]+40, 40, 10))
                pygame.draw.rect(game_display, red, (draw_bullet[0]+30, draw_bullet[1]+40, 10, 10))
            for move_bullet in range(len(enemy_space_ship.bullets)):
                enemy_space_ship.bullets[move_bullet][0] -= 15
            for del_bullet in enemy_space_ship.bullets:
                if del_bullet[0] <= -40:
                    enemy_space_ship.bullets.remove(del_bullet)

        # draw randomly positioned asteroids, pop if they hit any bullet
        for pop_asteroid in bullets:
            if asteroid_x < pop_asteroid[0]+90 < asteroid_x+70 and asteroid_y < pop_asteroid[1]+40 < asteroid_y+100:
                pygame.mixer.Sound.play(pop)
                bullets.remove(pop_asteroid)
                asteroid_x = 800 - 1500
                score += 50
            elif asteroid_x < pop_asteroid[0]+100 < asteroid_x+70 and asteroid_y < pop_asteroid[1]+50 < asteroid_y+100:
                pygame.mixer.Sound.play(pop)
                bullets.remove(pop_asteroid)
                asteroid_x = 800 - 1500
                score += 50

        # spawn missile randomly
        missile_spawn_num = random.randint(0, 100)
        if missile_spawn_num == 50 and not missile_alive and score > 450:
            warning = True

        # show warning before  missile spawning
        if warning:
            if warning_once:
                pygame.mixer.Sound.play(alert)
                warning_once = False
            game_display.blit(warning_message, (750, missile_y-15))
            if warning_counter > 45:
                pygame.mixer.Sound.play(whoosh)
                missile_alive = True
                warning_counter = 0
                warning = False
                warning_once = True
            else:
                warning_counter += 1

        # missile movement
        if missile_alive:
            missile_x -= 30
        if missile_x < 0-100:
            missile_hit_player = False
            missile_alive = False
            missile_x = 800
            missile_y = random.randint(0, 400)

        # spawn enemy space ship randomly
        enemy_spawn_num = random.randint(0, 100)
        if not enemy_space_ship_alive and score > 250 and enemy_spawn_num == 50:
            enemy_space_ship_alive = True
            enemy_space_ship.x = 800

        # enemy-player bullet collision detection
        for hit_enemy_space_ship in bullets:
            if enemy_space_ship.x < hit_enemy_space_ship[0]+90 < enemy_space_ship.x+100 \
               or enemy_space_ship.x < hit_enemy_space_ship[0]+100 < enemy_space_ship.x+100:
                if enemy_space_ship.y < hit_enemy_space_ship[1]+40 < enemy_space_ship.y+80 \
                   or enemy_space_ship.y < hit_enemy_space_ship[1]+50 < enemy_space_ship.y+80:
                    if not enemy_space_ship.x > 600:
                        pygame.mixer.Sound.play(explosion2)
                        score += 150
                        bullets.remove(hit_enemy_space_ship)
                        enemy_space_ship.x = -100
                        enemy_space_ship_alive = False

        # missile-player bullet
        for hit_missile in bullets:
            if missile_x < hit_missile[0]+90 < missile_x+100 \
               or missile_x < hit_missile[0]+100 < missile_x+100:
                if missile_y < hit_missile[1]+40 < missile_y+80 \
                   or missile_y < hit_missile[1]+50 < missile_y+80:
                    if not missile_x > 700:
                        pygame.mixer.Sound.play(explosion2)
                        bullets.remove(hit_missile)
                        score += 200
                        missile_hit_player = False
                        missile_alive = False
                        missile_x = 800
                        missile_y = random.randint(0, 400)

        # player-asteroid collision detection
        if asteroid_x < player.x < asteroid_x+70 or asteroid_x < player.x+100 < asteroid_x+70:
            if asteroid_y < player.y < asteroid_y+80 or asteroid_y < player.y+80 < asteroid_y+80:
                pygame.mixer.Sound.play(explosion)
                # player.damaged = True
                player.health -= 1
                asteroid_x = 800-1500

        # player-enemy rocket collision detection
        for hit_player in enemy_space_ship.bullets:
            if player.x < hit_player[0] < player.x+100 or player.x < hit_player[0]+40 < player.x+100:
                if player.y < hit_player[1]+40 < player.y+80 or player.y < hit_player[1]+50 < player.y+80:
                    pygame.mixer.Sound.play(explosion)
                   # player.damaged = True
                    player.health -= 1
                    enemy_space_ship.bullets.remove(hit_player)

        # player-misle collision detection
        if missile_x < player.x < missile_x+100 or missile_x < player.x+100 < missile_x+100:
            if missile_y < player.y < missile_y+88 or missile_y < player.y+80 < missile_y+88:
                if not missile_hit_player:
                    pygame.mixer.Sound.play(explosion)
                   # player.damaged = True
                    player.health -= 1
                    missile_hit_player = True

        game_display.blit(sprites.asteroid, (asteroid_x, asteroid_y))
        if asteroid_x <= 800 - 870:
            asteroid_x = 800
            asteroid_y = random.randint(0, 400)
        else:
            if not player.wreck_start:
                asteroid_x -= 7

        # draw score
        game_display.blit(message_to_screen("SCORE: {0}".format(score), font, 50, white), (10, 10))

        # draw high score
        if score < highscore_int:
            hi_score_message = message_to_screen("HI-SCORE: {0}".format(highscore_int), font, 50, white)
        else:
            highscore_file = open('highscore.dat', "w")
            highscore_file.write(str(score))
            highscore_file.close()
            highscore_file = open('highscore.dat', "r")
            highscore_int = int(highscore_file.read())
            highscore_file.close()
            hi_score_message = message_to_screen("HI-SCORE: {0}".format(highscore_int), font, 50, white)

        hi_score_message_rect = hi_score_message.get_rect()

        game_display.blit(hi_score_message, (800-hi_score_message_rect[2]-10, 10))

        # draw health
        if player.health >= 1:
            game_display.blit(sprites.icon, (10, 50))
            if player.health >= 2:
                game_display.blit(sprites.icon, (10+32+10, 50))
                if player.health >= 3:
                    game_display.blit(sprites.icon, (10+32+10+32+10, 50))

        # god-mode (for quicker testing)
        if godmode:
            score = 1000
            player.health = 3

        # drawing planet
        pygame.draw.rect(game_display, gray, (0, 500, 800, 100))

        pygame.display.update()

        pygame.display.set_caption("SPACE SHIP running at " + str(int(clock.get_fps())) + " frames per second.")
        clock.tick(FPS)


main_menu()
game_loop()
pygame.quit()
quit()

