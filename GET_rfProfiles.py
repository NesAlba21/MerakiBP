import meraki
from prettytable import PrettyTable

def get_rfProfiles(api, network_id):
    dashboard = meraki.DashboardAPI(api, output_log=False, print_console=False)

    # Check if the network supports wireless
    responsecheck = dashboard.networks.getNetwork(network_id)
    if "wireless" in responsecheck["productTypes"]:
        response = dashboard.wireless.getNetworkWirelessRfProfiles(network_id)
        if response == []:
            table = PrettyTable()
            table.title = "RF Profiles"
            table.field_names = ["Name", "Settings"]
            table.add_row(['-', 'No RF profiles configured'])


        else:
            list_data = []
            for rfSett in response:
                rfName = (rfSett["name"])
                rf24max = (rfSett["twoFourGhzSettings"]["maxPower"])
                rf24min = (rfSett["twoFourGhzSettings"]["minPower"])
                rf24minBit = (rfSett["twoFourGhzSettings"]["minBitrate"])
                rf5max = (rfSett["fiveGhzSettings"]["maxPower"])
                rf5min = (rfSett["fiveGhzSettings"]["minPower"])
                rf5minBit = (rfSett["fiveGhzSettings"]["minBitrate"])
                listRfVar = [rfName, rf24max, rf24min, rf24minBit, rf5max, rf5min, rf5minBit]
                list_data.append(listRfVar)

                table = PrettyTable()
                table.title = "RF Profiles"
                table.field_names = ["Name", "2.4 MaxPower", "2.4 minPower", "2.4 minBitrate", "5Ghz MaxPower", "5Ghz minPower",
                       "5Ghz minBitrate"]
                for rows in list_data:
                    table.add_row(rows)
    else:
        table = PrettyTable()
        table.title = "Netowrk SSID"
        table.field_names = ["Feature", "Settings"]
        table.add_row(["Network Product", "This network does not support wireless"])

    print(table)
    return (table)



