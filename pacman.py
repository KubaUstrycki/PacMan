from random import choice
from turtle import *
from freegames import floor, vector

state = {"score": 0}      #  wynik
path = Turtle(visible=False)     # zółw rysujący grafikę
writer = Turtle(visible=False)   # żółw rysujący aktualny wynik
aim = vector(0, 0) # w którą strone ma iść pacman
pacman = vector(-40, -0) # położenie startowe pacmana
ghosts = [  # duszki ::::: w którą strone ma iść ,, położenie startowe
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

print(pacman)
print(pacman+19)

Mapa = [ # 0 - czarne pola   1 - niebieski/"path"
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

#rysuje kwadracik 20x20
def square(x, y):
    path.up() # podniesienie ołówka
    path.goto(x, y) # ustawienie ołówka
    path.down() # opuszcza ołówek

    path.begin_fill() # oznacza początek rosowania figury, która będzie wypełniana.


    for count in range(4):  # liczy do 4
        path.forward(20) # rysuje linię 20px 
        path.left(90) # żółw obraca się w lewo o 90 stopni

    path.end_fill() # koniec rysowania figury wypełnianej


#  jako że rysowanie jest zepsute to to naprawia
def offset(point):
    x = (floor(point.x, 20) + 200) / 20 # przemieszcza w osi X
    y = (180 - floor(point.y, 20)) / 20 # przemieszcza w osi Y
    index = int(x + y * 20) # <-ilość pól   <------to ta wartość na mapie
    return index #zwraca 

#  sprawdzanie czy można po tym chodzić
def valid(point):
    index = offset(point)   # oblicza index tablicy z mapą 

    if Mapa[index] == 0:    #Sprawdza czy można po tym chodzić
        return False        # :( nie można

    index = offset(point + 19)  # sprawdza, czy dolny prawy punkt duszka/pacmana mieści się w polu

    if Mapa[index] == 0:
        return False            #znowu się nie da :(

    return point.x % 20 == 0 or point.y % 20 == 0   # sprawdza, czy obiekt znajduje się na siatce 20x20


# rysowanie mapy
def world():
    bgcolor("black")    #kolor czarny dla wszystkiego innego 
    path.color("blue")  #kolor niebieski dla drogi po której można chodzić

    for index in range(len(Mapa)): # przechodzi po każdej z pól na mapie
        tile = Mapa[index] #i podpisuje pod siebie

        if tile > 0: #jeśli pole na mapie jest większe od 0 to zmienia
            x = (index % 20) * 20 - 200 # odkrycie pól x
            y = 180 - (index // 20) * 20 # odkrycie pól y
            square(x, y) #rysowanie x,y

            if tile == 1: # jeśli pole na mapie = 1 to rysuje kropki białe
                path.up() # zółw podnosi ołówek.
                path.goto(x + 10, y + 10)  # przechodzi zółwik do środka pola
                path.dot(3, "white") #rysuje białą 2pikselową kropke


# ruch
def move():
    writer.undo()   # cofa ostatni rysunek żółwia piszącego (wynik)
    writer.write(state["score"]) #rysuje wynik
    clear() #usuwa wszystkie nie wcześniejsze linie

    if valid(pacman + aim):
        pacman.move(aim) 

    index = offset(pacman) # oblicza numer z tablicy mapy

    if Mapa[index] == 1:              # jeżeli pacman jest po raz pierwszy na polu, to...
        Mapa[index] = 2           
        state["score"] += 1           # zwiększ wynik
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)                  # i skasuj kropeczkę

    up()                              # żółw podnosi żółtą kredkę
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, "yellow")

    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)

            # while not valid(point+plan): # optymalizacja ruchu 
            #     plan = choice(options)

            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, "red")

    update()           # ?
    for point, course in ghosts:     
        if abs(pacman - point) < 20: #sprawdza czy duszek dotknął pacmana
            return

    ontimer(move, 20)   


# zmiana Ruch pm
def change(x, y):
    if valid(pacman + vector(x, y)): # jeżeli wykonywany ruch jest "valid", to 
        aim.x = x   # zmień właściwość X wektora ruchu
        aim.y = y   # zmień właściwość Y wektora ruchu

print("="*20,"START GRY","="*20)

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color("white")
writer.write(state["score"])
listen() # uruchamia odczytywanie klawiszy
onkey(lambda: change(5, 0), "Right")
onkey(lambda: change(-5, 0), "Left")
onkey(lambda: change(0, 5), "Up")
onkey(lambda: change(0, -5), "Down")
world() #rysuje mapę
move() 
done()