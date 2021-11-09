import time
import pygame as p
import sqlite3 as sq
p.init()
player = p.sprite.Group() #создание группы игрока
s = 1000 #счёт
FPS = 30# количество кадров в секунду
recname = [] #список ников игроков в убывающем порядке
save = True #добавлять в базу или нет. Чтобы добавить только один раз
f = p.font.SysFont('serif', 48) #шрифт и его размер
clock = p.time.Clock() #создание задержки
class Base: # работа с базой данных
    def __init__(self, name = 'qwer.db'): # создание базы
        self.con = sq.connect(name) # создание соединения
        self.cur = self.con.cursor() # создание курсора
        self.create_table() # создание таблицы
    def create_table(self, name='score'): # создание таблицы
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS '{name}'(nic text, score int)""") # создание таблицы score
    def insert(self, nic_us, score, name='score'):# добавление
        self.cur.execute(f"""INSERT INTO {name} (nic, score) VALUES('{nic_us}', '{score}')
""") # добавление данных в таблицу
        self.con.commit() # сохранение изменений
    def all(self, name='score'): # получение данных таблицы
        self.cur.execute(f"SELECT * FROM {name}") # выделение всей таблицы
        return self.cur.fetchall() # возврат данных
    def __del__(self): # закрытие соединения
        self.con.close()


class Player(p.sprite.Sprite): #класс игрока
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        self.image = p.Surface((50, 50)) # размер персонажа
        self.rect = self.image.get_rect() #создание "хитбокса"
        self.rect.center = (75, 350) #установка начальных координат игрока
        self.x = 0 #скорость по х
        self.y = 0 #скорость по у
    def update(self) :
        self.rect.x += self.x #движение по х
        self.rect.y += self.y #движение по у
class Vrag (p.sprite.Sprite): #класс врага
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.image = p.Surface((50, 50)) # размер врага
        self.rect = self.image.get_rect() # создание "хитбокса"
        self.rect.center = (x, y) #установка начальных координат врага
        self.y = 25 # скорость движения врага
    def update(self) :
        if self.rect.bottom>650 or self.rect.top<50: # касание границ экрана
            self.y = -self.y# смена направления движения
        self.rect.y += self.y# движение врага
scr = p.display.set_mode((1350, 700)) # создание окна игры для загрузки изображений
all = p.sprite.Group() # создание группы врагов
im = p.image.load('2.png').convert_alpha() # загрузка изображения врага
IM = p.transform.scale(im, (50, 50)) # уменьшение изображения до 50х50
vragsrect = [] # список хитбоксов врагов для отслеживания касания с игроком
vrags = [object, object, object, object, object, object, object, object]# список врагов
loos = False # переменная проигрыша
win = False # переменная выигрыша
text_score = f.render('score', False, (0, 0, 0)) # создание надписи score
text1 = f.render('R - restart', False, (0, 0, 0)) # подготовка надписи о рестарте
best = f.render('THE BEST', False, (0, 0, 0)) #подготовка надписи лучшие
for i in range(0, 8): # цикл создания врагов
    vrags[i] = Vrag(150+150*i, 80+540*(i%2)) # создание врагов в определённых координатах
    vrags[i].image = IM # наложение на врагов изображений
    all.add(vrags[i]) # добавление в группу
    vragsrect.append(vrags[i].rect) # добавление хитбокса врага в список
player = Player() # создание персонажа
im = p.image.load('1.jpg').convert_alpha() # загрузка изображения персонажа
IM = p.transform.scale(im, (50, 50)) # изменение разера изображения
player.image = IM # наложение изображение на иггрока
all.add(player) # добавление игрока в собственную группу
run = True # переменная для основного цикла
nik = True # переменная для цикла ввода ника
NIK = "" # ник игрока
sqbase = Base() # создание базы
sqbase.create_table() # создание таблицы
records = sqbase.all() # получение информации из базы на случай если игрок проиграет
if len(records)<5: # если в базе нет 5 строк
    for i in range(5): # заполняем 5 строк
        sqbase.insert('nobody', i)
records = sqbase.all() # получение банных из базы
score = []# создание списка для счёта
for i in records: #заполнение списка счёта
    score.append(i[1])
score.sort() # сортировка списка для выявления рекордсменов
top_nik = [] # список имён рекордсменов
top_score = [] #список счёта рекордсменов
for i in range(-1, -6, -1): # сборка лучших результатов в список
    top_score.append(score[i])
for i in top_score: # сборка ников рекордсменов
    for j in records:
        if i == j[1]:
            top_nik.append(j[0])
text_num_score = f.render(str(s), False, (0, 0, 0))
top_nik_text = []# список для ников в таблице рекордов
top_score_text = [] # список для счёта в таблице рекордов
for i in range(5): # создание надписей ников и счета рекордсменов
    top_nik_text.append(f.render(top_nik[i], False, (0, 0, 0)))
    top_score_text.append(f.render(str(top_score[i]), False, (0, 0, 0)))
while run: # основной цикл
    scr = p.display.set_mode((1350, 700)) #пересоздание экрана
    while nik: # цикл ввода ника
        a = f.render('enter your name', False, (255, 0, 0)) # создание надписи введи имя
        scr.blit(a, (1100 / 2, 100)) # прорисовка надписи введи имя на экране
        text_nik = f.render(NIK, False, (255, 0, 0)) # создание надписи ника игрока
        scr.blit(text_nik, (1100 / 2, 250)) # вывод ника на экран
        p.display.flip() # обновление экрана экрана
        for i in p.event.get(): # цикл обработки событий
            if i.type == p.QUIT: # закрытие окна
                nik = False # выход из цикла ввода ника
                run = False # выход из основного цикла
                sqbase.__del__() # удаление соединения
            if i.type == p.KEYDOWN: # обработка событий нажатия клавишь
                if i.key == p.K_RETURN: # обработка нажатия на enter
                    nik = False # выход из цикла ввода ника
                    p.display.flip()# обновление экрана
                elif i.key == p.K_BACKSPACE: # обработка нажатия на backspace
                    scr = p.display.set_mode((1350, 700)) # очищение экрана
                    NIK = NIK[0:len(NIK)-1] # удаление последнего символа
                    text_nik = f.render(NIK, False, (255, 0, 0)) # перезапись надписи ника
                    scr.blit(text_nik, (1100 / 2, 250)) # прорисовка ника
                    p.display.flip() #обновление экрана
                elif len(NIK) < 14: # ограничение 14 символов
                    NIK += i.unicode # добавление символа нажатой кнопки в конец ника

    p.draw.polygon(scr, (255, 0, 0), [[0, 0], [1350, 0], [1350, 50],
                                      [50, 50], [50, 650], [1300, 650],
                                      [1300, 50], [1350, 50], [1350, 700],
                                      [0, 700]]) # прорисовка рамки
    p.draw.rect(scr, (0, 255, 0), [1300, 50, 50, 600]) # прорисовка финишной линии
    all.draw(scr) # прорисовка врагов
    d = scr.get_at((player.rect.right-26, player.rect.bottom )) # определение цвета пикселя под игроком
    r = scr.get_at((player.rect.right+1, player.rect.top+26)) # определение цвета пикселя справа от игрока
    l = scr.get_at((player.rect.left-1, player.rect.top+26)) # определение цвета пикселя слева от игрока
    t = scr.get_at((player.rect.right-26, player.rect.top-2)) # определение цвета пикселя сверху от игрока
    for i in p.event.get(): # обработка событий
        if i.type == p.QUIT: # обработка закрытия окна
            run = False # выход из основного цикла
            sqbase.__del__()# удаление соединения
        if i.type == p.KEYDOWN: # обработка нажатия на клавиши
            if i.key == p.K_LEFT and l ==(0, 0, 0, 255): # стрелка влево
                player.x = -5 # движение влево
            if i.key == p.K_RIGHT and r ==(0, 0, 0, 255): # стрелка вправо
                player.x = 5 # движение вправо
            if i.key == p.K_UP and t ==(0, 0, 0, 255): # стрелка вверх
                player.y = -5 # движение вверх
            if i.key == p.K_DOWN and d ==(0, 0, 0, 255): # стрелка вниз
                player.y = 5 # движение вниз

        if i.type == p.KEYUP: # обработка отжатия клавишь
            if i.key == p.K_LEFT: # стрелка влево
                player.x = 0 # установка нуливой скорости
            if i.key == p.K_RIGHT: # стрелка вправо
                player.x = 0 # установка нуливой скорости
            if i.key == p.K_UP: # стрелка вверх
                player.y = 0 # установка нуливой скорости
            if i.key == p.K_DOWN: # стрелка вниз
                player.y = 0 # установка нуливой скорости
    if d != (0, 0, 0, 255) and player.y>0: # если пиксель снизу не чёрный
        player.y = 0 # установка нуливой скорости
    if t != (0, 0, 0, 255) and player.y<0: # если пиксель сверху не чёрный
        player.y = 0 # установка нуливой скорости
    if l != (0, 0, 0, 255) and player.x<0: # если пиксель слева не чёрный
        player.x = 0 # установка нуливой скорости
    if r != (0, 0, 0, 255) and player.x>0: # если пиксель справа не чёрный
        player.x = 0 # установка нуливой скорости
    if player.rect.collidelist(vragsrect) != -1: # если хитпоинт игрока соприкосается с хитпоинтом одного из врагов
        s = 0 # обнуление счёта
        loos = True # запуск цикла проигрыша
        text_num_score = f.render(str(s), False, (0, 0, 0)) # создание надписи очков в последней игре
    if r == (0, 255, 0): # если пиксел справа зелёный
        win = True # запуск цикла победы
        sqbase.insert(NIK, s) # добавление результатов в базу
        records = sqbase.all() # получение всей информации из базы
        score = [] # список для счёта
        for i in records: # заполнение списка для счёта
            score.append(i[1])
        score.sort() # сортировка сиска со счётом для выявления 5 лучших
        top_nik = [] #список лучших ников
        top_score = [] # список лучших очков
        for i in range(-1, -6, -1):# отбор 5 лучших очков
            top_score.append(score[i])
        for i in top_score:# отбор 5 лучших иков
            for j in records:
                if i == j[1]:
                    top_nik.append(j[0])
        text_num_score = f.render(str(s), False, (0, 0, 0)) # создание надписи счёта последней игры
        top_nik_text = [] # список надписей ников рекордсменов
        top_score_text = [] # список надписей счёта рекордсменов
        for i in range(5): # заполнение списков для таблицы рекордов
            top_nik_text.append(f.render(top_nik[i], False, (0, 0, 0)))
            top_score_text.append(f.render(str(top_score[i]), False, (0, 0, 0)))
    while win == True or loos == True: # цикл победы и поражения
        for i in p.event.get(): # обработка событий
            if i.type == p.QUIT: # закрытие окна
                run = False # выход из основного цикла
                win = False # выход из цикла победы
                loos = False # выход из цикла поражения
                sqbase.__del__()# удаление соединения
            if i.type == p.KEYDOWN: # обработка нажатия клавишь
                if i.key == p.K_r: # если клавша R нажата
                    nik = True # запуск цикла записи ника
                    win = False # выход из цикла победы
                    loos = False # выход из цикла поражения
                    player.rect.center = (75, 350) # возврат игрока на начальные координаты
                    player.x = 0 # обнуление скорости игрока по х
                    player.y = 0 # обнуление скорости игрока по у
                    s = 1000 # подготовка счёта к новой игре

        p.draw.rect(scr, (255, 255, 0), ([0, 0], [1350, 700])) # прорисовка жёлтого фона

        if win: # если победил
            text = f.render("YOU WIN", False, (0, 0, 0)) # подготовка надписи о победе
        if loos: # если проиграл
            text = f.render("YOU LOOS", False, (0, 0, 0)) # подготовка надписи о поражении

        scr.blit(text_score,(550, 20)) # вывод надписи score
        scr.blit(text_num_score,(700, 20)) # вывод счёта последней игры
        scr.blit(text, (1100/2, 100)) # прорисовка текста о победе или поражении
        scr.blit(text1, (1100/2, 650)) # прорисовка надписи о рестарте
        scr.blit(best, (1100/2, 200)) # прорисовка надписи лучшие
        for i in range(5):# прорисовка таблицы рекордов
            scr.blit(top_nik_text[i], (500, 300+50*i))
            scr.blit(top_score_text[i], (800, 300+50*i))
        p.display.flip() # обновение экрана
    if s>0: # если счётчик больше 0
        s = s - 1 # уменьшение счётчика
    cout = f.render(str(s), False, (0, 0, 0))
    scr.blit(cout, (1100/2, 0))
    all.update() # вызов функции движения игрока
    p.display.flip() # обновление эерана
    clock.tick(FPS)#задержка
