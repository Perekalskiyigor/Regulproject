import time
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
import threading




#######################################Class Mudbus##########################################
class ModbusProvider:
    def __init__(self):
        # Инициализация хранилища данных
        self.store = ModbusSlaveContext(
            hr=ModbusSequentialDataBlock(0, [0] * 100)  # 100 регистров, инициализированных значением 0
        )
        # то что я принимаю
        self.Table11free = 0 # Стол один ложе 1 свободно
        self.RobotTake11 = 0 # Взял плату 11
        self.Table12free = 0 # Стол один ложе 2 свободно
        # То что я отдаю в питон
        self.outTable11free = 0 # Стол один ложе 1 освободи
        self.outRobotTake11 = 0 # Возьми плату 11
        self.outTable12free = 0 # Стол один ложе 2 освободи

        # Запуск Modbus TCP сервера в отдельном потоке
        self.server_thread = threading.Thread(target=self.run_modbus_server, daemon=True)
        self.server_thread.start()

        # Запуск потока для обновления регистров
        self.update_thread = threading.Thread(target=self.update_registers, daemon=True)
        self.update_thread.start()

    def run_modbus_server(self):
        """Запуск Modbus TCP сервера."""
        context = ModbusServerContext(slaves=self.store, single=True)
        print("Starting Modbus TCP server on localhost:502")
        StartTcpServer(context, address=("192.168.1.108", 502))

    def update_registers(self):
        """Обновление значений регистров."""
        while True:
            # Чтение значений из регистров 0 и 1 (input1 и input2)
            self.Table11free = self.store.getValues(3, 0, count=1)[0]  # 3 - код функции для holding registers
            self.RobotTake11 = self.store.getValues(3, 1, count=1)[0]
            self.Table12free = self.store.getValues(3, 2, count=1)[0]

            # Запись значений в регистры 2 и 3 (output1 и output2)
            self.store.setValues(3, 31, [self.outTable11free])
            self.store.setValues(3, 32, [self.outRobotTake11])
            self.store.setValues(3, 33, [self.outTable12free])

            time.sleep(1)

    def get_inTable11free(self):
        """Получение данных из регистров."""
        return self.Table11free
    

    def set_outTable11free(self, outTable11free):
        """Установка данных в регистры."""
        self.outTable11free = outTable11free
        print(f"Modbus - Сдвинь плату освободив ложе1. {self.outTable11free}")

    
    def get_inRobotTake11(self):
        """Получение данных из регистров."""
        return self.RobotTake11
    
    def set_outRobotTake11(self, outRobotTake11):
        """Установка данных в регистры."""
        self.outRobotTake11 = outRobotTake11
        print(f"Modbus - Робот забери плату 1. {self.outRobotTake11}")

    def get_inTable12free(self):
        """Получение данных из регистров."""
        return self.Table12free
    

    def set_outTable12free(self, outTable12free):
        """Установка данных в регистры."""
        self.outTable12free = outTable12free
        print(f"Modbus - Сдвинь плату освободив ложе1. {self.outTable12free}")


#############################################################################################

