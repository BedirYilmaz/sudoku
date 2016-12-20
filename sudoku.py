import itertools, pygame, sys, time, random, codecs, snumber
from pygame.locals import *

sudokus = open("123456789.txt").read().splitlines()
sudoku1 = sudokus[random.randrange(0,10000)]
sudokuanswer = sudoku1

size = 9
difficulty = 10
tbsize = 50
red = pygame.Color("red")
green = pygame.Color("green")
blue = pygame.Color("blue")
black = pygame.Color("black")
white = pygame.Color("white")
gray = pygame.Color("gray")

table = [] # table of sudoku values
stable = [] # table of sudoku number objects
htable = [] # table of hidden values
clicked = False

# initialize rythm clock
clock = pygame.time.Clock()

# initialize screen variables
screenx = size*tbsize
screeny = size*tbsize
black = (0,0,0)
screenRect = Rect(0,0,size*tbsize,size*tbsize)
screen = pygame.display.set_mode((screenx, screeny))

# initialize font
pygame.font.init()
font_path = ".\Lato-Black.ttf"
font_size = 12
fontObj = pygame.font.Font(font_path, font_size)

# check whether there is any element appearing more than once in vertical sequences.
def isVerticallyTrue(sudoku):
    for i in range(0,size):
        col = sudoku[i::size]
        if len(col) != len(set(col)):
            return False
    return True

# check whether there is any element appearing more than once in horizontal sequences.
def isHorizontallyTrue(sudoku):
    for i in range(0,size):
        row = sudoku[size*i:size*(i+1)]
        if len(row) != len(set(row)):
            return False
    return True

# check whether there is any element appearing more than once in inner square areal sequences.
def isAreallyTrue(sudoku):
    areaSize = int(size**(0.5))
    areaBlockSize = size*areaSize
    areas = []
    for k in range(0, areaSize):
        for j in range(0, areaSize):
            area = []
            for i in range(0,areaSize):
                area.append(sudoku[(k*areaBlockSize+j*areaSize+size*i):(k*areaBlockSize+j*areaSize+areaSize+size*i):])
            area = list(itertools.chain.from_iterable(area))
            if len(area) != len(set(area)):
                return False
    return True

def generateHiddenCells():
    for i in range(0, difficulty):
        randHidden = random.randrange(0,80)
        while(randHidden in htable):
            randHidden = random.randrange(0,80)
        htable.append(randHidden)

def isTrue(s):
    print(isVerticallyTrue(s), end = ' ')
    print(isHorizontallyTrue(s), end = ' ')
    print(s==sudoku1, end = ' ')
    print(isAreallyTrue(s))
    return isVerticallyTrue(s) and isHorizontallyTrue(s) and isAreallyTrue(s) and ("0" not in s)

def test():
    for s in sudokus:
        print(isVerticallyTrue(s), end = ' ')
        print(isHorizontallyTrue(s), end = ' ')
        print(isAreallyTrue(s))

    print(isVerticallyTrue(sudoku1))
    print(isHorizontallyTrue(sudoku1))
    print(isAreallyTrue(sudoku1))

def inittable(sudoku):
    for i in range(0, size):
        for j in range(0, size):
            if (j + size*i) not in htable:
                s = snumber.Snumber(j, i, sudoku[i*size+j], Rect(j*tbsize, i*tbsize, tbsize, tbsize))
            else :
                s = snumber.Snumber(j, i, 0, Rect(j*tbsize, i*tbsize, tbsize, tbsize))
                l = list(sudoku)
                l[s.getX()+ s.getY()*size] = "0"
                sudoku = ''.join(l)
            stable.append(s)
    return sudoku

def renderTable():
    pygame.draw.rect(screen, white, (0, 0, tbsize*size, tbsize*size))
    areaSize = int(size**(0.5))
    count = 0
    for s in stable:
        c = black
        if s.getStatus():
            c = red
        pygame.draw.rect(screen, c, (s.getX()*tbsize, s.getY()*tbsize, tbsize, tbsize),1)

        if not (s.getValue() == 0):
            if (s.getX() + size*s.getY()) in htable:
                screen.blit(fontObj.render(s.getValue(), 1, red), (s.getX()*tbsize+tbsize*(2/5), s.getY()*tbsize+tbsize*(2/5)))
            else:
                screen.blit(fontObj.render(s.getValue(), 1, black), (s.getX()*tbsize+tbsize*(2/5), s.getY()*tbsize+tbsize*(2/5)))

        count += 1
    for i in range(0,areaSize):
        for j in range(0,areaSize):
            pygame.draw.rect(screen, black, (j*tbsize*areaSize, i*tbsize*areaSize, tbsize*areaSize, tbsize*areaSize),3)

isTrue(sudoku1)
generateHiddenCells()
sudokuanswer = inittable(sudoku1)
while 1:
    clock.tick(30)
    pygame.display.flip()
    renderTable()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit(); sys.exit();
        if clicked:
            if event.type == pygame.KEYDOWN:
                key = event.key
                key = str(pygame.key.name(key))

                if (not key.isdigit()) or key == "0":
                    break

                clicknumber.toggleStatus()
                clicknumber.setValue(key)
                renderTable()

                l = list(sudokuanswer)
                l[c.getX()+ c.getY()*size] = key
                sudokuanswer = ''.join(l)
                print(sudokuanswer)

                if isTrue(sudokuanswer):
                    print("AAAAAAAAAAAAAAAAAAAAA!")
                    pygame.quit(); sys.exit();

                clicked = False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked_rects = [r for r in stable if r.getRect().collidepoint(pos)]
                for c in clicked_rects:
                    c.toggleStatus()
                    clicked = True
                    clicknumber = c

    pygame.display.flip()
