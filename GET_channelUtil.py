import meraki
from GET_firmware import firmware
from prettytable import PrettyTable

def getChannelUtil(api, network_id):
    dashboard = meraki.DashboardAPI(api, output_log=False, print_console=False)
    #Liste = firmware(api, network_id)
    #print(Liste.attributes)
    #Check if the network supports wireless
    responsecheck = dashboard.networks.getNetwork(network_id)
    if "wireless" in responsecheck["productTypes"]:

        response = dashboard.networks.getNetworkNetworkHealthChannelUtilization(network_id, total_pages='all')

        bandera = 0
        flotantes24 = 0.0
        flotantes50 = 0.0
        list_data = []

        for apInfo in response:
            apSerial = apInfo["serial"]
            apModel = apInfo["model"]
            apUtil24 = apInfo["wifi0"]
            apUtil50 = apInfo["wifi1"]

            for apUtil in apUtil24:
                flotantes24 = flotantes24 + apUtil["utilization"]

            total24 = flotantes24 / 144
            total_24 = round(total24,2)
            total_24 = f"{total_24}%"

            for apUtil in apUtil50:
                flotantes50 += apUtil["utilization"]

            total50 = flotantes50 / 144
            total_50 = round(total50,2)
            total_50 = f"{total_50}%"


            compliant24 = "Compliant"
            compliant50 = "Compliant"

            if total24 > 60:
                compliant24 = "Failed"

            if total50 > 40:
                compliant50 = "Failed"

            listChannelVar = [apSerial, apModel, total_24, total_50, compliant24, compliant50]
            list_data.append(listChannelVar)
            table = PrettyTable()
            table.title = "Channel Utilization"
            table.field_names = ["Serial", "Model", "2.4 GHz Utilization 1 day","5.0GHz Utilization 1 day", "2.4GHz Best Practice", "5.0GHz Best Practice" ]

            for rows in list_data:
                table.add_row(rows)

        print(table)

    return (table)