class Table:
    def __init__(self):
        self.lodge1 = None
        self.lodge2 = None

    def pause(self):
        time.sleep(2)


    def robot_take_board_from_lodge1(self):
        print("Робот <- Забери плату с ложе 1.")
        self.pause()
        return "Робот -> Плату забрал."

    def robot_take_board_from_lodge2(self):
        print("Робот <- Забери плату с ложе 2.")
        self.pause()
        return "Робот -> Плату забрал."

    def robot_place_board_on_lodge1(self):
        print("Робот <- Положи плату ложе 1.")
        self.pause()
        self.lodge1 = "Плата 1"
        return "Робот -> Плату положил."

    def robot_place_board_on_lodge2(self):
        print("Робот <- Положи плату ложе 2.")
        self.pause()
        self.lodge2 = "Плата 2"
        return "Робот -> Плату положил."

    def regul_move_board_right(self):
        print("Регул <- Сдвинь плату вправо.")
        self.pause()
        return "Регул -> Сдвинул."

    def regul_move_board_to_free_lodge1(self):
        print("Регул <- Сдвинь плату освободив ложе1.")
        self.pause()
        self.lodge1 = None
        return "Регул -> Сдвинул."

    def regul_move_board_to_free_lodge2(self):
        print("Регул <- Сдвинь плату освободив ложе2.")
        self.pause()
        self.lodge2 = None
        return "Регул -> Сдвинул."


    def regul_lower_soldering_iron(self):
        print("Регул <- Опусти прошивальщик на ложе")
        self.pause()
        return "Регул -> Опустил."

    def regul_raise_soldering_iron(self):
        print("Регул <- Подними прошивальщик.")
        self.pause()
        return "Регул -> Поднял."

    def server_start_stitching(self):
        print("Сервер <- Начни шить.")
        self.pause()
        return "Сервер -> Ответ по прошивке (хорошо/плохо)."
    
    def make_photo_from_CAM(self):
        print("Камера <- Сделай фото штрихкода платы")
        self.pause()
        return "Камера -> Фото получено"

    # Метод для первого цикла
    def first_cycle(self):
        print("****ЦИКЛ SETUP******")
        result = self.robot_place_board_on_lodge1()
        print(result)
        result = self.regul_move_board_to_free_lodge2()
        print(result)
        result = self.make_photo_from_CAM()
        print(result)
        result = self.robot_place_board_on_lodge2()
        print(result)
        print("Стол 1ложе занято")
        print("Стол 2ложе занято")
        print("Регул -> Ничего не делай.")
        #"Регул <- Опусти прошивальщик ложе 1."
        result = self.regul_lower_soldering_iron()
        print(result)
        # "РСервер <- Начни шить. ложе 1"
        result = self.server_start_stitching()
        print(result)
        # "Регул <- Подними прошивальщик. ложе 1"
        result = self.regul_raise_soldering_iron()
        print(result)
        self.pause()
        print("****ЦИКЛ SETUP Завершен******")

    # Метод для защиты что нет плат
    def defence_cycle(self):
        print("******ЦИКЛ DEFENCE*******")
        
        # 1 Регул <- Сдвинь плату освободив ложе1.
        result = self.regul_move_board_to_free_lodge1()
        print(result)
        # Связь по мадбас с регулом
        modbus_provider.set_outTable11free(1)
        i = modbus_provider.get_inTable11free()
        while True:
            i = modbus_provider.get_inTable11free()
            if i!=1:
                print("Ожидаем ответа от мадбас стол сдвинут 1 ложе свободно")
                time.sleep(1)
            else:
                modbus_provider.set_outTable11free(0)
                break
        
        # 2. Робот <- Забери плату с ложе 1.
        result = self.robot_take_board_from_lodge1()
        modbus_provider.set_outRobotTake11(1)
        i = modbus_provider.get_inRobotTake11()
        while True:
            i = modbus_provider.get_inRobotTake11()
            if i!=1:
                print("Ожидаем ответа от робота, что он взялл первую плату с ложе 1")
                time.sleep(1)
            else:
                modbus_provider.set_outRobotTake11(0)
                break

        # 3 Регул <- Сдвинь плату освободив ложе2.
        result = self.regul_move_board_to_free_lodge2()
        print(result)
        # Связь по мадбас с регулом
        modbus_provider.set_outTable12free(1)
        i = modbus_provider.get_inTable12free()
        while True:
            i = modbus_provider.get_inTable12free()
            if i!=1:
                print("Ожидаем ответа от мадбас стол сдвинут 2 ложе свободно")
                time.sleep(1)
            else:
                modbus_provider.set_outTable12free(0)
                break

        # 4. Робот <- Забери плату с ложе 2.
        result = self.robot_take_board_from_lodge2()
        modbus_provider.set_outRobotTake11(1)
        i = modbus_provider.get_inRobotTake11()
        while True:
            i = modbus_provider.get_inRobotTake11()
            if i!=1:
                print("Ожидаем ответа от робота, что он взялл вторую плату с ложе 2")
                time.sleep(1)
            else:
                modbus_provider.set_outRobotTake11(0)
                break
        print("******ЦИКЛ DEFENCE Завершен*******")

    # Метод для основного цикла
    def main_cycle(self):
        while True:
            if self.lodge1 is None and self.lodge2 is None:
                self.lodge1 = "Плата 1"
                self.lodge2 = "Плата 2"
                self.pause()
            ####################### 2 операция на столе
            # Регул <- Сдвинь плату освободив ложе1.
            result = self.regul_move_board_to_free_lodge1()
            print(result)
            # 4. Робот <- Забери плату с ложе 1.
            result = self.robot_take_board_from_lodge1()
            print(result)
            print("Стол 1ложе свободен.")
            # Робот <- Положи плату ложе 1.
            result = self.robot_place_board_on_lodge1()
            print(result)
            # Фоткаем плату перед тем как пместить на ложе
            result = self.make_photo_from_CAM()
            print(result)
            print("Стол 1ложе занято.")
            #  Регул <- Опусти прошивальщик (плата на ложе2).
            result = self.regul_lower_soldering_iron()
            # "РСервер <- Начни шить. ложе 2"
            result = self.server_start_stitching()
            print(result)
            # Регул <- Подними прошивальщик.
            result = self.regul_raise_soldering_iron()
            print(result)

            ####################### 3 операция на столе
            # Регул <- Сдвинь плату освободив ложе2.
            result = self.regul_move_board_to_free_lodge2()
            print(result)
            # 4. Робот <- Забери плату с ложе 2.
            result = self.robot_take_board_from_lodge2()
            print(result)
            print("Стол 2ложе свободен.")
            # Робот <- Положи плату ложе 2.
            result = self.robot_place_board_on_lodge2()
            print(result)
            # Фоткаем плату перед тем как пместить на ложе
            result = self.make_photo_from_CAM()
            print(result)
            print("Стол 2ложе занято.")
            #  Регул <- Опусти прошивальщик (плата на ложе2).
            result = self.regul_lower_soldering_iron()
            # "РСервер <- Начни шить. ложе 1"
            result = self.server_start_stitching()
            print(result)
            # Регул <- Подними прошивальщик.
            result = self.regul_raise_soldering_iron()
            print(result)
            print("********************************************")



if __name__ == "__main__":

    # Создание объекта и выполнение алгоритма
    table = Table()
    modbus_provider = ModbusProvider()

    modbus_provider.set_outTable11free(1)


    # Выполнение первого цикла
    flag1 = True
    if flag1 == True:
        table.defence_cycle()
        flag1 = False

    # Выполнение первого цикла
    flag = True
    if flag == True:
        table.first_cycle()
        flag = False
    table.main_cycle()
    
        # # Получение данных
        # input1, input2 = modbus_provider.get_data()
        # print(f"Received data - input1: {input1}, input2: {input2}")

        # # Установка данных
        # modbus_provider.set_data(i, 6)
        # i=i+1
        # time.sleep(2)



