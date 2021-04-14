import json
import PySimpleGUI as sg

sg.theme('Black')

image_color_frame_layout = [
    [sg.Text("Type"), sg.Combo(["Preset", "Random", "Constant"], "Preset", readonly=True, enable_events=True, key='color_type')],
    [sg.Checkbox("Invert", default=False, key='invert')],
    [sg.Column([
        [sg.Text("Red")],
        [sg.Text("Green")],
        [sg.Text("Blue")],
        [sg.Text("Alpha")]
    ]),
    sg.Column([
        [sg.Input('255', size = (3, 1), key='image_red', disabled=True, disabled_readonly_background_color='black')],
        [sg.Input('255', size = (3, 1), key='image_green', disabled=True, disabled_readonly_background_color='black')],
        [sg.Input('255', size = (3, 1), key='image_blue', disabled=True, disabled_readonly_background_color='black')],
        [sg.Input('255', size = (3, 1), key='image_alpha', disabled=True, disabled_readonly_background_color='black')]
    ])]
]

bg_color_frame_layout = [
    [sg.Column([
        [sg.Text("Red")],
        [sg.Text("Green")],
        [sg.Text("Blue")]
    ]),
    sg.Column([
        [sg.Input('0', size = (3, 1), key='bg_red')],
        [sg.Input('0', size = (3, 1), key='bg_green')],
        [sg.Input('0', size = (3, 1), key='bg_blue')]
    ])]
]

image_size_frame_layout = [
    [sg.Column([
        [sg.Text("Width")],
        [sg.Text("Height")]
    ]),
    sg.Column([
        [sg.Input('300', size = (6, 1), key='image_width')],
        [sg.Input('300', size = (6, 1), key='image_height')]
    ])]
]

image_speed_frame_layout = [
    [sg.Text("Type"), sg.Combo(["Constant", "Random"], "Constant", readonly=True, key='speed_type')],
    [sg.Column([
        [sg.Text("X")],
        [sg.Text("Y")]
    ]),
    sg.Column([
        [sg.Input('1', size = (3, 1), key='image_x')],
        [sg.Input('1', size = (3, 1), key='image_y')]
    ])]
]

layout = [
    [sg.Column([
        [sg.Frame("Image color", image_color_frame_layout, key='a')],
        [sg.Frame("Background color", bg_color_frame_layout)]
    ]),
    sg.Column([
        [sg.Column([
            [sg.Text("Number of images")],
            [sg.Text("Image type")],
            [sg.Text("Refresh speed")],
        ]),
        sg.Column([
            [sg.Spin([i for i in range(1, 11)], 1, size=(2, 1), key='number_of_images')],
            [sg.Spin([i for i in range(1, 3)], 1, size=(2, 1), key='image_type')],
            [sg.Input("100", size=(4, 1), key='refresh_speed')]
        ])],
        [sg.Frame("Image size", image_size_frame_layout)],
        [sg.Frame("Image speed", image_speed_frame_layout)],
    ])],
    [sg.Ok(), sg.Cancel()]
]


def Menu(path = 'config.json'):
    with open(path, 'r') as jsonFile:
        config = json.load(jsonFile)
        
    jsonFile = open('config.json', 'w')
    window = sg.Window("DVD Screensaver Options", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break

        elif event == "Ok":
            config['number_of_images'] = str(values['number_of_images'])
            config['image_type'] = str(values['image_type'])
            config['refresh_speed'] = str(values['refresh_speed'])
            config['image_color']['type'] = str(values['color_type']).lower()
            config['image_color']['invert'] = str(values['invert']).lower()
            config['image_color']['r'] = values['image_red']
            config['image_color']['g'] = values['image_green']
            config['image_color']['b'] = values['image_blue']
            config['image_color']['a'] = values['image_alpha']
            config['background_color']['r'] = values['bg_red']
            config['background_color']['g'] = values['bg_green']
            config['background_color']['b'] = values['bg_blue']
            config['image_size']['width'] = values['image_width']
            config['image_size']['height'] = values['image_height']
            config['image_speed']['type'] = values['speed_type'].lower()
            config['image_speed']['x'] = values['image_x']
            config['image_speed']['y'] = values['image_y']
            break

    json.dump(config, jsonFile, indent=4)
    jsonFile.close()
    window.close()