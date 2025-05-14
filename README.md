```bash
rmdir /s /q .venv
python -m venv venv
venv\Scripts\activate
pip install flask
flask --app app run --debug

Packages:
pip install flask
pip install opencv_python
pip install mediapipe
pip install customtkinter
pip install Pillow
pip install python-dotenv
pip install fpdf

To run the RFID app use this followig command in the terminal:
1. install the following
 pip install mfrc522
 pip install Pillow
2. venv/Scripts/activate or .venv/bin/activate (in raspi linux)
3. cd Photobooth/rfid
3. python main.py
