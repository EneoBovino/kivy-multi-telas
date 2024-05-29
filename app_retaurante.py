from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

# Para realizar as chamadas na API REST
import requests

# Para gerenciar o tamanho da janela
from kivy.config import Config

Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '500')

# Popup para exibir mensagem de erro de autenticação
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

# Implementação do popup de erro através do script python principal
# class PopupErro(Popup):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.title = 'Erro de autenticação'
#         self.size_hint = (0.7, 0.4)
#         self.auto_dismiss = False

#         self.box = BoxLayout(orientation='vertical')
#         self.box.add_widget(
#             Label(
#                 text="Usuário ou senha inválidos!",
#             )
#         )

#         self.box.add_widget(
#             Button(
#                 text="Fechar",
#                 on_press=self.dismiss
#             )
#         )

#         self.add_widget(self.box)

# Implementação do popup de erro usando o arquivo kv
class PopupErro(Popup):
    pass
class TelaLogin(Screen):
        
    def autenticar(self):
        usuario = self.ids.txt_usuario.text
        senha = self.ids.txt_senha.text
               
        url = 'https://2181-168-232-136-83.ngrok-free.app/restaurante/autenticar'
        # url = 'http://localhost:5500/restaurante/autenticar'
        dados = {'usuario': usuario, 'senha': senha}
        resposta = requests.post(url, json=dados)
        if resposta.status_code == 200:
            self.manager.current = 'tela_principal'
        else:
            popup_erro = PopupErro()
            popup_erro.open()
            # PopupErro().open()

class TelaPrincipal(Screen):
    pass

class TelaGarcom(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        import sqlite3
        # Consulta ao banco de dados para obter o cardapio
        conn = sqlite3.connect('cardapio.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cardapio')
        self.cardapio = cursor.fetchall()
        conn.close()
        self.cardapio_itens = [item[1] for item in self.cardapio if item[5] == 'Bar']
        ##########
        self.mesas = [str(i) for i in range(1, 11)]
        self.pedido_mesa = {"mesa": "", "cozinha": [], "bar": [], "status": "pendente"}
        self.mesa_id = ""
    
    def atualiza_lista_cardapio(self):
        if self.ids.radio_bar.active:
            self.ids.itens_cardapio.values = [item[1] for item in self.cardapio if item[5].lower() == 'bar']
        elif self.ids.radio_cozinha.active:
            self.ids.itens_cardapio.values = [item[1] for item in self.cardapio if item[5].lower() == 'cozinha']

        self.ids.itens_cardapio.text = "Selecione"





    def decrementa_qtd_item(self):
        if int(self.ids.qtd_item.text) > 0:
            self.ids.qtd_item.text = str(int(self.ids.qtd_item.text) - 1)

    def incrementa_qtd_item(self):
        self.ids.qtd_item.text = str(int(self.ids.qtd_item.text) + 1)

 
    def inclui_pedido_na_lista(self):
        if self.ids.mesa_id.text == "Mesa":
            return
        qtd = self.ids.qtd_item.text
        pedido = self.ids.itens_cardapio.text
        if pedido == "Selecione":
            return
        if qtd == "0":
            return
        if self.ids.bar.active:
            self.pedido_mesa["bar"].append(f"{qtd} - {pedido}")
        elif self.ids.cozinha.active:
            self.pedido_mesa["cozinha"].append(f"{qtd} - {pedido}")
        self.ids.lista_itens.text += f"\n{qtd} - {pedido}"
        self.ids.qtd_item.text = "0"
        self.ids.itens_cardapio.text = "Selecione"
        print(self.pedido_mesa)

    def enviar_pedido(self):
        url = 'http://localhost:5500/restaurante/criar_pedido'
        self.pedido_mesa["mesa"] = self.ids.mesa_id.text
        resposta = requests.post(url, json=self.pedido_mesa)
        if resposta.status_code == 201:
            popup = PopupErro()
            popup.title = "Pedido enviado"
            popup.ids.lbl_popup.text = "Pedido enviado com sucesso!"
            popup.open()


class TelaCozinha(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grade = GridLayout(cols=2, spacing=10, size_hint=(1, 1)) 
        for i in range(1, 11):
            mesa = "mesa_" + str(i)
            btn = Button(text=mesa)
            self.grade.add_widget(btn)
            self.ids[mesa] = btn
        self.add_widget(self.grade)
    
    
    def on_enter(self):
        url = 'http://localhost:5500/restaurante/listar_pedidos'
        resposta = requests.get(url)
        pedidos = resposta.json()
        for pedido in pedidos:
            mesa = "mesa_" + str(pedido['mesa'])
            self.ids[mesa].color = (1, 0, 0, 1)
                
class GerenciadorTelas(ScreenManager):
    pass

# Builder.load_file('restaurante_float.kv')
# Builder.load_file('restaurante_grid.kv')
kv = Builder.load_file('restaurante_mixed_layout.kv')

class RestauranteApp(App):
    def build(self):
        return kv
    
if __name__ == "__main__":
    RestauranteApp().run()