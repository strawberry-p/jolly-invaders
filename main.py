import pygame as pg
import asyncio
import random as r
FPS = 60
SCALE = 30
SIZE = SCALE*32
px,py = (15,31)
colors = ["red", "yellow", "blue","green","purple","orange"]
clr = 0
inc = 0
class Bullet:
    def __init__(self, color: int, x:int, dir: tuple[int,int] = (0,-1)):
        self.clr = color
        self.x = x
        self.y = 30
        self.dx = dir[0]
        self.dy = dir[1]
async def player_spot(mat:pg.Surface):
    mat.set_at((px,py),colors[clr])
    mat.set_at((px-1,py),"white")
    mat.set_at((px+1,py),"white")
    mat.set_at((px,py-1),"white")
async def main():
    global px,py,inc,clr
    pg.init()
    sc = pg.display.set_mode((SIZE,SIZE))
    clk = pg.time.Clock()
    mat = pg.Surface((32,32))
    running = True
    while running:
        inc += 1
        if inc >= FPS//2:
            print(clr)
            inc = 0
            if r.randrange(2*len(colors)) == 0: clr = r.randrange(len(colors))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                k = event.key
                if k == pg.K_a or k == pg.K_LEFT:
                    px -= 1
                    if px < 0: px = 31
                elif k == pg.K_d or k == pg.K_RIGHT:
                    px += 1
                    if px > 31: px = 0
        mat.fill("black")
        await player_spot(mat)
        sc.blit(pg.transform.scale(mat,(SIZE,SIZE)),(0,0))
        pg.display.flip()
        clk.tick(FPS)
        await asyncio.sleep(0)
    pg.quit()

asyncio.run(main())
