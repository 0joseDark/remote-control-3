#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pip install flask

from flask import Flask, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)

# Configuração dos pinos GPIO
GPIO.setmode(GPIO.BCM)
pins = {
    'pin5': 23,
    'pin6': 24,
    'pin7': 25,
    'pin8': 4
}

for pin in pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/control', methods=['POST'])
def control():
    data = request.json
    command = data.get('command')
    
    if command in pins:
        pin = pins[command]
        GPIO.output(pin, not GPIO.input(pin))  # Toggle the pin state
        state = GPIO.input(pin)
        return jsonify({'status': 'success', 'command': command, 'state': state})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid command'}), 400

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        GPIO.cleanup()
