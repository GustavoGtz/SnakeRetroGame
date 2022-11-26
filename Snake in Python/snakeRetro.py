
"""
Retro snake game.

@author: Gustavo Gutierrez Navarro
@date: 25/11/2022
"""

import sys, pygame
import random


class Snake(object):
    """
    width Ancho de la serpiente.
    height Alto de la serpiente.
    snakeBody Arreglo que contiene las partes de la serpiente.
    """
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snakeBody = []
    
    def addBody(self, xPos, yPos, previousBodySnake):
        self.snakeBody.append(BodySnake(xPos, yPos, self.width, self.height, previousBodySnake))
        
    def snakeEat(self, foodXPos, foodYPos):
        self.snakeBody.insert(0, BodySnake(foodXPos, foodYPos, self.width, self.height, None))
        self.snakeBody[1].previousBodySnake = self.snakeBody[0]
        
    def moveSnakeUp(self):
        self.moveBody()
        self.snakeBody[0].yPos -= self.height
        
    def moveSnakeDown(self):
        self.moveBody()
        self.snakeBody[0].yPos += self.height
        
    def moveSnakeRight(self):
        self.moveBody()
        self.snakeBody[0].xPos += self.width
        
    def moveSnakeLeft(self):
        self.moveBody()
        self.snakeBody[0].xPos -= self.width
        
    def moveBody(self):
        for i in reversed(range(1, len(self.snakeBody))):
            self.snakeBody[i].xPos = self.snakeBody[i].previousBodySnake.xPos
            self.snakeBody[i].yPos = self.snakeBody[i].previousBodySnake.yPos
    
class BodySnake(object):
    """
    width Ancho del rectangulo.
    height Alto del rectangulo.
    xPos Ubicación del rectangulo en X (Esquina izquierda superior).
    yPos Ubicación del rectangulo en Y (Esquina izquierda superior).
    """
    
    def __init__(self, xPos, yPos, width, height, previousBodySnake):
        self.width = width
        self.height = height
        self.xPos = xPos
        self.yPos = yPos
        self.previousBodySnake = previousBodySnake

pygame.init()
pygame.font.init()
# Colores RGB.
SCREEN_COLOR = (143, 185, 13) # Verde antiguo.
OBJECTS_COLOR = (32, 33, 32)  # Gris casi negro.
# Tamaño de la pantalla.
WIDTH = 800
HEIGHT = 800
# Ajustes para el marco.
WIDTH_PROPORTION = 0.05
HEIGHT_PROPORTION = 0.05
SPACE_SIZE = 1            # Longitud del espaciado entre cuadraditos.
ROWS = 20
COLUMNS = 20
# Recursos gráficos.
iconImage = pygame.image.load('imgs\snakeIcon.png') # Icono de la ventana.
scoreFont = pygame.font.Font('fonts\minecraft.ttf', 25, bold = True) # Fuente del texto de puntuación.
# Recursos de audio.
eatSound = pygame.mixer.Sound('sounds\snakeEat.wav')
collisionSound = pygame.mixer.Sound('sounds\snakeCollision.wav')

# Inicialización de la ventana.
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake Retro')
pygame.display.set_icon(iconImage)
FramePerSec = pygame.time.Clock()
game = True # Variable para saber cuando se cierra el juego.
play = True # Variable para saber cuando la partida continua o si ya perdio.
# Coordenadas del marco.
frameCoordinates = (WIDTH*WIDTH_PROPORTION,       # Esquina superior en X.
                    HEIGHT*HEIGHT_PROPORTION,     # Esquina superior en Y.
                    WIDTH*(1-WIDTH_PROPORTION),   # Esquina inferior en X.
                    HEIGHT*(1-HEIGHT_PROPORTION)) # Esquina inferior en Y.
