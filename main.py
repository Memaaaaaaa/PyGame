import sqlite3 as sq
import pygame as pg

pg.init()

player = pg.sprite.Group()  # создание группы игрока
game_score = 1000  # счёт
FPS = 30  # количество кадров в секунду
recname = []  # список ников игроков в убывающем порядке
f = pg.font.SysFont('serif', 48)  # шрифт и его размер
clock = pg.time.Clock()  # создание задержки


class Base:  # работа с базой данных
    """__init__ - создание базы, соединения и курсора
       create_table - создание таблицы
       insert - добавление информации в таблицу
       insert_into - добавление в определённое место
       give_something - получить счёт игрока по его нику
       all - запрос на данные из всей таблицы
       del - удаление соединения"""
    def __init__(self, name='qwer.db'):  # создание базы
        self.con = sq.connect(name)  # создание соединения
        self.cur = self.con.cursor()  # создание курсора
        self.create_table()  # создание таблицы

    def create_table(self, name='score'):  # создание таблицы
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS '{name}'(nic text, score int)""")  # создание таблицы score

    def insert(self, nic_us, score, name='score'):  # добавление
        self.cur.execute(f"""INSERT INTO {name} (nic, score) VALUES('{nic_us}', '{score}')
                            """)  # добавление данных в таблицу
        self.con.commit()  # сохранение изменений
    def insert_into(self, name_us, score, name = 'score'): # перезапись счёта игрока
        self.cur.execute(f"""
        UPDATE '{name}' SET score = '{score}' WHERE nic = '{name_us}'""")
        self.con.commit()   # сохранение изменений
    def give_something(self, nic_us, name = 'score'):   # получение счёта определённого игрока
        self.cur.execute(f"""SELECT score FROM '{name}' WHERE nic = '{nic_us}'""")   # выделение нужного
        return self.cur.fetchone()   # возврат счёта игрока
    def all(self, name='score'):  # получение данных таблицы
        self.cur.execute(f"SELECT * FROM {name}")  # выделение всей таблицы
        return self.cur.fetchall()  # возврат данных

    def __del__(self):  # закрытие соединения
        self.con.close()


class Player(pg.sprite.Sprite):  # класс игрока
    """_init_ - создание игрока его хитбокса и наложение текстуры
        update - движение игрока по осям Х и У"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load('1.jpg').convert_alpha(), (50, 50))  # размер персонажа
        self.rect = self.image.get_rect()  # создание "хитбокса"
        self.rect.center = (75, 350)  # установка начальных координат игрока
        self.x = 0  # скорость по х
        self.y = 0  # скорость по у

    def update(self):
        self.rect.x += self.x  # движение по х
        self.rect.y += self.y  # движение по у


class Vrag(pg.sprite.Sprite):  # класс врага
    """__init__ - создание объекта врага с хитбоксом и текстурой
       update - движение врага с отскоком от стены"""
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
          # загрузка изображения врага
          # уменьшение изображения до 50х50
        self.image = pg.transform.scale(pg.image.load('2.png').convert_alpha(), (50, 50))  # размер врага
        self.rect = self.image.get_rect()  # создание "хитбокса"
        self.rect.center = (x, y)  # установка начальных координат врага
        self.y = 25  # скорость движения врага

    def update(self):
        if self.rect.bottom > 650 or self.rect.top < 50:  # касание границ экрана
            self.y = -self.y  # смена направления движения
        self.rect.y += self.y  # движение врага


scr = pg.display.set_mode((1350, 700))  # создание окна игры для загрузки изображений
all = pg.sprite.Group()  # создание группы врагов

vrags_rect = []  # список хитбоксов врагов для отслеживания касания с игроком
vrags = [object for i in range(8)]  # список врагов

loos = False  # переменная проигрыша
win = False  # переменная выигрыша

text_score = f.render('score', False, (0, 0, 0))  # создание надписи score
text_restart = f.render('R - restart', False, (0, 0, 0))  # подготовка надписи о рестарте
best = f.render('THE BEST', False, (0, 0, 0))  # подготовка надписи лучшие
rul_text = ['идти вверх - стрелка вверх',
            'идти вниз - стрелка вниз',
            'идти вправо - стрелка вправо',
            'идти влево - стрелка влево',
            'дойди до зелёного']   # текст правил
ruls = [f.render(rul_text[i], False, (255, 0, 0)) for i in range(5)] # правила игры

for i in range(0, 8):  # цикл создания врагов
    vrags[i] = Vrag(150 + 150 * i, 80 + 540 * (i % 2))  # создание врагов в определённых координатах
    all.add(vrags[i])  # добавление в группу
    vrags_rect.append(vrags[i].rect)  # добавление хитбокса врага в список

player = Player()  # создание персонажа

all.add(player)  # добавление игрока в собственную группу

run = True  # переменная для основного цикла
nik = True  # переменная для цикла ввода ника
nicname = ""  # ник игрока
sq_base = Base()  # создание базы
sq_base.create_table()  # создание таблицы
records = sq_base.all()  # получение информации из базы на случай если игрок проиграет
bot_name = ['nobody1',
            'nobody2',
            'nobody3',
            'nobody4',
            'nobody5'] # имена ботов
