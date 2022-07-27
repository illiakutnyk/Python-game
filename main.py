from tkinter import *
import random

GAME_WIDTH = 800
GAME_HEIGHT = 800
SPEED = 80
SPACE_SIZE = 40
BODY_PARTS = 3
BACKGROUND_COLOR = '#f7cb3f'


class Snake:
  def __init__(self):
    self.body_size = BODY_PARTS
    self.coordinates = []
    self.squares = []

    for i in range (0, BODY_PARTS):
      self.coordinates.append([0, 0])

    for x, y in self.coordinates:
      square = canvas.create_image(x, y, anchor="nw", image=headDownImage, tag="head")
      self.squares.append(square)

class Food:
  
  def __init__(self, snakeCoordinates):
    x, y = randomizeFoodAppearance(snakeCoordinates)

    self.coordinates = [x, y]
    canvas.create_image(x, y, anchor="nw", image=appleImage, tag="food")
    
  
def randomizeFoodAppearance(snakeIndices):
  x = random.randint(0, (GAME_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE
  y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE) - 1) * SPACE_SIZE
  for snakeX, snakeY in snakeIndices:
    if snakeX == x and snakeY == y:
      return randomizeFoodAppearance(snakeIndices)
      
  return x, y


def getHeadImage():
  global direction
  return {
    'up': headUpImage,
    'down': headDownImage,
    'right': headRightImage,
    'left': headLeftImage,
  }[direction]

def getTailImage(tailCoordinates, previousCoordinates):
  x, y = tailCoordinates
  prevX, prevY = previousCoordinates

  if x < prevX:
    return taliLeftImage
  elif x > prevX:
   return taliRightImage
  elif y < prevY:
   return taliUpImage
  elif y > prevY:
    return taliDownImage


def getBodyPartImage(previousCoordinates, tailCoordinates, nextCoordinates):
  prevX, prevY = previousCoordinates
  x, y = tailCoordinates
  nextX, nextY = nextCoordinates

  if prevX == x and x == nextX:
    return bodyVerticalImage
  elif prevY == y and y == nextY:
   return bodyHorizontalImage
  elif  (prevX == x and nextX > x and nextY ==y and prevY < y) or (prevX > x and x == nextX and y == prevY and y > nextY):
    return bodyTopRightImage
  elif (prevX > x and nextX == x and nextY > y and y == prevY) or (prevX == x and x < nextX and prevY > y and y == nextY):
    return bodyBottomRightImage
  elif  (prevX == x and x > nextX and prevY < y and y == nextY) or (prevY == y and nextY < y and nextX == x and prevX < x):
    return bodyTopLeftImage
  elif  (prevX < x and x == nextX and prevY == y and y < nextY) or (prevY > y and y == nextY and nextX < x and prevX == x):
    return bodyBottomLeftImage
  else:
    return taliDownImage


def next_turn(snake, food):
  x, y = snake.coordinates[0]

  if direction == 'up':
    y -= SPACE_SIZE
  elif direction == 'down':
    y += SPACE_SIZE
  elif direction == 'left':
    x -= SPACE_SIZE
  elif direction == 'right':
    x += SPACE_SIZE

  snake.coordinates.insert(0, (x, y))

  if x == food.coordinates[0] and y == food.coordinates[1]:
    global score
    score +=1 

    label.config(text="Score:{}".format(score))

    canvas.delete('food')

    food = Food(snake.coordinates)

  else :
    del snake.coordinates[-1]


  for i in snake.squares:
    canvas.delete(i)

  snake.squares = []

  for i in range(len(snake.coordinates)):
    x, y = snake.coordinates[i]
    if i == 0:
      headImage = getHeadImage()
      square = canvas.create_image(x, y, anchor="nw", image=headImage)
      snake.squares.append(square)
    elif i == len(snake.coordinates) - 1:
      tailCoordinates = snake.coordinates[-1]
      previousCoordinates = snake.coordinates[-2]
      tailImage = getTailImage(tailCoordinates, previousCoordinates)
      square = canvas.create_image(x, y, anchor="nw", image=tailImage)
      snake.squares.append(square)
    else:
      previousCoordinates = snake.coordinates[i-1]
      tailCoordinates = snake.coordinates[i]
      nextCoordinates = snake.coordinates[i+1]
      bodyPartImageImage = getBodyPartImage(previousCoordinates, tailCoordinates, nextCoordinates)
      square = canvas.create_image(x, y, anchor="nw", image=bodyPartImageImage)
      snake.squares.append(square)

  if check_collision(snake):
    game_over()
  else:
    window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
  global direction

  if new_direction == 'left':
    if direction != 'right':
      direction = new_direction
  if new_direction == 'right':
    if direction != 'left':
      direction = new_direction
  if new_direction == 'up':
    if direction != 'down':
      direction = new_direction
  if new_direction == 'down':
    if direction != 'up':
      direction = new_direction

