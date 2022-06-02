from ctypes.wintypes import tagSIZE
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder
from pyModbusTCP.client import ModbusClient
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock

from datacards import CardInputRegister, CardHoldingRegister, CardCoil

class MyWidget(MDScreen):
    def __init__(self,tags, **kw):
        super().__init__(**kw)
        self._tags = tags
        self._modclient = ModbusClient()

        for i in range(1):
            for tag in self._tags:
                if tag["type"] == "input":
                    self.ids.modbus_data.add_widget(CardInputRegister(tag, self._modclient))
                elif tag["type"] == "holding":
                    self.ids.modbus_data.add_widget(CardHoldingRegister(tag, self._modclient))
                elif tag["type"] == "coil":
                    self.ids.modbus_data.add_widget(CardCoil(tag, self._modclient))

    def connect(self):
        if self.ids.bt_con.text == "CONECTAR":
            try:
                self._modclient.host = self.ids.hostname.text
                self._modclient.port = int(self.ids.port.text)
                self._modclient.open()
                if(self._modclient.is_open()):
                    Snackbar(text="Conexão realizada com sucesso", bg_color=(0,1,0,1)).open()
                    self.ids.bt_con.text = "DESCONECTAR"
                self._ev = []
                for card in self.ids.modbus_data.children:
                    print("For de child")
                    if card.tag['type'] == "holding" or card.tag['type'] == "coil":
                        print(card.tag['type'])
                        self._ev.append(Clock.schedule_once(card.update_data))
                    else:
                        self._ev.append(Clock.schedule_interval(card.update_data,1)) #Atualiza valor a cada 1 segundo
            except Exception as e:
                print(f"Erro ao realizar a conexão com o servidor", e.args)
                Snackbar(text="Falha na conexão", bg_color=(1,0,0,1)).open()
        else:
            self.ids.bt_con.text = "CONECTAR"
            for event in self._ev:
                event.cancel()
            self._modclient.close()
            Snackbar(text="Cliente desconectado", bg_color=(1,0,0,1)).open()

class BasicApp(MDApp):
    __tags = [
        {'name':'tempForno','description':'Temperatura Forno','unit':'ºC','address':1000,'type':"input"},
        {'name':'setpoint','description':'Temperatura desejada','unit':'ºC','address':2000,'type':"holding"},
        {'name':'status','description':'Estado atuador','address':1000,'type':"coil"}
    ]

    def build(self):
        self.theme_cls.primary_palette = "LightGreen"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.accent_palette = "LightGreen"
        return MyWidget(self.__tags)

Builder.load_file('main.kv')

if __name__ == '__main__':
    BasicApp().run()