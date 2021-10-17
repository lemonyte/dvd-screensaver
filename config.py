import os
import json
import PySimpleGUI as sg

sg.theme('Black')

image_color_frame_layout = [
    [sg.Text("Type"), sg.Combo(["Preset", "Random", "Constant"], "Preset", readonly=True, enable_events=True, key='color_type')],
    [sg.Column([
        [sg.Text("Red")],
        [sg.Text("Green")],
        [sg.Text("Blue")],
        [sg.Text("Alpha")]
    ]),
    sg.Column([
        [sg.Spin([*range(255)], 255, size=(3, 1), key='image_r')],
        [sg.Spin([*range(255)], 255, size=(3, 1), key='image_b')],
        [sg.Spin([*range(255)], 255, size=(3, 1), key='image_a')],
        [sg.Spin([*range(255)], 255, size=(3, 1), key='image_g')]
    ])],
    [sg.Checkbox("Invert transparency", default=False, key='transparency_inversion')]
]

bg_color_frame_layout = [
    [sg.Column([
        [sg.Text("Red")],
        [sg.Text("Green")],
        [sg.Text("Blue")]
    ]),
    sg.Column([
        [sg.Spin([*range(255)], 0, size=(3, 1), key='bg_r')],
        [sg.Spin([*range(255)], 0, size=(3, 1), key='bg_g')],
        [sg.Spin([*range(255)], 0, size=(3, 1), key='bg_b')]
    ])]
]

image_size_frame_layout = [
    [sg.Column([
        [sg.Text("Width")],
        [sg.Text("Height")]
    ]),
    sg.Column([
        [sg.Input('300', size=(6, 1), key='image_width')],
        [sg.Input('300', size=(6, 1), key='image_height')]
    ])]
]

image_speed_frame_layout = [
    [sg.Text("Type"), sg.Combo(["Constant", "Random"], "Constant", readonly=True, key='speed_type')],
    [sg.Column([
        [sg.Text("X")],
        [sg.Text("Y")]
    ]),
    sg.Column([
        [sg.Input("2", size=(3, 1), key='image_speed_x')],
        [sg.Input("2", size=(3, 1), key='image_speed_y')]
    ])]
]

layout = [
    [sg.Column([
        [sg.Frame("Image color", image_color_frame_layout)],
        [sg.Frame("Background color", bg_color_frame_layout)]
    ]),
    sg.Column([
        [sg.Column([
            [sg.Text("Number of images")],
            [sg.Text("Image style")],
            [sg.Text("Refresh speed")],
        ]),
        sg.Column([
            [sg.Spin([*range(1, 11)], 1, size=(2, 1), key='image_count')],
            [sg.Spin([*range(1, 3)], 1, size=(2, 1), key='style')],
            [sg.Spin([*range(1, 120)], 60, size=(4, 1), key='refresh_speed')]
        ])],
        [sg.Frame("Image size", image_size_frame_layout)],
        [sg.Frame("Image speed", image_speed_frame_layout)],
    ])],
    [sg.Save(), sg.Cancel()]
]


def update_config(config: dict, values: dict):
    config['image_count'] = int(values['image_count'])
    config['style'] = str(values['style'])
    config['refresh_speed'] = int(values['refresh_speed'])
    config['color_type'] = str(values['color_type']).lower()
    config['transparency_inversion'] = bool(values['transparency_inversion'])
    config['image_color'] = {}
    config['image_color']['r'] = int(values['image_r'])
    config['image_color']['g'] = int(values['image_g'])
    config['image_color']['b'] = int(values['image_b'])
    config['image_color']['a'] = int(values['image_a'])
    config['background_color'] = {}
    config['background_color']['r'] = int(values['bg_r'])
    config['background_color']['g'] = int(values['bg_g'])
    config['background_color']['b'] = int(values['bg_b'])
    config['image_size'] = {}
    config['image_size']['width'] = int(values['image_width'])
    config['image_size']['height'] = int(values['image_height'])
    config['image_speed'] = {}
    config['image_speed']['type'] = str(values['speed_type']).lower()
    config['image_speed']['x'] = float(values['image_speed_x'])
    config['image_speed']['y'] = float(values['image_speed_y'])


def menu(path: str = 'config.json'):
    try:
        with open(path, 'r') as file:
            config = json.load(file)
    except Exception:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        config = {}
    window = sg.Window("DVD Screensaver Options", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        elif event == "Save":
            update_config(config, values)
            with open(path, 'w') as file:
                json.dump(config, file, indent=4)
            break
    window.close()
