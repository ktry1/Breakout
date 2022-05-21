import random

import dearpygui.dearpygui as dpg
def change_color(r,g,b,item_label):
    with dpg.theme() as item_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (r, g, b), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (r, g, b), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (r, g, b), category=dpg.mvThemeCat_Core)
    dpg.bind_item_theme(item=item_label, theme=item_theme)



def spawn_ball():
    dpg.add_button(label="", width=10, height=10, tag=f"ball", pos=[random.randint(100,700), 400], parent="Playfield")
    change_color(r=255, g=255, b=255, item_label=f"ball")