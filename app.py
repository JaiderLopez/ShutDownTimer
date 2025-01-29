# import flet as ft
from flet import app, Page, Container, Row, Column
from flet import Text, Button
from flet import Icon, Icons, Theme
from flet import border, border_radius, alignment, MainAxisAlignment, CrossAxisAlignment
import time
import os
import sys

class Controls(Container):
   def __init__(self, num_control, funtion, icon):
      super().__init__(expand= True, expand_loose= True)
      self.content = Icon(name= icon, size= 16)
      self.funtion = funtion
      self.num_control = num_control
      self.width = 50
      self.height = 20
      self.bgcolor = "black" 
      self.border_radius = border_radius.only(top_left= 5, top_right= 5)
      
      self.on_click = self.add_or_remove
   
   def add_or_remove(self, e):
      self.num_control.update_num(self.num_control.texto + self.funtion)
      self.page.update()

class Boton(Container):
   def __init__(self, texto: int):
      super().__init__()
      self.texto = texto
      self.width = 50
      self.height = 50
      # self.bgcolor = "#ffffff"      
      self.bgcolor = "#000000"      
      self.alignment= alignment.center
      # self.border_radius = 10
      self.border = border.all(1, 'black')
      self.update_num(self.texto)
      
   def update_num(self, numero):
      self.texto = numero
      if self.texto != ':':
         self.texto %= 60

         if self.texto < 10:
            self.content = Text(f"0{self.texto}", size= 36, color= '#ff9500')
         else:
            self.content = Text(self.texto, size= 36, color= '#ff9500')
      else:
         self.content = Text(self.texto, size= 36, color= '#ff9500')


class App(Container):
# ---------------------------------------- CONTROLES ----------------------------------------
   def __init__(self, page):
      super().__init__(expand= True)
      self.page = page

      self.hours = 0
      self.minutes = 0
      self.seconds = 0
      self.pause = True
      
      # TIMER CONTAINERS
      self.hour_num = Boton(self.hours)
      self.minute_num = Boton(self.minutes)
      self.second_num = Boton(self.seconds)
      
      # TIMER BUTTONS
      self.btn_pause = Button('Pause', on_click= self.pause_or_continue, visible= False)
      self.btn_sleep = Button('Sleep', on_click= self.timer, data= 'sleep', disabled= False)
      self.btn_power = Button('Power', on_click= self.timer, data= 'power', disabled= False)
      
      # CONTROLS BUTTONS
      self.contrlos_up = []
      self.contrlos_down = []
      for timer in [self.hour_num, self.minute_num, self.second_num]:
         self.contrlos_up.append(Controls(timer, 1, Icons.ARROW_DROP_UP))
         self.contrlos_down.append(Controls(timer, -1, Icons.ARROW_DROP_DOWN))

      # CONTROLS VIEW
      self.controls_list = Container(content= Row(
         spacing= 0,
         controls=[
            Column(controls=[
               self.contrlos_up[0],
               self.hour_num,
               self.contrlos_down[0],
            ], spacing= 0, alignment= MainAxisAlignment.CENTER, width= 50),
            Boton(':',),
            Column(controls=[
               self.contrlos_up[1],
               self.minute_num, 
               self.contrlos_down[1],
            ], spacing= 0, alignment= MainAxisAlignment.CENTER, width= 50),
            Boton(':'),
            Column(controls=[
               self.contrlos_up[2],
               self.second_num, 
               self.contrlos_down[2],
            ], spacing= 0, alignment= MainAxisAlignment.CENTER, width= 50),
            self.btn_pause,
            self.btn_sleep,
            self.btn_power,
         ]
         ),
      # gradient= LinearGradient(colors= [self.list_colors['rosa'],self.list_colors['azul'],]),
      bgcolor= 'black',
      expand= True,
      height= 120,
      alignment= alignment.center, 
      border_radius= 10,
      )

# ---------------------------------------- VENTANA ---------------------------------------- 
   def build(self):
      self.page.window_maximizable = False
      self.page.window_resizable = False
      self.page.window.width = 400
      self.page.window.height = 155
      self.page.window.max_width = 400
      self.page.window.max_height = 155
      self.page.window.min_width = 400
      self.page.window.min_height = 155
      self.page.theme_mode = 'dark'
      self.page.fonts = {
         'digit' : self.resource_path("assets/DS-DIGI.TTF")
      }
      self.page.theme = Theme(font_family= 'digit')
      self.page.padding = 0
      self.page.add(Column(
         controls= [
            self.controls_list
         ],
      ))
 
# ---------------------------------------- FUNCIONES ----------------------------------------
   def resource_path(self, relative_path):
      if hasattr(sys, "_MEIPASS"):
         return os.path.join(sys._MEIPASS, relative_path)
      return os.path.abspath(relative_path)
   
   def change(self,):
      self.pause = not self.pause
      self.btn_pause.visible = not self.btn_pause.visible
      self.btn_sleep.visible = not self.btn_sleep.visible
      self.btn_power.visible = not self.btn_power.visible
      for i in range(3):
         self.contrlos_up[i].disabled = not self.contrlos_up[i].disabled
         self.contrlos_down[i].disabled = not self.contrlos_down[i].disabled

   def pause_or_continue(self, e):
      if self.btn_pause.text == "Continue":
         self.btn_pause.text = "Pause"
      self.change()
      self.page.update()

   def clock(self):
      horas = self.hour_num.texto 
      minutos = self.minute_num.texto
      segundos = self.second_num.texto
      while horas > 0 or minutos > 0 or segundos > 0:
         if self.pause:
            break
         # print(f"{horas:02}:{minutos:02}:{segundos:02}")
         time.sleep(1)
         if segundos > 0:
            segundos -= 1
            self.second_num.update_num(segundos)
         elif minutos > 0:
            minutos -= 1
            segundos = 59
            self.second_num.update_num(segundos)
            self.minute_num.update_num(minutos)
         elif horas > 0:
            horas -= 1
            minutos = 59
            segundos = 59
            self.second_num.update_num(segundos)
            self.minute_num.update_num(minutos)
            self.hour_num.update_num(horas)
         self.page.update()

   def timer(self, e):
      control = e.control.data
      self.change()
      self.clock()

      if not self.pause:
         if control == 'sleep':
            self.btn_pause.text = "Continue"
            self.page.update()
            time.sleep(1)
            os.system("shutdown /h")
            # print("Sleeping")
         elif control == 'power':
            os.system("shutdown /s")
            # print("Power out")
 
def main(page: Page):
   app = App(page)
   app.build()
 
if __name__ == '__main__':
   app(target = main, assets_dir= 'assets')

