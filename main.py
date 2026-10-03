import pygame as pg
import asyncio
import random as r
FPS = 60
SCALE = 30
SIZE = SCALE*32
OFF = 30
ENEMYTIME = 30
px,py = (15,31)
colors2 = ["red", "yellow", "blue","green","purple","orange"]
bullet_colors2 = [(180,0,0),(90+OFF,90+OFF,0),(0,0,180),(0,180,0),(90,0,90),(120+OFF,60+OFF,0)]
colors = ["red","yellow","blue"]
bullet_colors = [(180,0,0),(90+OFF,90+OFF,0),(0,0,180)]
#scheduled: list[list[int,int]] = [[2,0],[2,1],[2,2],[2,3],[2,4],[2,5],[2,0],[2,1],[2,2],[2,3],[2,4],[2,5],[2,0],[2,1],[2,2],[2,3]]
scheduled: list[list[int,int]] = [[2,0],[2,1],[2,2],[2,0],[2,1],[2,2],[2,0],[2,1],[2,2],[2,0],[2,1],[2,2],[2,0],[2,1],[2,2],[2,0]]
bullets: list = []
foes: list[list] = [] #believe it or not they're bullets too
clr = 1
inc = 0
shoot_inc = 0
bmove_inc = 0
enemy_inc = 0
class Bullet:
    def __init__(self, color: int, x:int, dir: tuple[int,int] = (0,-1),enemy:bool = False):
        self.clr = color
        self.x = x
        if enemy: self.y = 0
        else: self.y = 30
        self.dx = dir[0]
        self.dy = dir[1]
        self.is_enemy: bool = enemy
        self.dying = False
    def move(self):
        self.x += self.dx
        self.y += self.dy
        if not (0 <= self.x <= 31): return True
        elif self.dying: return True
        elif self.y < 0: return True
        elif self.y >= 29 and self.is_enemy and not self.dying: raise Exception("Loss ",self.clr)
        elif not self.is_enemy:
            if len(foes[self.x//2]):
                enemy = foes[self.x//2][0]
                if enemy.x//2 == self.x//2 and enemy.y//2 == self.y//2:
                    if enemy.clr == self.clr:
                        if not enemy.dying:
                            print(f"enemy at y {enemy.y} x {enemy.x} dying. killed by {self.is_enemy} at {self.y} {self.x}")
                            enemy.dying = True
                    return True
            else: print(f"free column {self.x//2}")

        return False
    def dsp(self,mat:pg.Surface):
        if self.dying: color = "gray"
        elif self.is_enemy: color = colors[self.clr]
        else: color = bullet_colors[self.clr]
        #if not self.is_enemy: print(f"displaying {color} at {(self.x,self.y)}")
        mat.set_at((self.x,self.y),color)
        if self.is_enemy:
            mat.set_at((self.x+1,self.y),color)
            mat.set_at((self.x,self.y+1),color)
            mat.set_at((self.x+1,self.y+1),color)

async def player_spot(mat:pg.Surface):
    mat.set_at((px,py),colors[clr])
    mat.set_at((px-1,py),"white")
    mat.set_at((px+1,py),"white")
    mat.set_at((px,py-1),"white")
    await asyncio.sleep(0)
async def main():
    global px,py,inc,clr,shoot_inc,bmove_inc,enemy_inc,ENEMYTIME
    pg.init()
    sc = pg.display.set_mode((SIZE,SIZE))
    clk = pg.time.Clock()
    mat = pg.Surface((32,32))
    running = True
    i = 0
    for s in scheduled:
        print(s)
        foes.append([Bullet(s[1],2*i,(0,2),True) for x in range(s[0])])
        i += 1
    while running:
        inc += 1
        shoot_inc += 1
        bmove_inc += 1
        if bmove_inc >= FPS//6:
            bmove_inc = 0
            for col in foes:
                if len(col) and col[0].dying: col.pop(0)
            i = 0
            while i < len(bullets):
                b = bullets[i]
                if b.move():
                    bullets.pop(i)
                else: i += 1
            enemy_inc += 1
        if enemy_inc >= ENEMYTIME:
            enemy_inc = 0
            i = 0
            while i < len(foes):
                if scheduled[i][0] <= 0:
                    scheduled[i] = [r.randrange(8),r.randrange(len(colors))]
                col = foes[i]
                j = 0
                for enemy in col:
                    try:
                        if enemy.move(): foes[i].pop(j)
                        else: j += 0
                    except BaseException as _:
                        foes[i].pop(j)
                        mat.fill("black")
                        for k in range(32):
                            mat.set_at((k,k),"white")
                            mat.set_at((31-k,k),"white")
                            await asyncio.sleep(0)
                        sc.blit(pg.transform.scale(mat,(SIZE,SIZE)),(0,0))
                        pg.display.flip()
                        await asyncio.sleep(0)
                        clk.tick(1)
                        running = False
                        await asyncio.sleep(0)
                        break
                        pass
                scheduled[i][0] -= 1
                foes[i].append(Bullet(scheduled[i][1],2*i,(0,2),True))
                i += 1
            print(scheduled)
        if shoot_inc >= (2*FPS)//3:
            shoot_inc = 0
            bullets.append(Bullet(clr,px))
            print([x.__dict__ for x in bullets])
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
        for col in foes:
                for i in col:
                    i.dsp(mat)
        await player_spot(mat)
        sc.blit(pg.transform.scale(mat,(SIZE,SIZE)),(0,0))
        pg.display.flip()
        clk.tick(FPS)
        await asyncio.sleep(0)
    pg.quit()

asyncio.run(main())