def check_collision(snake):
  x, y = snake.coordinates[0]

  if x < 0 or x >= GAME_WIDTH:
    return True
  elif y < 0 or y >= GAME_HEIGHT:
    return True

  for body_part in snake.coordinates[1:]:
    if x == body_part[0] and y == body_part[1]:
      return True

  return False

def game_over():
  canvas.delete(ALL)
  canvas.create_text(
    canvas.winfo_width()/2, 
    canvas.winfo_height()/2 - 50, 
    text="GAME OVER", 
    fill="red",
    font=('Roboto', 60),
    tag="game_over")
  canvas.create_text(
    canvas.winfo_width()/2, 
    canvas.winfo_height()/2 + 50, 
    text="Press SPACE to start a new game", 
    fill="red",
    font=('Roboto', 30),
    tag="game_over")

  global isGameOver
  isGameOver = True

def initNewGame():
  canvas.delete(ALL)

  for i in range(int(GAME_HEIGHT/SPACE_SIZE)):
    y = i * SPACE_SIZE
    alternate = 0 if i == 0 or i%2 == 0 else 1
    for j in range(int(GAME_WIDTH/SPACE_SIZE)):
      color = '#f7cb3f' if j%2 == alternate else '#f2c129'
      x = j * SPACE_SIZE
      canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=color, width=0)

  global score, direction, isGameOver, label
  score = 0
  direction = 'down'
  isGameOver = False

  label.config(text="Score:{}".format(score))

  window.update()

  snake = Snake()
  food = Food(snake.coordinates)
  next_turn(snake, food)

window = Tk()
window.title("Python game")

score = 0
direction = 'down'
isGameOver = False

label = Label(window, text='', font=('Roboto', 40))
label.pack()

canvas = Canvas(window, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<space>', lambda event: initNewGame() if isGameOver else False)

# IMAGES
# apple
appleImage = PhotoImage(file='images/apple.png')
# heads
headDownImage = PhotoImage(file='images/head_down.png')
headUpImage = PhotoImage(file='images/head_up.png')
headRightImage = PhotoImage(file='images/head_right.png')
headLeftImage = PhotoImage(file='images/head_left.png')
# body parts
bodyVerticalImage = PhotoImage(file='images/body_vertical.png')
bodyHorizontalImage = PhotoImage(file='images/body_horizontal.png')
bodyTopLeftImage = PhotoImage(file='images/body_topleft.png')
bodyTopRightImage = PhotoImage(file='images/body_topright.png')
bodyBottomLeftImage = PhotoImage(file='images/body_bottomleft.png')
bodyBottomRightImage = PhotoImage(file='images/body_bottomright.png')
# tail
taliUpImage = PhotoImage(file='images/tail_up.png')
taliDownImage = PhotoImage(file='images/tail_down.png')
taliLeftImage = PhotoImage(file='images/tail_left.png')
taliRightImage = PhotoImage(file='images/tail_right.png')

initNewGame()

window.mainloop()