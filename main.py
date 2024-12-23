import pygame
import numpy

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


def init_screen(player1, player2, screen_width, screen_height):
    """
    The code that is contained in the init_screen function sets the visuals for the window.
    The window name will be saying the names of the two users who are playing against each other.
    The window will be set to a certain size depending on the users inputs for the screen width
    and height and the color of the screen will be set to white. Vertical and horizontal lines
    will be drawn to set the lines for the board.
    """
    pygame.display.set_caption(f"{player1} vs {player2} : Tic Tac Toe")
    screen = pygame.display.set_mode([screen_width, screen_height])
    screen.fill(WHITE)

    # vertical lines
    posX = screen_width / 3
    pygame.draw.line(screen, BLACK, (posX, 0), (posX, screen_height))
    posX = screen_width * 2 / 3
    pygame.draw.line(screen, BLACK, (posX, 0), (posX, screen_height))

    # horizontal lines
    posY = screen_height / 3
    pygame.draw.line(screen, BLACK, (0, posY), (screen_width, posY))
    posY = screen_height * 2 / 3
    pygame.draw.line(screen, BLACK, (0, posY), (screen_width, posY))

    pygame.display.flip()

    return screen


def load_images(screen_width, screen_height):
    """
    This function will load the 'X' and 'O' images that will be used for the Tic-Tac-Toe game.
    The images will be resized in a certain way depending on the screen width and height
    that the user enters. The width and height of the images would need to be divided by 3
    because there are 3 rows and columns. It is multiplied by 0.8 because the image needs
    to be 80% of each spot.
    """
    xImage = pygame.image.load("xImage.png")
    oImage = pygame.image.load("oImage.png")
    image_width = int(screen_width / 3 * 0.8)
    image_height = int(screen_height / 3 * 0.8)
    image_dimensions = (image_width, image_height)
    xImage = pygame.transform.scale(xImage, image_dimensions)
    oImage = pygame.transform.scale(oImage, image_dimensions)
    return xImage, oImage


def mouseClick(board, screen_width, screen_height, image, player):
    """
    This function finds out the (x,y) coordinates of the mouse location and depending on
    the coordinates, it computes the row and column in the board. It then fills the board
    spot with either a 'X' or 'O' image.
    """
    x, y = pygame.mouse.get_pos()
    row = int(3 * y / screen_height)
    col = int(3 * x / screen_width)

    if board[row][col] is not None:
        return False

    board[row][col] = player
    # We add (screen_width / 30) to ensure that the x-coordinate is shifted
    # 10% to the right in the spot
    posX = (screen_width * col / 3) + (screen_width / 30)
    # We add (screen_height / 30) to ensure that the y-coordinate is shifted
    # 10% below in the spot
    posY = (screen_height * row / 3) + (screen_height / 30)
    screen.blit(image, (posX, posY))
    pygame.display.flip()
    return True


def all_spots_filled(board):
    """
    This function checks if all of the spots in the board are filled.
    """
    return numpy.all(board != None)


def player_won(board, screen_width, screen_height, player):
    """ 
    This function decides whether the current player is the winner. It checks each row, each column
    and the 2 diagonals to see whether the current player has 3 in row. If the current is the winner,
    it draws a horizontal or vertical or diagonal line.
    """
    # Check all rows
    res = numpy.all(board == player, axis=1)
    for row in range(0, len(res)):
        if res[row]:
            # We add (screen_height / 6) to ensure line is in the middle of the row
            posY = (screen_height * row / 3) + (screen_height / 6)
            pygame.draw.line(screen, RED, (0, posY), (screen_width, posY))
            return True

    # Check all columns
    res = numpy.all(board == player, axis=0)
    for col in range(0, len(res)):
        if res[col]:
            # We add (screen_width / 6) to ensure line is in the middle of the column
            posX = (screen_width * col / 3) + (screen_width / 6)
            pygame.draw.line(screen, RED, (posX, 0), (posX, screen_height))
            return True

    # Check diagonal left to right
    if numpy.all(numpy.diagonal(board) == player):
        pygame.draw.line(screen, RED, (0, 0), (screen_width, screen_height))
        return True

    # Check diagonal right to left
    if numpy.all(numpy.diagonal(numpy.fliplr(board)) == player):
        pygame.draw.line(screen, RED, (screen_width, 0), (0, screen_height))
        return True

    return False


def game_over(board, screen_width, screen_height, player):
    """ 
    This function checks and displays who the winner is or if the game has ended in a draw. 
    """
    if player_won(board, screen_width, screen_height, player):
        print("{} won".format(player1 if player == "X" else player2))
        pygame.display.flip()
        return True
    if all_spots_filled(board):
        print("Game Draw")
        return True
    return False


def start_game():
    """ 
    This function contains the main loop which starts the game. 
    This makes sure that the program keeps running and that the window will not close on itself.
    It also shows what happens each time the mouse is released (after clicking).
    """
    board = numpy.array([[None] * 3, [None] * 3, [None] * 3])
    running = True
    ignore_mouse_click = False
    player = "X"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if ignore_mouse_click:
                    continue
                image = xImage if player == "X" else oImage
                if mouseClick(board, screen_width, screen_height, image,
                              player):
                    if game_over(board, screen_width, screen_height, player):
                        ignore_mouse_click = True
                    else:
                        player = "O" if player == "X" else "X"


# Get user inputs. Inputs are the 2 player names and desired screen dimensions.
player1 = input(f"Enter Player 1 Name: ").capitalize()
player2 = input(f"Enter Player 2 Name: ").capitalize()
screen_width = int(
    input(f"Enter the desired width for the screen (in pixels): "))
screen_height = int(
    input(f"Enter the desired height for the screen (in pixels): "))

pygame.init()
screen = init_screen(player1, player2, screen_width, screen_height)
xImage, oImage = load_images(screen_width, screen_height)
start_game()
pygame.quit()