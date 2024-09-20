import random

import serial
from utility.data import YAMLDataHandler
from datetime import datetime
from modules.utils import Ticks

if __name__ == "__main__":
    try:
        print(f"[INFO] Serial Communication Initialize")
        coms = serial.Serial('COM24', 9600, timeout=1)  # serial config
        coms.reset_input_buffer()
        arduino_data = []
        send_time = 0
        while True:
            try:
                if Ticks() - send_time >= 1000:
                    send_time = Ticks()
                    output_state = random.randint(0, 1)
                    button_state = random.randint(0, 1)
                    dummy_value = random.randint(200, 400)
                    write_data = f"{output_state} {button_state} {dummy_value}\n"
                    coms.write(write_data.encode('utf-8'))
                    coms.flush()
                if coms.in_waiting > 0:
                    buffer_data = coms.readline().decode('utf-8', 'ignore').strip().split()
                    arduino_data = buffer_data if len(buffer_data) == 4 else arduino_data
                    print(arduino_data)
                    coms.reset_input_buffer()
            except (TypeError, Exception) as e:
                pass
    except (RuntimeError, Exception) as e:
        print(f"[ERROR] {datetime.timestamp(datetime.now())} Serial Initialize Failed: \n{e}")
