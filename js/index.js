let devices = document.getElementsByClassName('device')
let device_ids = []
let device_states = []
let device_values = []
let device_value_spans = []
let is_updating = []

for (device of devices) {
    device_ids.push(device.id)
    device_states.push(document.getElementById(device.id + '-state'))
    device_values.push(document.getElementById(device.id + '-value'))
    device_value_spans.push(document.getElementById(device.id + '-value-span'))
    is_updating.push(false)
}

function DisableUpdate(id) {
    let index = device_ids.indexOf(id)
    is_updating[index] = true
    device_value_spans[index].innerHTML = device_values[index].value
}

function EnableUpdate(id) {
    setTimeout(function() {
        is_updating[device_ids.indexOf(id)] = false
    }, 500)
}

function ToggleDevice(id) {
    device_states[device_ids.indexOf(id)].checked ^= true
    UpdateDevice(id)
}

function UpdateDevice(id) {
    let index = device_ids.indexOf(id)
    let state = device_states[index].checked ? 1 : 0
    let value = +device_values[index].value
    is_updating[index] = true

    $.post(`/device/${id}`, { "state": state, "value": value }, function(data) { EnableUpdate(id) })
}

function UpdateDevicesContent(data, status) {
    for (let i = 0; i < devices.length; i++) {
        if (is_updating[i])
            continue

        device_states[i].checked = data["devices"][i].state == 1
        device_values[i].value = data["devices"][i].value
        device_values[i].title = data["devices"][i].value
        device_value_spans[i].innerHTML = data["devices"][i].value
    }
}

setInterval(function() {
    $.get(`/devices`, UpdateDevicesContent)
}, 500)
