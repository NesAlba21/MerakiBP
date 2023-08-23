import meraki
from prettytable import PrettyTable

def getWarmSpare(api, network_id):
    try:

        dashboard = meraki.DashboardAPI(api, output_log=False, print_console=False)

        response = dashboard.appliance.getNetworkApplianceWarmSpare(
            network_id
        )

        list_data=[]
        enabled = response['enabled']
        primarySerial = response['primarySerial']
        spareSerial = response['spareSerial']
        try:
            uplinkMode = response['uplinkMode']
        except KeyError:
            uplinkMode = "None"
        try:
            wan1_ip = response['wan1']['ip']
        except KeyError:
            wan1_ip = "None"
        try:
            wan1_subnet = response['wan1']['subnet']
        except KeyError:
            wan1_subnet = "None"
        try:
            wan2_ip = response['wan2']['ip']
        except KeyError:
            wan2_ip = "None"
        try:
            wan2_subnet = response['wan2']['subnet']
        except KeyError:
            wan2_subnet = "None"


        # Check the serial and bring the device name
        responseDevices = dashboard.networks.getNetworkDevices(
            network_id
        )
        namePrimary = None
        for d in responseDevices:
            if d['serial'] == primarySerial:
                # If the 'serial' value matches, save the value of the 'name' key
                namePrimary = d['name']

        nameSpare = None
        for d in responseDevices:
            if d['serial'] == spareSerial:
                # If the 'serial' value matches, save the value of the 'name' key
                nameSpare = d['name']

        list_var = [namePrimary, nameSpare, uplinkMode, wan1_ip, wan1_subnet, wan2_ip, wan2_subnet]
        list_data.append(list_var)


        # Put the info into a Pretty Table
        table = PrettyTable()
        table.title = "Network MX applicance in warmspare"
        table.field_names = ["Primary", "Spare", "Uplink Mode", "Wan1 Ip", "Wan1 Subnet", "Wan2 Ip", "Wan2 Subnet"]
        for row in list_data:
            table.add_row(row)
        print(table)
    except meraki.APIError as e:
        print(e)
        table = PrettyTable()
        table.title = "Network MX applicance in warmspare"
        table.field_names = ["Device", "Status"]
        table.add_row(["None", "No MX device in the network"])
        print(table)
    return (table)

