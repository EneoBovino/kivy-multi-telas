from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

class TelaPrincipal(BoxLayout):
    pass

class TelaGarcom(BoxLayout):
    pass

# Builder.load_file('restaurante_float.kv')
# Builder.load_file('restaurante_grid.kv')
Builder.load_file('restaurante_box.kv')

class RestauranteApp(App):
    def build(self):
        return TelaGarcom()
    
if __name__ == "__main__":
    RestauranteApp().run()