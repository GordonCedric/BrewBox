from repositories.DataRepository import DataRepository

from flask import Flask, jsonify
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS
from helpers.ProjectKlasse import Project
from RPi import GPIO
import threading


GPIO.setwarnings(False)

project = Project()
project.setup()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=True,
                    engineio_logger=True, async_mode="gevent")
CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)


# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.
def all_out():
    while True:
        # [SENSOR DATA OPHALEN EN WEGSCHRIJVEN IN DATABASE]
        DataRepository.add_temperatures(project.get_temperatures())
        DataRepository.add_volumes(project.get_volumes())
        # print('*** We zetten alles uit **')
        # DataRepository.update_status_alle_lampen(0)
        # status = DataRepository.read_status_lampen()
        # socketio.emit('B2F_status_lampen', {'lampen': status})
        # time.sleep(15)

thread = threading.Thread(target = all_out)
thread.start()


print("**** Program started ****")

# API ENDPOINTS


@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    # vraag de status op van de lampen uit de DB
    status = DataRepository.read_status_lampen()
    emit('B2F_status_lampen', {'lampen': status}, broadcast=True)


@socketio.on('F2B_switch_light')
def switch_light(data):
    # Ophalen van de data
    lamp_id = data['lamp_id']
    new_status = data['new_status']
    print(f"Lamp {lamp_id} wordt geswitcht naar {new_status}")

    # Stel de status in op de DB
    res = DataRepository.update_status_lamp(lamp_id, new_status)

    # Vraag de (nieuwe) status op van de lamp en stuur deze naar de frontend.
    data = DataRepository.read_status_lamp_by_id(lamp_id)
    socketio.emit('B2F_verandering_lamp', {'lamp': data})

    # Indien het om de lamp van de TV kamer gaat, dan moeten we ook de hardware aansturen.
    if lamp_id == '3':
        print(f"TV kamer moet switchen naar {new_status} !")
        GPIO.output(led1, new_status)

# ANDERE FUNCTIES


# def lees_knop(pin):
#     if knop1.pressed:
#         print("**** button pressed ****")
#         if GPIO.input(led1) == 1:
#             threading.Thread(target=switch_light(
#                 {'lamp_id': '3', 'new_status': 0})).start()

#         else:
#             switch_light({'lamp_id': '3', 'new_status': 1})
#             threading.Thread(target=switch_light(
#                 {'lamp_id': '3', 'new_status': 1})).start()


# knop1.on_press(lees_knop)

if __name__ == '__main__':

    socketio.run(app, debug=False, host='0.0.0.0')
