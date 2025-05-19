bash
python3 -m venv arduino_env

source arduino_env/bin/activate

pip install streamlit pyserial

streamlit run app.py