# Tamaño de los cuadrados.
squareSize = (int((frameCoordinates[2] - frameCoordinates[0]) / COLUMNS), int((frameCoordinates[3] - frameCoordinates[1]) / ROWS)) #(width, height)
# Serpiente.
snake = Snake(squareSize[0], squareSize[1]) # Arreglo donde se guardara el cuerpo del a serpiente.
snake.addBody(frameCoordinates[0] + squareSize[0]*(ROWS//2), frameCoordinates[1] + squareSize[1]*(COLUMNS//2), None) # Cabeza de la serpiente.
snake.addBody(snake.snakeBody[0].xPos - squareSize[0], snake.snakeBody[0].yPos, snake.snakeBody[0]) # Cuerpo de la serpiente.

snakeDirection = 'NONE'
snakeSpeed = 10
# Contador de puntos.
scoreLabel = scoreFont.render('SCORE:      ', True, OBJECTS_COLOR)
scoreLabelRect = scoreLabel.get_rect() # Dimensiones del texto de score.
score = 0 # Iniciamos el puntaje

# Comida.
foodXPos = 0
foodYPos = 0
foodDisplay = False # Indica si hay comida en juego.

keyCooldown = False # Cooldown para pulsar teclas.

loseLabel = scoreFont.render('GAME OVER', True, OBJECTS_COLOR) # Cartel para la derrota.
loseLabelRect = loseLabel.get_rect()
loseLabelRect.center = (WIDTH // 2, frameCoordinates[1] - loseLabelRect[3] // 2)
continueLabel = scoreFont.render('Press r to continue      Press x to exit', True, OBJECTS_COLOR)
continueLabelRect = continueLabel.get_rect()
continueLabelRect.center = (WIDTH // 2, frameCoordinates[3] + continueLabelRect[3] // 2 + 2)

while game:
    FramePerSec.tick(snakeSpeed)
    while play == False:
        # Pantalla de derrota.
        screen.blit(loseLabel, loseLabelRect)
        screen.blit(continueLabel, continueLabelRect)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                play = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    game = False
                    play = True
                if event.key == pygame.K_r:
                    # Se reinicia el juego.
                    play = True
                    score = 0
                    snakeDirection = 'NONE'
                    snake = Snake(squareSize[0], squareSize[1])
                    snake.addBody(frameCoordinates[0] + squareSize[0]*(ROWS//2), frameCoordinates[1] + squareSize[1]*(COLUMNS//2), None)
                    snake.addBody(snake.snakeBody[0].xPos - squareSize[0], snake.snakeBody[0].yPos, snake.snakeBody[0])
                    foodDisplay = False
        pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
            play = False
        # Determina dirección de la serpiente.
        if event.type == pygame.KEYDOWN:
            if keyCooldown == False:
                # En cada caso se comprueba que el movimiento no sea el opuesto al que se esta realizando.
                if event.key == pygame.K_LEFT:
                    if snakeDirection != 'RIGHT' and snakeDirection != 'NONE': # Caso 'NONE' para el inicio de partida.
                        snakeDirection = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    if snakeDirection != 'LEFT':
                        snakeDirection = 'RIGHT'
                if event.key == pygame.K_UP:
                    if snakeDirection != 'DOWN':
                        snakeDirection = 'UP'
                if event.key == pygame.K_DOWN:
                    if snakeDirection != 'UP':
                        snakeDirection = 'DOWN'
            keyCooldown = True
    # Checar el cooldown.
    if keyCooldown == True:
        keyCooldown = False
    # Configuración de la pantalla.
    screen.fill(SCREEN_COLOR)
    # Color de la pantalla.
    pygame.draw.rect(screen, OBJECTS_COLOR, pygame.Rect(frameCoordinates[0], 
                                                        frameCoordinates[1], 
                                                        frameCoordinates[2] - frameCoordinates[0], 
                                                        frameCoordinates[3] - frameCoordinates[1], 
                                                        ))
    # Cuadricula.
    for i in range(1, ROWS):
        pygame.draw.line(screen, SCREEN_COLOR, 
                         (frameCoordinates[0], frameCoordinates[1] + squareSize[1]*i),
                         (frameCoordinates[2] + squareSize[0], frameCoordinates[1] + squareSize[1]*i), 
                         SPACE_SIZE)
    
    for j in range(1, COLUMNS):
        pygame.draw.line(screen, SCREEN_COLOR, 
                         (frameCoordinates[0] + squareSize[0]*j, frameCoordinates[1]),
                         (frameCoordinates[0] + squareSize[0]*j, frameCoordinates[3] + squareSize[1]), 
                         SPACE_SIZE)
    pygame.draw.rect(screen, SCREEN_COLOR, pygame.Rect(frameCoordinates[0] + squareSize[0], 
                                                        frameCoordinates[1] + squareSize[1], 
                                                        frameCoordinates[2] - frameCoordinates[0] - squareSize[0]*2, 
                                                        frameCoordinates[3] - frameCoordinates[1] - squareSize[1]*2, 
                                                        ))
    # Movimiento de la serpiente.
    if snakeDirection == 'LEFT':
        for i in range(1, len(snake.snakeBody)):
            if snake.snakeBody[0].xPos - squareSize[0] == snake.snakeBody[i].xPos and snake.snakeBody[0].yPos == snake.snakeBody[i].yPos:
                play = False
                collisionSound.play()
                break
        else:
            if snake.snakeBody[0].xPos - squareSize[0] == frameCoordinates[0]:
                play = False
                collisionSound.play()
            else:
                snake.moveSnakeLeft()
    
    if snakeDirection == 'RIGHT':
        for i in range(1, len(snake.snakeBody)):
            if snake.snakeBody[0].xPos + squareSize[0] == snake.snakeBody[i].xPos and snake.snakeBody[0].yPos == snake.snakeBody[i].yPos:
                play = False
                collisionSound.play()
                break
        else:
            if snake.snakeBody[0].xPos + squareSize[0] == (frameCoordinates[2] - squareSize[0]):
                play = False
                collisionSound.play()
            else:
                snake.moveSnakeRight()
                
    if snakeDirection == 'UP':
        for i in range(1, len(snake.snakeBody)):
            if snake.snakeBody[0].yPos - squareSize[1] == snake.snakeBody[i].yPos and snake.snakeBody[0].xPos == snake.snakeBody[i].xPos:
                play = False
                collisionSound.play()
                break
        else:
            if snake.snakeBody[0].yPos - squareSize[1] == frameCoordinates[1]:
                play = False
                collisionSound.play()
            else:
                snake.moveSnakeUp()
    
    if snakeDirection == 'DOWN':
        for i in range(1, len(snake.snakeBody)):
            if snake.snakeBody[0].yPos + squareSize[1] == snake.snakeBody[i].yPos and snake.snakeBody[0].xPos == snake.snakeBody[i].xPos:
                play = False
                collisionSound.play()
                break
        else:
            if snake.snakeBody[0].yPos + squareSize[1] == (frameCoordinates[3] - squareSize[1]):
                play = False
                collisionSound.play()
            else:
                snake.moveSnakeDown()
    # Comprueba si la serpiente comio la comida.
    if snake.snakeBody[0].xPos == foodXPos and snake.snakeBody[0].yPos == foodYPos:
        score += 1
        snake.snakeEat(foodXPos, foodYPos)
        foodDisplay = False
        eatSound.play()
    # Dibuja a la serpiente.
    for i in range(0, len(snake.snakeBody)):
        body = snake.snakeBody[i]
        pygame.draw.rect(screen, OBJECTS_COLOR, pygame.Rect(body.xPos, body.yPos, body.width, body.height))   # Cuerpo de la serpiente negro.
        pygame.draw.rect(screen, SCREEN_COLOR, pygame.Rect(body.xPos, body.yPos, body.width, body.height), 2) # Borde de la serpiente verde.  
    # Spawnea la comida
    while foodDisplay == False:
        foodXPos = frameCoordinates[0] + squareSize[0]*random.randint(1, COLUMNS - 2)
        foodYPos = frameCoordinates[1] + squareSize[1]*random.randint(1, ROWS - 2)
        for i in range(0, len(snake.snakeBody)):
            body = snake.snakeBody[i]
            if body.xPos == foodXPos and body.yPos == foodYPos:
                print("No se puede spawnear")
                break
        else:
            foodDisplay = True
    # Dibuja la comida.
    pygame.draw.ellipse(screen, OBJECTS_COLOR, pygame.Rect(foodXPos, foodYPos, squareSize[0], squareSize[1]))
    pygame.draw.ellipse(screen, SCREEN_COLOR, pygame.Rect(foodXPos, foodYPos, squareSize[0], squareSize[1]), 3)
    # Contador de puntos.
    screen.blit(scoreLabel, (frameCoordinates[0], frameCoordinates[1] - scoreLabelRect[3])) # Cartel.
    screen.blit(scoreFont.render(str(score), True, OBJECTS_COLOR), (scoreLabelRect[0] + scoreLabelRect[2], frameCoordinates[1] - scoreLabelRect[3])) # Puntaje.
    
    pygame.display.flip()
pygame.quit()
sys.exit()
