import time
import pygame as p
import sqlite3 as sq
p.init()
player = p.sprite.Group()
x = 0
y = 0
s = 1000
recname = []
save = True
f = p.font.SysFont('serif', 48)

conn = sq.connect('qwer.db')
cur = conn.cursor()
q = "CREATE TABLE IF NOT EXISTS user(name TEXT, s INT)"
cur.execute(q)


class Player(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        self.image = p.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (75, 350)
        self.x = 0
        self.y = 0
    def update(self) :
        self.rect.x += self.x
        self.rect.y += self.y
class Vrag (p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.image = p.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.y = 10
    def update(self) :
        if self.rect.bottom>650 or self.rect.top<50:
            self.y = -self.y
        self.rect.y += self.y
scr = p.display.set_mode((1350, 700))
all = p.sprite.Group()
im = p.image.load('2.png').convert_alpha()
IM = p.transform.scale(im, (50, 50))
vragsrect = []
vrags = [object, object, object, object, object, object, object, object]
loos = False
win = False
for i in range(0, 8):
    vrags[i] = Vrag(150+150*i, 80+540*(i%2))
    vrags[i].image = IM
    all.add(vrags[i])
    vragsrect.append(vrags[i].rect)
player = Player()
im = p.image.load('1.jpg').convert_alpha()
IM = p.transform.scale(im, (50, 50))
player.image = IM
all.add(player)
print(len(all))
run = True
nik = True
NIK = ""
while run:
    scr = p.display.set_mode((1350, 700))

    while nik:
        scr = p.display.set_mode((1350, 700))
        a = f.render('enter your name', False, (255, 0, 0))
        scr.blit(a, (1100 / 2, 100))

        text_nik = f.render(NIK, False, (255, 0, 0))
        scr.blit(text_nik, (1100 / 2, 250))
        p.display.flip()
        for i in p.event.get():
            if i.type == p.QUIT:
                nik = False
                run = False
            if i.type == p.KEYDOWN:

                if i.key == p.K_RETURN:
                    nik = False

                    p.display.flip()
                elif i.key == p.K_BACKSPACE:
                    NIK = NIK[0:len(NIK)-1]
                    text_nik = f.render(NIK, False, (255, 0, 0))
                    scr.blit(text_nik, (1100 / 2, 250))
                    p.display.flip()
                elif len(NIK) < 14:
                    NIK += i.unicode

    p.draw.polygon(scr, (255, 0, 0), [[0, 0], [1350, 0], [1350, 50], [50, 50], [50, 650], [1300, 650], [1300, 50], [1350, 50], [1350, 700], [0, 700]])
    p.draw.rect(scr, (0, 255, 0), ([1250, 50], [1300, 600]))
    all.draw(scr)
    d = scr.get_at((player.rect.right-26, player.rect.bottom ))
    r = scr.get_at((player.rect.right+1, player.rect.top+26))
    l = scr.get_at((player.rect.left-1, player.rect.top+26))
    t = scr.get_at((player.rect.right-26, player.rect.top-2))
    for i in p.event.get():
        if i.type == p.QUIT:
            run = False
        if i.type == p.KEYDOWN:
            if i.key == p.K_LEFT and l ==(0, 0, 0, 255):
                player.x = -5
            if i.key == p.K_RIGHT and r ==(0, 0, 0, 255):
                player.x = 5
            if i.key == p.K_UP and t ==(0, 0, 0, 255):
                player.y = -5
            if i.key == p.K_DOWN and d ==(0, 0, 0, 255):
                player.y = 5

        if i.type == p.KEYUP:
            if i.key == p.K_LEFT:
                player.x = 0
            if i.key == p.K_RIGHT:
                player.x = 0
            if i.key == p.K_UP:
                player.y = 0
            if i.key == p.K_DOWN:
                player.y = 0
    if d != (0, 0, 0, 255) and player.y>0:
        player.y = 0
    if t != (0, 0, 0, 255) and player.y<0:
        player.y = 0
    if l != (0, 0, 0, 255) and player.x<0:
        player.x = 0
    if r != (0, 0, 0, 255) and player.x>0:
        player.x = 0
    if player.rect.collidelist(vragsrect) != -1:
        s = 0
        loos = True
    if r == (0, 255, 0):
        win = True

    while win == True or loos == True:

        if  save:
            sTr = (NIK, s)
            cur.execute("INSERT INTO user VALUES(?, ?)", sTr)
            conn.commit()
            save = False

        cur.execute("SELECT * FROM user")
        aa = cur.fetchall()
        save = False
        rec = []

        for i in aa:
            rec.append(i[1])
        Rec = sorted(rec)

        for i in p.event.get():
            if i.type == p.QUIT:
                run = False
                win = False
                loos = False
            if i.type == p.KEYDOWN:
                if i.key == p.K_r:
                    nik = True
                    win = False
                    loos = False
                    player.rect.center = (75, 350)
                    player.x = 0
                    player.y = 0
                    s = 1000

        p.draw.rect(scr, (255, 255, 0), ([0, 0], [1350, 700]))
        text1 = f.render('R - restart', False, (0, 0, 0))
        best = f.render('THE BEST', False, (0, 0, 0))
        for i in range(1, len(Rec)):
            for j in range(0, len(aa)):
                if Rec[-i] == aa[j][1] and aa[j][0] not in recname :
                    recname.append(aa[j][0])
        print(Rec)
        print(recname)
        if win:
            text = f.render("YOU WIN", False, (0, 0, 0))
        if loos:
            text = f.render("YOU LOOS", False, (0, 0, 0))
        nic1 = f.render(recname[0], False, (0, 0, 0))
        nic2 = f.render(recname[1], False, (0, 0, 0))
        nic3 = f.render(recname[2], False, (0, 0, 0))
        nic4 = f.render(recname[3], False, (0, 0, 0))
        nic5 = f.render(recname[4], False, (0, 0, 0))

        sum = f.render(str(s), False, (0, 0, 0))
        sum1 = f.render(str(Rec[-1]), False, (0, 0, 0))
        sum2 = f.render(str(Rec[-2]), False, (0, 0, 0))
        sum3 = f.render(str(Rec[-3]), False, (0, 0, 0))
        sum4 = f.render(str(Rec[-4]), False, (0, 0, 0))
        sum5 = f.render(str(Rec[-5]), False, (0, 0, 0))


        scr.blit(nic1,(1000/2, 250))
        scr.blit(nic2,(1000/2, 300))
        scr.blit(nic3,(1000/2, 350))
        scr.blit(nic4,(1000/2, 400))
        scr.blit(nic5,(1000/2, 450))

        scr.blit(sum1,(700, 250))
        scr.blit(sum2,(700, 300))
        scr.blit(sum3,(700, 350))
        scr.blit(sum4,(700, 400))
        scr.blit(sum5,(700, 450))

        scr.blit(sum,(1100/2, 20))


        scr.blit(text, (1100/2, 100))
        scr.blit(text1, (1100/2, 650))
        scr.blit(best, (1100/2, 200))

        p.display.flip()
    if s>0:
        s = s - 1
    cout = f.render(str(s), False, (0, 0, 0))
    scr.blit(cout, (1100/2, 0))
    all.update()
    p.display.flip()
    time.sleep(0.001)