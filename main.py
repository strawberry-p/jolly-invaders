import pygame as pg
import asyncio
import random as r
FPS = 60
SCALE = 30
SIZE = SCALE*32
OFF = 30
px,py = (15,31)
colors = ["red", "yellow", "blue","green","purple","orange"]
bullet_colors = [(180,0,0),(90+OFF,90+OFF,0),(0,0,180),(0,180,0),(90,0,90),(120+OFF,60+OFF,0)]
bullets: list[Bullet] = []
clr = 1
inc = 0
shoot_inc = 0
bmove_inc = 0
class Bullet:
    def __init__(self, color: int, x:int, dir: tuple[int,int] = (0,-1)):
        self.clr = color
        self.x = x
        self.y = 30
        self.dx = dir[0]
        self.dy = dir[1]
    def move(self):
        self.x += self.dx
        self.y += self.dy
        if not (0 <= self.x <= 31): return True
        if self.y < 0: return True
        else:
            return False
    def dsp(self,mat:pg.Surface):
        mat.set_at((self.x,self.y),bullet_colors[self.clr])

async def player_spot(mat:pg.Surface):
    mat.set_at((px,py),colors[clr])
    mat.set_at((px-1,py),"white")
    mat.set_at((px+1,py),"white")
    mat.set_at((px,py-1),"white")
async def main():
    global px,py,inc,clr,shoot_inc,bmove_inc
    pg.init()
    sc = pg.display.set_mode((SIZE,SIZE))
    clk = pg.time.Clock()
    mat = pg.Surface((32,32))
    running = True
    while running:
        inc += 1
        shoot_inc += 1
        bmove_inc += 1
        if bmove_inc >= FPS//5:
            bmove_inc = 0
            i = 0
            while i < len(bullets):
                b = bullets[i]
                if b.move():
                    bullets.pop(i)
                else: i += 1
        if shoot_inc >= (2*FPS)//3:
            shoot_inc = 0
            bullets.append(Bullet(clr,px))
        if inc >= FPS//2:
            print(clr)
            inc = 0
            if r.randrange(2//2*len(colors)) == 0: clr = r.randrange(len(colors))
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
        for b in bullets:
            b.dsp(mat)
        await player_spot(mat)
        sc.blit(pg.transform.scale(mat,(SIZE,SIZE)),(0,0))
        pg.display.flip()
        clk.tick(FPS)
        await asyncio.sleep(0)
    pg.quit()

asyncio.run(main())
