import PySimpleGUI as sg
import requests

sg.theme('DarkAmber')  # Add a touch of color
accept = sg.Button('Accept')
reject = sg.Button('Reject')
# All the stuff inside your window.
layout = [[sg.Text('Payment processor emulator')],
          [sg.Text('Type in order ID'), sg.InputText()],
          [accept, reject, sg.Button('Cancel')]]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    elif event == "Accept":
        r = requests.post("http://localhost:8080/payment/ok", json={"id": int(values[0])},
                          headers={"Content-Type": "application/json"})
        if r.json()["status"] == "OK":
            accept.update(button_color="green")
        else:
            accept.update(button_color="red")
    elif event == "Reject":
        r = requests.post("http://localhost:8080/payment/nope", json={"id": int(values[0])},
                          headers={"Content-Type": "application/json"})
        if r.json()["status"] == "OK":
            reject.update(button_color="green")
        else:
            reject.update(button_color="red")

window.close()
