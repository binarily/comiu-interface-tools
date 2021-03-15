import PySimpleGUI as sg
import requests

sg.theme('LightBrown')  # Add a touch of color
order = sg.Multiline('Orders will appear here', size=(45, 5), disabled=True)
segments = [
    sg.Button(f"Segment #{x}") for x in range(4)
]
current_state = ""
current_id = -1
colours = {4: "red", 5: "green", 6: "blue"}
segment_ids = {7: 0, 8: 1, 9: 2, 10: 3}
# All the stuff inside your window.
layout = [[sg.Text('First available order')],
          [order],
          segments,
          [sg.Button('Change state'), sg.Button('Cancel')]]

# Create the Window
window = sg.Window('Window Title', layout)


def update_data(json, new_state=False):
    if current_state == "" and len(json) > 0:
        current_order = json[0]
        new_state = "prepared"
        new_id = current_order["id"]
        order_string = f"Order #{new_id}\n"
        for element in current_order["elements"]:
            order_string += f"{element['beverage']['name']} x {element['quantity']}\n"
        order.update(value=order_string)
        return (new_id, new_state)
    elif current_state == "prepared" and new_state:
        # Add colour to segment
        current_order = json[0]
        new_colour = colours[int(current_order["colour"]["colour"])]
        new_segment = segment_ids[int(current_order["colour"]["segment"])]
        segments[new_segment].update(button_color=new_colour)
        return current_id, "ready"
    elif current_state == "ready" and new_state:
        # Remove colour from segment
        for segment in segments:
            segment.update(button_color=None)
        order.update(value="")
        return current_id, ""
    elif len(json) > 0:
        current_order = json[0]
        order_string = f"Order #{current_id}\n"
        for element in current_order["elements"]:
            order_string += f"{element['beverage']['name']} x {element['quantity']}\n"
        order.update(value=order_string)
        for segment in segments:
            segment.update(button_color=None)
        for received_orders in json:
            if received_orders["colour"] is not None:
                new_colour = colours[int(received_orders["colour"]["colour"])]
                new_segment = segment_ids[int(received_orders["colour"]["segment"])]
                segments[new_segment].update(button_color=new_colour)
        return current_id, current_state
    else:
        for segment in segments:
            segment.update(button_color=None)
        order.update(value="")
        return current_id, ""


def change_state():
    if current_state == "":
        return current_id, current_state
    elif current_state == "prepared":
        r = requests.get(f'http://127.0.0.1:8081/interface/ready/{current_id}')
        return update_data(r.json(), new_state=True)
    elif current_state == "ready":
        r = requests.get(f'http://127.0.0.1:8081/interface/done/{current_id}')
        return update_data(r.json(), new_state=True)


def update():
    r = requests.get(f'http://127.0.0.1:8081/interface/list')
    return update_data(r.json())


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read(timeout=1000, timeout_key="Update")
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    elif event == "Change state":
        (current_id, current_state) = change_state()
    elif event == "Update":
        (current_id, current_state) = update()

window.close()
