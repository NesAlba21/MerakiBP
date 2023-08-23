import meraki
from prettytable import PrettyTable

def getSsid(api, network_id):
    dashboard = meraki.DashboardAPI(api, output_log=False, print_console=False)

    #Check if the network supports wireless
    responsecheck = dashboard.networks.getNetwork(network_id)
    if "wireless" in responsecheck["productTypes"]:

        response = dashboard.wireless.getNetworkWirelessSsids(network_id)

        list_data = []
        for ssidsInf in response:
            if ssidsInf["enabled"] == True:
                ssidsName = (ssidsInf["name"])
                ssidsAuth = (ssidsInf["authMode"])

                try:
                    ssidsEnc = (ssidsInf["encryptionMode"])
                except KeyError:
                    ssidsEnc = "-"

                try:
                    ssidsWpa = (ssidsInf["wpaEncryptionMode"])
                except KeyError:
                    ssidsWpa = '-'
                try:
                    ssidsIpAss = (ssidsInf["ipAssignmentMode"])
                except KeyError:
                    ssidsIpAss = '-'

                if ssidsInf["authMode"] == "8021x-radius":
                    for ssidsRadVar in ssidsInf["radiusServers"]:
                        ssidsRad = (ssidsRadVar["host"])
                        ssidsRadPort = (ssidsRadVar["port"])
                else:
                    ssidsRad = "None"
                    ssidsRadPort = "None"
                    listSsidsVar = [ssidsName, ssidsAuth, ssidsEnc, ssidsWpa, ssidsRad, ssidsRadPort, ssidsIpAss]
                    list_data.append(listSsidsVar)
        table = PrettyTable()
        table.title = "Netowrk SSIDs"
        table.field_names = ["Name", "Auth", "Encryption", "WPA mode", "Radius", "Radius Port", "Ip Assignment"]
        for rows in list_data:
            table.add_row(rows)
        print(table)

    else:
        table = PrettyTable()
        table.title = "Netowrk SSID"
        table.field_names = ["Feature", "Settings"]
        table.add_row(["Network Product", "This network does not support wireless"])
        print(table)

    return  (table)