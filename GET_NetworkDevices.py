import meraki
from prettytable import PrettyTable


def getNetworkDevices(api, network_id, selected_option):
    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)

    response = dashboard.networks.getNetworkDevices(
        network_id
    )

    for item in response:
        item['tags'] = ', '.join(item['tags'])


    list_devices = []
    list_serial = []
    for data in response:
        try:
            serial = (data['serial'])
        except KeyError:
            serial = "None"
        try:
            macaddress = (data['mac'])
        except KeyError:
            macaddress = "None"
        try:
            tags = (data['tags'])
        except KeyError:
            tags = "None"
        try:
            name = (data['name'])
        except KeyError:
            name = "None"
        try:
            model = (data['model'])
        except KeyError:
            model = "None"

        # Serial List based if there are MS on the network
        modelStr = str(model)
        if modelStr.startswith("MS"):
            listVar = [serial]
            list_serial.append(listVar)


        try:
            lanIp = (data['lanIp'])
        except KeyError:
            lanIp = "None"
        try:
            wan1Ip =  (data['wan1Ip'])
        except KeyError:
            wan1Ip = "None"
        try:
            wan2Ip = (data['wan2Ip'])
        except KeyError:
            wan2Ip = "None"

        list_var = [name, model, serial, macaddress, tags, lanIp, wan1Ip, wan2Ip]
        list_devices.append(list_var)


    # Put the info into a Pretty Table
    table = PrettyTable()
    table.title = f"{selected_option['name']} Network Devices"
    table.field_names = ["Name", "Model", "Serial", "Mac", "Tags", "LAN Ip", "Wan1 Ip", "Wan2 Ip"]
    table.align["Name"] = "l"
    table.align["Model"] = "l"
    for row in list_devices:
        table.add_row(row)
    print(table)
    return (list_serial, table)

def getNetworkDevicesWeb(api, network_id):
    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)

    response = dashboard.networks.getNetworkDevices(
        network_id
    )

    for item in response:
        item['tags'] = ', '.join(item['tags'])

    list_devices = []
    list_serial = []
    for data in response:
        try:
            serial = (data['serial'])
        except KeyError:
            serial = "None"
        try:
            macaddress = (data['mac'])
        except KeyError:
            macaddress = "None"
        try:
            tags = (data['tags'])
        except KeyError:
            tags = "None"
        try:
            name = (data['name'])
        except KeyError:
            name = "None"
        try:
            model = (data['model'])
        except KeyError:
            model = "None"

        # Serial List based if there are MS on the network
        modelStr = str(model)
        if modelStr.startswith("MS"):
            listVar = [serial]
            list_serial.append(listVar)

        try:
            lanIp = (data['lanIp'])
        except KeyError:
            lanIp = "None"
        try:
            wan1Ip = (data['wan1Ip'])
        except KeyError:
            wan1Ip = "None"
        try:
            wan2Ip = (data['wan2Ip'])
        except KeyError:
            wan2Ip = "None"

        list_var = [name, model, serial, macaddress, tags, lanIp, wan1Ip, wan2Ip]
        list_devices.append(list_var)

    # Put the info into a Pretty Table
    table = PrettyTable()
    table.title = f"{network_id} Network Devices"
    table.field_names = ["Name", "Model", "Serial", "Mac", "Tags", "LAN Ip", "Wan1 Ip", "Wan2 Ip"]
    table.align["Name"] = "l"
    table.align["Model"] = "l"
    for row in list_devices:
        table.add_row(row)
    print(table)
    return (list_serial, table)