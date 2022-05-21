import random
import threading
import dearpygui.demo as demo
from math import sin,cos
from time import sleep
from functions import change_color,spawn_ball
import dearpygui.dearpygui as dpg


dpg.create_context()
dpg.create_viewport(title='Breakout',small_icon="Misc/favicon.ico", width=830, height=800)
dpg.set_viewport_resizable(False)

#Variables
stage = 1
balls = 5
score = 0
with open("Misc/High_Score.txt") as file:
    high_score = int(file.read())



with dpg.font_registry():
    font = dpg.add_font("Misc/ARCADECLASSIC.TTF", 75)

def update_score():
    while True:
        dpg.hide_item("score_label")
        dpg.configure_item(item="score_label", default_value=str(score))
        sleep(0.3)
        dpg.show_item("score_label")
        sleep(0.3)

def move_paddle():
    while True:
        dpg.set_item_pos(item="paddle", pos=[dpg.get_mouse_pos()[0]-20, 720])



def spawn_rows():
    global item_coordinates,items
    item_coordinates=[]
    items = []
    x = 10
    y = 100
    labels = ["wall-red-h","wall-red-l","wall-orange-h","wall-orange-l","wall-green-h","wall-green-l","wall-yellow-h","wall-yellow-l"]
    colors = [[119,21,21],[119,21,21],[255,165,0],[255,165,0],[0,255,0],[0,255,0],[255,255,0],[255,255,0]]
    for row in range(8):
        for i in range(14):
            dpg.add_button(label="", width=800 / 14 - 5, height=10, tag=f"{labels[row]}{i}", callback=None, pos=[x, y])
            change_color(r=colors[row][0], g=colors[row][1], b=colors[row][2], item_label=f"{labels[row]}{i}")
            x += 800 / 14
            item_coordinates.append([x,y])
            items.append(f"{labels[row]}{i}")
        x = 10
        y +=15

with dpg.window(tag="Playfield",no_scrollbar=True,max_size=[830,800]):

    dpg.bind_font(font)
    stage = dpg.add_text(default_value=str(stage), pos=[80, -10])
    score_label = dpg.add_text(tag ="score_label",default_value=str(score), pos=[120,30])
    balls_left = dpg.add_text(default_value=str(balls), pos=[600, -10])
    high_score_label = dpg.add_text(default_value=str(high_score), pos=[640, 30])
    spawn_rows()
    spawn_ball()

    dpg.draw_line((-2, -5), (-2, 800), color=(128,128,128), thickness=6)
    dpg.draw_line((-5, -5), (820, -5), color=(128,128,128), thickness=6)
    dpg.draw_line((800, -5), (800, 800), color=(128,128,128), thickness=6)

    dpg.add_button(label="",width=40,height=20,tag="paddle",callback=None)
    dpg.set_item_pos("paddle",[400,720])

change_color(r=80,g=133,b=188,item_label="paddle")



def move_ball():
    global score,balls,high_score
    game_over = False
    speed = 3
    coordinates = dpg.get_item_pos("ball")
    directions = [1,-1]
    Vx = random.choice(directions)
    Vy = 1
    del  directions
    phaze = False
    sleep(1)
    while not game_over:
        sleep(0.01)

        for i in range(speed):
            coordinates = dpg.get_item_pos("ball")
            paddle_coordinates = dpg.get_item_pos("paddle")
            if not phaze == True:
                for _ in range(len(item_coordinates)):
                        if item_coordinates[_][0]-57.14<=coordinates[0]<=item_coordinates[_][0] and item_coordinates[_][1]<=coordinates[1]<=item_coordinates[_][1]+5  :
                            if "yellow" in items[_]:
                                score +=1
                            elif "green" in items[_]:
                                score += 3
                            elif "orange" in items[_]:
                                score +=5
                            elif"red" in items[_]:
                                score +=7
                            dpg.delete_item(item=items[_])
                            phaze = True
                            if not speed==15:
                                speed +=1

                            dpg.set_item_pos(item="ball", pos=[coordinates[0] - Vx, coordinates[1] - Vy])
                            Vy = -Vy


                            del item_coordinates[_]
                            del items[_]
                            break

            if paddle_coordinates[1] - coordinates[1] <= 10 and (
                    paddle_coordinates[0]-10 <= coordinates[0] <= paddle_coordinates[0] + 40):
                dpg.set_item_pos(item="ball", pos=[coordinates[0], paddle_coordinates[1]-10])
                coordinates = dpg.get_item_pos("ball")
                Vy = -Vy
                phaze = False

            elif coordinates[0] >= 800:

                dpg.set_item_pos(item="ball", pos=[coordinates[0] - Vx, coordinates[1]-Vy])
                coordinates = dpg.get_item_pos("ball")
                Vx = -Vx
                phaze = False
            elif coordinates[0] <= 0:

                dpg.set_item_pos(item="ball", pos=[coordinates[0] - Vx, coordinates[1]-Vy])
                coordinates = dpg.get_item_pos("ball")
                Vx = - Vx
                phaze = False
            elif coordinates[1] >= 750:
                phaze = False
                dpg.set_item_pos(item="ball", pos=[random.randint(100,700), 400])
                directions = [1, -1]
                Vx = random.choice(directions)
                del directions
                coordinates = dpg.get_item_pos("ball")
                balls-=1
                if balls ==0:
                    dpg.configure_item(item=balls_left, default_value=str(balls))

                    dpg.delete_item("ball")
                    game_over = True
                    print(score)
                    print(high_score)
                    if high_score < score:
                        with open("Misc/High_Score.txt",mode="w") as file:
                            file.write(str(score))
                        dpg.add_text(default_value='GAME OVER', pos=[250, 300], tag="game_over", parent="Playfield")
                        dpg.add_text(default_value='NEW RECORD', pos=[240, 380], tag="game_over", parent="Playfield")
                        dpg.configure_item(item=high_score_label, default_value=score)
                    else:
                        dpg.add_text(default_value='GAME OVER', pos=[250, 300], tag="game_over", parent="Playfield")
                    break
                else:

                    dpg.configure_item(item=balls_left, default_value=str(balls))

                    sleep(1)
                    speed = 3



            elif coordinates[1] <= 10:

                dpg.set_item_pos(item="ball", pos=[coordinates[0] - Vx, coordinates[1]-Vy])
                coordinates = dpg.get_item_pos("ball")
                Vy = -Vy
                phaze = False

            dpg.set_item_pos(item="ball",pos=[coordinates[0]+Vx,coordinates[1] + Vy])






dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_primary_window(window="Playfield", value=True)
#Thread declaration
paddle_thread = threading.Thread(name="move paddle", target=move_paddle,args=())
ball_thread = threading.Thread(name="move ball", target=move_ball, args=())
score_thread = threading.Thread(name="update score", target=update_score, args=())
paddle_thread.start()
ball_thread.start()
score_thread.start()


dpg.start_dearpygui()
dpg.destroy_context()