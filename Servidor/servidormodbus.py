from pyModbusTCP.server import DataBank, ModbusServer
from time import sleep
import random


class ServidorMODBUS():
    """
    Classe Servidor MODBUS
    """
    def __init__(self, host_ip,port):
        """
        Construtor
        """
        self._server =  ModbusServer(host=host_ip, port=port, no_block=True)
        self._db = DataBank
    
    def run(self):
        """
         Execução do servidor
        """
        self._server.start()
        setpoint = self._db.set_words(2000,[25,])
        print("Servidor em execução")
        while True:
            if self._db.get_bits(1000)[0]:
                setpoint = self._db.get_words(2000)[0]
            self._db.set_words(1000,[random.randrange(int(0.95*setpoint),int(1.05*setpoint))])
            print('=====================')
            print(f'Tabela MODBUS')
            print(f'Holding Registers\r\n R1000: {self._db.get_words(1000)}\r\n R2000: {self._db.get_words(2000)}')
            print(f'Coils \r\n R1000: {self._db.get_bits(1000)}')
            print('=====================')
            sleep(1)
            
        



