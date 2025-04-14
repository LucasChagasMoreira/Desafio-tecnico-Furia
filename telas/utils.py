from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
def show_popup(message):
    """Função auxiliar que cria e exibe um Popup com título e mensagem."""
    conteudo_vazio = Widget(size_hint=(None, None), size=(0,0))

    popup = Popup(
        title=message,
        content=conteudo_vazio,
        size_hint=(None, None),
        size=(300, 100)
    )

    popup.open()

