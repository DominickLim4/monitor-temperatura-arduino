import streamlit as st
import serial
import time
import threading
from typing import Optional

class ArduinoController:
    def __init__(self, port: str = "COM3", baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.arduino: Optional[serial.Serial] = None
        self.temperature = 0.0
        self.running = False
        
    def connect(self) -> bool:
        try:
            self.arduino = serial.Serial(self.port, self.baudrate)
            time.sleep(2)  # Arduino reset delay
            return True
        except serial.SerialException:
            return False
    
    def disconnect(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            
    def read_temperature(self) -> float:
        if self.arduino and self.arduino.is_open:
            try:
                if self.arduino.in_waiting > 0:
                    line = self.arduino.readline().decode('utf-8').strip()
                    return float(line)
            except (ValueError, UnicodeDecodeError):
                pass
        return self.temperature
    
    def control_led(self, state: bool):
        if self.arduino and self.arduino.is_open:
            command = b'L' if state else b'D'
            self.arduino.write(command)
    
    def monitor_temperature(self):
        while self.running:
            self.temperature = self.read_temperature()
            time.sleep(1)

# Initialize session state
if 'arduino_controller' not in st.session_state:
    st.session_state.arduino_controller = ArduinoController()
    st.session_state.connected = False
    st.session_state.monitoring = False

arduino = st.session_state.arduino_controller

# UI
st.title("Arduino Monitor de Temperatura")

# Connection controls
col1, col2 = st.columns(2)

with col1:
    if st.button("Conectar Arduino"):
        if arduino.connect():
            st.session_state.connected = True
            st.success("Conectado")
        else:
            st.error("Conexão Falha")

with col2:
    if st.button("Desconectar"):
        arduino.disconnect()
        st.session_state.connected = False
        st.session_state.monitoring = False
        arduino.running = False

# Temperature monitoring
if st.session_state.connected:
    if not st.session_state.monitoring:
        if st.button("Começar o monitoramento"):
            arduino.running = True
            st.session_state.monitoring = True
            thread = threading.Thread(target=arduino.monitor_temperature)
            thread.daemon = True
            thread.start()
    
    # Display temperature
    temp_placeholder = st.empty()
    temp_placeholder.metric("Temperatura", f"{arduino.temperature:.1f}°C")
    
    # LED control
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Ligar o LED"):
            arduino.control_led(True)
    
    with col4:
        if st.button("Desligar o LED"):
            arduino.control_led(False)
    
    # Auto refresh
    if st.session_state.monitoring:
        time.sleep(0.1)
        st.rerun()
else:
    st.warning("Arduino nao conectado")