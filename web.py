import os
import hashlib
from flask import Flask
from flask import request, send_from_directory
from controller import Controller


app = Flask(__name__)
controller = Controller('192.168.0.117', 1883, 'devices.txt')


def get_md5(filename):
    with open(filename, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


@app.route('/js/<filename>')
def js_file(filename):
    return send_from_directory(app.config['JS_FOLDER'], filename)


@app.route('/css/<filename>')
def css_file(filename):
    return send_from_directory(app.config['CSS_FOLDER'], filename)


@app.route('/images/<filename>')
def image_file(filename):
    return send_from_directory(app.config['IMAGES_FOLDER'], filename)


def device_to_html(name, device):
    checked = "checked" if device.state == 1 else ""
    hide = 'style="display:none"' if device.value is None else ''

    return '''
    <div class="device" id="{name}" ondblclick="ToggleDevice('{name}')">
        <div class="device-row">
            <label class="switch-checkbox">
                <input type="checkbox" id="{name}-state" {checked} onchange="UpdateDevice('{name}')">
                <span class="switch-checkbox-text"><b>{name}</b></span>
            </label>
        </div>
        <div class="device-row device-value"{hide}>
            <input type="range" class="device-value-track" id="{name}-value" min="0" max="100" step="5" value="{value}"
                title="{value}" onchange="UpdateDevice('{name}')" oninput="DisableUpdate('{name}')">
            <span class="device-value-span" id="{name}-value-span">{value}</span>
        </div>
    </div>
    '''.format(name=name, value=device.value, checked=checked, hide=hide)


def group_to_html(group):
    devices = "\n".join([device_to_html(name, group.devices[name]) for name in group.devices])
    hide = ' style="display:none"' if group.need_hide else ''
    caret = '►' if group.need_hide else '▼'

    return '''
        <div class="group" id="{name}">
            <div class="group-name" onclick="ToggleGroup('{name}')">
                <span class="group-caret" id="{name}-caret">{caret}</span>{name}
            </div>
            <div class="devices" id="{name}-devices"{hide}>{devices}</div>
        </div>
    '''.format(name=group.name, devices=devices, hide=hide, caret=caret)


@app.route('/', methods=['GET'])
def index():
    groups_html = "\n".join([group_to_html(group) for group in controller.groups])
    css = get_md5(app.config["CSS_FOLDER"] + "/styles.css")
    js = get_md5(app.config["JS_FOLDER"] + "/index.js")

    return '''
        <html>
        <head>
            <title>Управление светом</title>
            <meta charset='utf-8'>
            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
            <link rel="stylesheet" type="text/css" href="/css/styles.css?v={css}">

            <link rel="shortcut icon" href="/images/favicon.ico" type="image/x-icon" />
            <link rel="apple-touch-icon" sizes="57x57" href="/images/apple-touch-icon-57x57.png">
            <link rel="apple-touch-icon" sizes="60x60" href="/images/apple-touch-icon-60x60.png">
            <link rel="apple-touch-icon" sizes="72x72" href="/images/apple-touch-icon-72x72.png">
            <link rel="apple-touch-icon" sizes="76x76" href="/images/apple-touch-icon-76x76.png">
            <link rel="apple-touch-icon" sizes="114x114" href="/images/apple-touch-icon-114x114.png">
            <link rel="apple-touch-icon" sizes="120x120" href="/images/apple-touch-icon-120x120.png">
            <link rel="apple-touch-icon" sizes="144x144" href="/images/apple-touch-icon-144x144.png">
            <link rel="apple-touch-icon" sizes="152x152" href="/images/apple-touch-icon-152x152.png">
            <link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon-180x180.png">
            <link rel="icon" type="image/png" href="/images/favicon-16x16.png" sizes="16x16">
            <link rel="icon" type="image/png" href="/images/favicon-32x32.png" sizes="32x32">
            <link rel="icon" type="image/png" href="/images/favicon-96x96.png" sizes="96x96">
            <link rel="icon" type="image/png" href="/images/android-chrome-192x192.png" sizes="192x192">
            <meta name="msapplication-square70x70logo" content="/images/smalltile.png" />
            <meta name="msapplication-square150x150logo" content="/images/mediumtile.png" />
            <meta name="msapplication-square310x310logo" content="/images/largetile.png" />

        </head>
        <body>
            <h1>Наше гнёздышко</h1>
            {groups_html}

            <div class="buttons">
                <div class="button" onclick="TurnOffAll()">Выключить всё</div>
            </div>
            <script src="/js/jquery-3.6.0.min.js"></script>
            <script src="/js/index.js?v={js}"></script>
        </body>
        </html>
    '''.format(groups_html=groups_html, css=css, js=js)


@app.route('/device/<device_name>', methods=['POST'])
def device(device_name):
    state = request.form["state"]
    value = request.form["value"]

    if ' ' in device_name:
        device_name = '"' + device_name + '"'

    controller.process_command('{device_name} {state} {value}'.format(device_name=device_name, state=state, value=value))
    return {"status": "OK"}


@app.route('/devices', methods=['GET'])
def devices():
    return {"devices": [controller.devices[device_name].to_json() for device_name in controller.devices]}


def main():
    host = "0.0.0.0"
    port = 5000
    debug = True

    path = os.path.dirname(__file__)
    app.config['JS_FOLDER'] = os.path.join(path, 'js')
    app.config['CSS_FOLDER'] = os.path.join(path, 'css')
    app.config['IMAGES_FOLDER'] = os.path.join(path, 'images')
    app.run(debug=debug, host=host, port=port)


if __name__ == '__main__':
    main()
