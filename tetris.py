import pygame
import keyboard
import threading
import time
import random
import math

def check_score():
    global doneblock
    global done
    global score
    for i in range(20): # height
        check = []
        check2 = []
        for j in range(20): #width
            if [j, i] in doneblock:
                check.append(True)
                check2.append([j, i])
            else:
                check.append(False)
        if all(check) == True:
            score += 1000
            for o in check2:
                doneblock.remove(o)
                done.remove([j for j in done if j[0]==o[0] and j[1] == o[1]][0])
            doneblock = [[j[0], j[1]+1] if j[1] < i else j for j in doneblock]
            done = [[j[0], j[1]+1, j[2]] if j[1] < i else j for j in done]

def get_random_style():
    blockstyle = random.choice(style)
    block = [i for i in sum([[[j, i] if blockstyle[0][i][j] == 1 else None for j in range(len(blockstyle[0][i]))] for i in range(len(blockstyle[0]))], []) if i] + [blockstyle[1]]
    return blockstyle, block

def update():
    
    screen.fill((0, 0, 0))
    text = font.render(str(score), True, (255, 255, 255))
    text_rect = text.get_rect(center=(200, 30))
    screen.blit(text, text_rect)

    #for i in range(21):
        #pygame.draw.line(screen, (255, 255, 255), (i*20-1, 0), (i*20-1, 400), 1)
        #pygame.draw.line(screen, (255, 255, 255), (0, i*20-1), (400, i*20-1), 1)

    for i in block[:-1]:
        pygame.draw.rect(screen, block[-1], (i[0]*20, i[1]*20, 19, 19))
    for i in done:
        pygame.draw.rect(screen, i[2], (i[0] * 20, i[1] * 20, 19, 19))

def block_movement(count):
    global block
    global done
    global doneblock
    global blockstyle
    global style
    global run
    global score
    
    if len(count) == 20:
        if all([True if i[1] > 2 else False for i in sorted(doneblock, key = lambda x: x[1], reverse = True)]):
            for i in block[:-1]:
                if [i[0], i[1]+1] in doneblock:
                    newdone = []
                    newdoneblock = []
                    [done.append(i+[block[-1]]) for i in block[:-1]]
                    [doneblock.append(i) for i in block[:-1]]
                    [newdone.append(i) for i in done if i not in newdone]
                    [newdoneblock.append(i) for i in doneblock if i not in newdoneblock]
                    done = newdone
                    doneblock = newdoneblock
                    blockstyle, block = get_random_style()
                    break

            if max([i[1] for i in block[:-1]]) * 10 < 190 and block:
                for i in block[:-1]:
                    block[block.index(i)] = [block[block.index(i)][0], block[block.index(i)][1]+1]
            else:
                newdone = []
                newdoneblock = []
                [done.append(i+[block[-1]]) for i in block[:-1]]
                [doneblock.append(i) for i in block[:-1]]
                [newdone.append(i) for i in done if i not in newdone]
                [newdoneblock.append(i) for i in doneblock if i not in newdoneblock]
                done = newdone
                doneblock = newdoneblock
                blockstyle, block = get_random_style()
        else:
            score = 'You Lose'

def detect_move():
    global block
    global done
    global doneblock
    global blockstyle
    global style
    global stop
    while True:
        if keyboard.is_pressed('a'):
            if all([True if [i[0]-1, i[1]] not in doneblock and i[0]-1 >= 0 else False for i in block[:-1]]):
                block = [[i[0]-1, i[1]] for i in block[:-1]] + [block[-1]]
        if keyboard.is_pressed('d'):
            if all([True if [i[0]+1, i[1]] not in doneblock and i[0]+1 < 20 else False for i in block[:-1]]):
                block = [[i[0]+1, i[1]] for i in block[:-1]] + [block[-1]]
        if keyboard.is_pressed('s'):
            for i in block[:-1]:
                if [i[0], i[1] + 1] in doneblock:
                    newdone = []
                    newdoneblock = []
                    [done.append(i + [block[-1]]) for i in block[:-1]]
                    [doneblock.append(i) for i in block[:-1]]
                    [newdone.append(i) for i in done if i not in newdone]
                    [newdoneblock.append(i) for i in doneblock if i not in newdoneblock]
                    done = newdone
                    doneblock = newdoneblock
                    blockstyle, block = get_random_style()
                    break
                
            if all([True if i[1]+1 < 20 else False for i in block[:-1]]):
                block = [[i[0], i[1]+1] for i in block[:-1]] + [block[-1]]
            
        if keyboard.is_pressed('w'):
            blockstyle = [[list(reversed(i)) for i in list(zip(*blockstyle[0]))]] + [blockstyle[-1]]
            newblock = [i for i in sum([[[j, i] if blockstyle[0][i][j] == 1 else None for j in range(len(blockstyle[0][i]))] for i in range(len(blockstyle[0]))], []) if i] + [blockstyle[1]]
            height = math.ceil(sum([i[1] for i in block[:-1]]) / len(block[:-1]))-1
            width = math.ceil(sum([i[0] for i in block[:-1]]) / len(block[:-1]))-1
            block = [[i[0]+width, i[1]+height] for i in newblock[:-1]] + [newblock[-1]]
        if keyboard.is_pressed('space'):
            if stop == True:
                stop = False
            else:
                stop = True
        time.sleep(0.08)

clock = pygame.time.Clock()
style = [[[[1, 1, 1, 1], [0, 0, 0, 0]], (0, 255, 255)],
          [[[1, 0, 0], [1, 1, 1]], (0, 0, 255)],
          [[[0, 1, 0], [1, 1, 1]], (255, 0, 255)],
          [[[1, 1], [1, 1]], (255, 255, 0)],
          [[[0, 0, 1], [1, 1, 1]], (255, 185, 0)],
          [[[1, 1, 0], [0, 1, 1]], (255, 0, 0)],
          [[[0, 1, 1], [1, 1, 0]], (0, 255, 0)]]
count = []
done = []
doneblock = []
score = 0
stop = False
blockstyle, block = get_random_style()
pygame.init()
pygame.display.set_caption('Tetris')
font = pygame.font.Font('font.ttf', 32)
file = 'theme.mp3'
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play(-1)
screen = pygame.display.set_mode((400, 400))
run = True
x = threading.Thread(target=detect_move)
x.daemon = True
x.start()

def main():
    global run
    global count
    global stop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if not stop:
            if len(count) == 20:   
                count = []
            else:
                count.append(1)
            update()
            block_movement(count)
            check_score()
        clock.tick(60)
        pygame.display.update()

if __name__ == '__main__':
    main()

quit()
