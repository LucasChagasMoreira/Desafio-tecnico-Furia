from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from telas.utils import show_popup, CACHE_PATH
from kivy.metrics import dp
import json
import requests


class TelaCadastro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "cadastro"

        # Layout principal
        layout = BoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(20), dp(20), dp(20)],
            spacing=dp(20)
        )

        # Título da tela
        titulo = Label(
            text="Cadastro",
            font_size="32sp",
            size_hint=(1, 0.2),
            halign="center",
            valign="middle"
        )
        # Atualiza o text_size do título
        titulo.bind(size=lambda instance, value: setattr(instance, 'text_size', instance.size))
        
        # nome do usuário
        self.nome = TextInput(
            hint_text="Digite seu nome aqui",
            size_hint=(1, None),
            height=dp(50),
            font_size="20sp",
            multiline=False
        )
        
        # Texto para o e-mail
        self.email = TextInput(
            hint_text="Digite seu email aqui",
            size_hint=(1, None),
            height=dp(50),
            font_size="20sp",
            multiline=False
        )
        
        # Botão para confirmar o cadastro
        confirmar = Button(
            text="Cadastrar",
            size_hint=(1, None),
            height=dp(50),
            font_size="20sp",
            background_color=(0.2, 0.6, 0.8, 1)
        )
        confirmar.bind(on_press=self.cadastrar)
        
        # Adicionando os widgets
        layout.add_widget(titulo)
        layout.add_widget(self.nome)
        layout.add_widget(self.email)
        layout.add_widget(confirmar)
        
        # Adiciona o layout principal a tela
        self.add_widget(layout)

    def cadastrar(self, instance):
        # Verifica se todos os campos foram preenchidos
        if self.nome.text and self.email.text:

            data = {
                "Nome": self.nome.text,
                "Email": self.email.text                
            }

            url = "http://localhost:5000/api/usuario"

            try:
                # requisição POST com os dados
                response = requests.post(url, json=data)
                if response.status_code == 201:
                    show_popup("Dados salvos com sucesso!")
                    print("Dados salvos com sucesso!")
                    
                    try:
                        with open(CACHE_PATH, "w", encoding="utf-8") as cache_file:
                            json.dump(data, cache_file)
                        print("Cache salvo com sucesso!")
                    except Exception as cache_error:
                        print("Erro ao salvar o cache:", cache_error)
                        
                    self.nome.text = ""
                    self.email.text = ""
                    
                    #retorna a aba de login
                    self.manager.current = "login"
                    return 0
                else:
                    show_popup("Erro ao salvar os dados: " + str(response.status_code))
                    print("Erro ao salvar os dados: ", response.status_code)
                    return 2
            except Exception as e:
                show_popup("Erro ao conectar com o servidor!")
                print("Erro ao conectar com o servidor: ", e)
                return 3
        else:
            show_popup("Por favor, preencha todos os campos.")
            print("Por favor, preencha todos os campos.")
            return 2
    
    #função para a trocar para tela inicial
    def ir_para_inicial(self, instance):
        self.manager.current = "login"