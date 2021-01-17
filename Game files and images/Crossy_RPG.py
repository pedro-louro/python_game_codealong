import pygame
import time

#Size of the Screen
screen_title = "Crossy RPG"
screen_width = 800
screen_height = 800

#Colors according to RGB codes
white_color = (255,255,255)
black_color = (0,0,0)

#Clock used to update game events and frames
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)
class Game:
    tick_rate = 60

    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        #Create the window of specified size in white to display the game 
        self.game_screen = pygame.display.set_mode((width, height))
        #Set the game window color to white
        self.game_screen.fill(white_color)
        pygame.display.set_caption(title)

        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))
 
    def run_game_loop(self, level, level_speed):
        is_game_over = False
        did_win = False
        direction = 0

        player_character = PlayerCharecter('player.png', 375, 700, 50, 50)
        enemy_0 = NonPlayerCharecter('enemy.png', 20, 600,50, 50)
        enemy_0.SPEED *= level_speed

        enemy_1 = NonPlayerCharecter('enemy.png', self.width - 40, 400,50, 50)
        enemy_1.SPEED *= level_speed

        enemy_2 = NonPlayerCharecter('enemy.png', 20, 200,50, 50)
        enemy_2.SPEED *= level_speed

        treasure = GameObject('treasure.png', 375, 50, 50, 50)
        #Main game loop used to update all gameplay such us movements, checks
        
        while not is_game_over:

            for event in pygame.event.get():
                #If we have a quit type event (exit down) then exist the game
                if event.type == pygame.QUIT:
                    is_game_over = True
                #Detect when key is pressed down
                elif event.type == pygame.KEYDOWN:
                    #Move up if key pressed
                    if event.key == pygame.K_UP:
                        direction = 1
                    #Move down if key pressed
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                #Detect hen Key is released
                elif event.type == pygame.KEYUP:
                    #Stop the movement when key no longer pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
                print(event)
            
            # Redraw the screen to be a black white window
            self.game_screen.fill(white_color)
            self.game_screen.blit(self.image, (0, 0))

            #Show treasure
            treasure.draw(self.game_screen)
            # Update the Player position
            player_character.move(direction, self.height)
            # Draw the player at the new position
            player_character.draw(self.game_screen)

            # Move and draw the enemy character
            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            if level > 3:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)

            if level > 6:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)

            if player_character.detect_collision(enemy_0):
                is_game_over = True
                did_win = False
                text = font.render('You Lose!', True, black_color)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break
            elif player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                level += 1
                text = font.render('You Win!', True, black_color)
                self.game_screen.blit(text, (300, 350))
                clock.tick(0.5)

                break

            #Update all game graphics
            pygame.display.update()
            #Tick the clock to update everything within the game
            clock.tick(self.tick_rate)
        
        if did_win:
            text2 = font.render('Level {0}'.format(level), True, black_color)
            self.game_screen.blit(text2, (300, 450))
            pygame.display.update()
            clock.tick(0.5)
            self.run_game_loop(level, level_speed + 0.5)
        else:
            return

class GameObject:

    def __init__(self, image_path, x, y, width, height):
        
        #Load the player image from the file directiry
        object_image = pygame.image.load(image_path)
        #Scale the image up
        self.image = pygame.transform.scale(object_image, (width,height))

        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

class PlayerCharecter (GameObject):

    SPEED = 7

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED

        if self.y_pos >= max_height -40:
            self.y_pos = max_height -40

    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False

        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False

        return True

class NonPlayerCharecter (GameObject):

    SPEED = 3

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 40:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED
       
pygame.init()

new_game = Game('background.png', screen_title, screen_width, screen_height)
new_game.run_game_loop(1, 1)



pygame.quit()
quit()

#Load the player image from the file directiry
#player_image = pygame.image.load("player.png")
#Scale the image up
#player_image = pygame.transform.scale(player_image, (50,50))

#draw rectangel on top of the game screen canvas (x, y, width, height)
#pygame.draw.rect(game_screen, black_color,[350, 350, 100, 100])
#draw circle on top of the game screen (x, y,radius)
#pygame.draw.circle(game_screen, black_color, (400, 300), 50)

#game_screen.blit(player_image, (375,375))