if len(records) < 5:  # если в базе нет 5 строк
    for i in range(5):  # заполняем 5 строк
        sq_base.insert(bot_name[i], i)

records = sq_base.all()  # получение банных из базы
score = []  # создание списка для счёта

for i in records:  # заполнение списка счёта
    score.append(i[1])

score.sort()  # сортировка списка для выявления рекордсменов
top_nik = []  # список имён рекордсменов
top_score = []  # список счёта рекордсменов

for i in range(-1, -6, -1):  # сборка лучших результатов в список
    top_score.append(score[i])

for i in top_score:  # сборка ников рекордсменов
    for j in records:
        if i == j[1]:
            top_nik.append(j[0])

text_num_score = f.render(str(game_score), False, (0, 0, 0)) # текст счёта последней игры
top_nik_text = []  # список для ников в таблице рекордов
top_score_text = []  # список для счёта в таблице рекордов

for i in range(5):  # создание надписей ников и счета рекордсменов
    top_nik_text.append(f.render(top_nik[i], False, (0, 0, 0)))
    top_score_text.append(f.render(str(top_score[i]), False, (0, 0, 0)))

while run:  # основной цикл
    scr = pg.display.set_mode((1350, 700))  # пересоздание экрана

    while nik:  # цикл ввода ника
        y_rul_text = 500  # координата у правил

        for i in range(5):  # прорисовка правил
            scr.blit(ruls[i], (450, y_rul_text))  # прорисовка правил
            y_rul_text += 35

        a = f.render('enter your name', False, (255, 0, 0))  # создание надписи введи имя
        scr.blit(a, (1100 / 2, 100))  # прорисовка надписи введи имя на экране
        text_nik = f.render(nicname, False, (255, 0, 0))  # создание надписи ника игрока
        scr.blit(text_nik, (1100 / 2, 250))  # вывод ника на экран

        for i in pg.event.get():  # цикл обработки событий
            if i.type == pg.QUIT:  # закрытие окна
                nik = False  # выход из цикла ввода ника
                run = False  # выход из основного цикла
                sq_base.__del__()  # удаление соединения

            if i.type == pg.KEYDOWN:  # обработка событий нажатия клавишь
                if i.key == pg.K_RETURN:  # обработка нажатия на enter
                    nik = False  # выход из цикла ввода ника

                elif i.key == pg.K_BACKSPACE:  # обработка нажатия на backspace
                    scr = pg.display.set_mode((1350, 700))  # очищение экрана
                    nicname = nicname[0:len(nicname) - 1]  # удаление последнего символа
                    text_nik = f.render(nicname, False, (255, 0, 0))  # перезапись надписи ника
                    scr.blit(text_nik, (1100 / 2, 250))  # прорисовка ника

                elif len(nicname) < 14:  # ограничение 14 символов
                    nicname += i.unicode  # добавление символа нажатой кнопки в конец ника
        pg.display.flip()
    pg.draw.polygon(scr, (255, 0, 0), [[0, 0], [1350, 0], [1350, 50],
                                       [50, 50], [50, 650], [1300, 650],
                                       [1300, 50], [1350, 50], [1350, 700],
                                       [0, 700]])  # прорисовка рамки
    pg.draw.rect(scr, (0, 255, 0), [1300, 50, 50, 600])  # прорисовка финишной линии
    all.draw(scr)  # прорисовка врагов

    down_color = scr.get_at((player.rect.right - 26, player.rect.bottom))  # определение цвета пикселя под игроком
    right_color = scr.get_at((player.rect.right + 1, player.rect.top + 26)) # определение цвета пикселя справа от игрока
    left_color = scr.get_at((player.rect.left - 1, player.rect.top + 26))  # определение цвета пикселя слева от игрока
    top_color = scr.get_at((player.rect.right - 26, player.rect.top - 2))  # определение цвета пикселя сверху от игрока

    for i in pg.event.get():  # обработка событий
        if i.type == pg.QUIT:  # обработка закрытия окна
            run = False  # выход из основного цикла
            sq_base.__del__()  # удаление соединения

        if i.type == pg.KEYDOWN:  # обработка нажатия на клавиши
            if i.key == pg.K_LEFT and left_color == (0, 0, 0, 255):  # стрелка влево
                player.x = -5  # движение влево

            if i.key == pg.K_RIGHT and right_color == (0, 0, 0, 255):  # стрелка вправо
                player.x = 5  # движение вправо

            if i.key == pg.K_UP and top_color == (0, 0, 0, 255):  # стрелка вверх
                player.y = -5  # движение вверх

            if i.key == pg.K_DOWN and down_color == (0, 0, 0, 255):  # стрелка вниз
                player.y = 5  # движение вниз

        if i.type == pg.KEYUP:  # обработка отжатия клавишь
            if i.key == pg.K_LEFT:  # стрелка влево
                player.x = 0  # установка нуливой скорости

            if i.key == pg.K_RIGHT:  # стрелка вправо
                player.x = 0  # установка нуливой скорости

            if i.key == pg.K_UP:  # стрелка вверх
                player.y = 0  # установка нуливой скорости

            if i.key == pg.K_DOWN:  # стрелка вниз
                player.y = 0  # установка нуливой скорости

    if down_color != (0, 0, 0, 255) and player.y > 0:  # если пиксель снизу не чёрный
        player.y = 0  # установка нуливой скорости

    if top_color != (0, 0, 0, 255) and player.y < 0:  # если пиксель сверху не чёрный
        player.y = 0  # установка нуливой скорости

    if left_color != (0, 0, 0, 255) and player.x < 0:  # если пиксель слева не чёрный
        player.x = 0  # установка нуливой скорости

    if right_color != (0, 0, 0, 255) and player.x > 0:  # если пиксель справа не чёрный
        player.x = 0  # установка нуливой скорости

    if player.rect.collidelist(vrags_rect) != -1:  # если хитпоинт игрока соприкосается с хитпоинтом одного из врагов
        game_score = 0  # обнуление счёта
        loos = True  # запуск цикла проигрыша
        text_num_score = f.render(str(game_score), False, (0, 0, 0))  # создание надписи очков в последней игре

    if right_color == (0, 255, 0):  # если пиксел справа зелёный
        win = True  # запуск цикла победы
        records = sq_base.all()  # получение всей информации из базы
        nics = []  # создание списка под ники
        for i in records:  # заполнение списка никами
            nics.append(i[0])
        if nicname in nics:  # если такой игрок уже играл
            old_score = sq_base.give_something(nicname)   # получаем его старый счёт

            if game_score > old_score[0]:   # если новый счёт больше старого
                sq_base.insert_into(nicname, game_score)  # замена счёта

        else:   # если игрока нет в базе
            sq_base.insert(nicname, game_score)   # добавляем результаты игрока в базу

        score = []  # список для счёта

        records = sq_base.all()  # получение всей информации из базы

        for i in records:  # заполнение списка для счёта
            score.append(i[1])

        score.sort()  # сортировка сиска со счётом для выявления 5 лучших
        top_nik = []  # список лучших ников
        top_score = []  # список лучших очков

        for i in range(-1, -6, -1):  # отбор 5 лучших очков
            top_score.append(score[i])

        for i in top_score:  # отбор 5 лучших иков
            for j in records:
                if i == j[1]:
                    top_nik.append(j[0])

        text_num_score = f.render(str(game_score), False, (0, 0, 0))  # создание надписи счёта последней игры
        top_nik_text = []  # список надписей ников рекордсменов
        top_score_text = []  # список надписей счёта рекордсменов

        for i in range(5):  # заполнение списков для таблицы рекордов
            top_nik_text.append(f.render(top_nik[i], False, (0, 0, 0)))
            top_score_text.append(f.render(str(top_score[i]), False, (0, 0, 0)))

    while win == True or loos == True:  # цикл победы и поражения
        for i in pg.event.get():  # обработка событий
            if i.type == pg.QUIT:  # закрытие окна
                run = False  # выход из основного цикла
                win = False  # выход из цикла победы
                loos = False  # выход из цикла поражения
                sq_base.__del__()  # удаление соединения

            if i.type == pg.KEYDOWN:  # обработка нажатия клавишь
                if i.key == pg.K_r:  # если клавша R нажата
                    nik = True  # запуск цикла записи ника
                    win = False  # выход из цикла победы
                    loos = False  # выход из цикла поражения
                    player.rect.center = (75, 350)  # возврат игрока на начальные координаты
                    player.x = 0  # обнуление скорости игрока по х
                    player.y = 0  # обнуление скорости игрока по у
                    game_score = 1000  # подготовка счёта к новой игре

        pg.draw.rect(scr, (255, 255, 0), ([0, 0], [1350, 700]))  # прорисовка жёлтого фона

        if win:  # если победил
            text = f.render("YOU WIN", False, (0, 0, 0))  # подготовка надписи о победе

        if loos:  # если проиграл
            text = f.render("YOU LOOS", False, (0, 0, 0))  # подготовка надписи о поражении

        scr.blit(text_score, (550, 20))  # вывод надписи score
        scr.blit(text_num_score, (700, 20))  # вывод счёта последней игры
        scr.blit(text, (1100 / 2, 100))  # прорисовка текста о победе или поражении
        scr.blit(text_restart, (1100 / 2, 650))  # прорисовка надписи о рестарте
        scr.blit(best, (1100 / 2, 200))  # прорисовка надписи лучшие

        for i in range(5):  # прорисовка таблицы рекордов
            scr.blit(top_nik_text[i], (500, 300 + 50 * i))
            scr.blit(top_score_text[i], (800, 300 + 50 * i))
        pg.display.flip()  # обновение экрана

    if game_score > 0:  # если счётчик больше 0
        game_score = game_score - 1  # уменьшение счётчика

    cout = f.render(str(game_score), False, (0, 0, 0))
    scr.blit(cout, (1100 / 2, 0))

    all.update()  # вызов функции движения игрока
    pg.display.flip()  # обновление экрана
    clock.tick(FPS)  # задержка
