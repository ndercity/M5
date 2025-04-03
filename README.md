```bash
rmdir /s /q venv
python -m venv venv
.venv\Scripts\activate
pip install flask
flask --app app run --debug
