import PySimpleGUI as sg
import requests

screen = sg.InputText(disabled=True)
beverage_buttons = [
    sg.Button('Carlsberg', button_color="OFF"), sg.Button('Tuborg', button_color="OFF"),
    sg.Button('Okocim', button_color="OFF"), sg.Button('Desperados', button_color="OFF"),
    sg.Button('Sommersby', button_color="OFF"), sg.Button('Kronenburg', button_color="OFF"),
    sg.Button('Kustosz', button_color="OFF"), sg.Button('Grolsch', button_color="OFF")
]
colour_button = sg.Button("Colour")
colours = {4: "red", 5: "green", 6: "blue"}

alternating_color = "white"
# All the stuff inside your window.
layout = [[sg.Text('Table interface')],
          [sg.Text("Screen"), screen],
          [sg.Button('+'), sg.Button('PAY'), sg.Button('-')],
          beverage_buttons[0:4],
          beverage_buttons[4:8],
          [colour_button, sg.Button("Update"), sg.Button('Cancel')]]


def plus():
    r = requests.get('http://127.0.0.1:8082/interface/plus')
    update_state(r.json())


def minus():
    r = requests.get('http://127.0.0.1:8082/interface/minus')
    update_state(r.json())


def pay():
    r = requests.get('http://127.0.0.1:8082/interface/pay')
    update_state(r.json())


def update():
    r = requests.get('http://127.0.0.1:8082/interface/list')
    update_state(r.json())


def beverage(name):
    if name == "Carlsberg":
        beverage_id = 0
    elif name == "Tuborg":
        beverage_id = 1
    elif name == "Okocim":
        beverage_id = 2
    elif name == "Desperados":
        beverage_id = 3
    elif name == "Sommersby":
        beverage_id = 4
    elif name == "Kronenburg":
        beverage_id = 5
    elif name == "Kustosz":
        beverage_id = 6
    elif name == "Grolsch":
        beverage_id = 7

    r = requests.get(f'http://127.0.0.1:8082/interface/beverage/{beverage_id}')
    update_state(r.json())


def update_state(json):
    screen.update(json["screen_text"])
    for index in range(8):
        state = json["buttons"][str(index)]
        if state == "OFF":
            beverage_buttons[index].update(button_color=None)
        elif state == "ON":
            beverage_buttons[index].update(button_color="white")
        else:
            beverage_buttons[index].update(button_color=alternating_color)
    if json["colour"] is not None:
        colour_button.update(button_color=colours[int(json["colour"])])
    else:
        colour_button.update(button_color=None)


def alternate_colour(alternating_color):
    if alternating_color is None:
        return "white"
    else:
        return None


# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read(timeout=1000, timeout_key="switch")
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    elif event == "Update":
        update()
    elif event == '+':
        plus()
    elif event == '-':
        minus()
    elif event == 'PAY':
        pay()
    elif event == "switch":
        alternating_color = alternate_colour(alternating_color)
        update()
    else:
        beverage(event)

window.close()
