import meraki
from prettytable import PrettyTable

def firmware(api, network_id):

    dashboard = meraki.DashboardAPI(api, output_log=False, print_console=False)

    # Get the available version
    response = dashboard.networks.getNetworkFirmwareUpgrades(
        network_id
    )

    # Get the current devices version
    responseDevices = dashboard.networks.getNetworkDevices(
        network_id
    )

    # Get the available firmware from every single meraki devices
    try:
        applianceFirmware = (response["products"]["appliance"]["availableVersions"])
        for firmware in applianceFirmware:
            availableAppl = (firmware["firmware"])
            releaseType = (firmware['releaseType'])
    except KeyError:
        print("")

    try:
        switchFirmware = (response["products"]["switch"]["availableVersions"])
        for firmware in switchFirmware:
            availableSw = (firmware["firmware"])
            releaseType = (firmware['releaseType'])
    except KeyError:
        print("")

    try:
        wirelessFirmware = (response["products"]["wireless"]["availableVersions"])
        for firmware in wirelessFirmware:
            availableWireless = (firmware["firmware"])
            releaseType = (firmware['releaseType'])
    except KeyError:
        print("")


    # Get meraki current devices from a network
    listDevices = []
    for devices in responseDevices:
        settingsToPrint = {
            "name": devices["name"] if "name" in devices else None,
            "serial": devices["serial"] if "serial" in devices else None,
            "model": devices["model"] if "model" in devices else None,
            "firmware": devices["firmware"] if "firmware" in devices else None,
        }
        deviceName = (settingsToPrint["name"])
        deviceSerial = (settingsToPrint["serial"])
        deviceModel = (settingsToPrint["model"])
        deviceFirmware = (settingsToPrint["firmware"])
        listDevicesVar = [deviceName, deviceSerial, deviceModel, deviceFirmware]
        listDevices.append(listDevicesVar)

    """Print the available applicances versions"""
    #print(availableAppl)
    #print(availableSw)
    #print(availableWireless)
    #print(listDevices)


    # Searching device string in current devices list and add the available version
    search_appliance = "wired"
    search_switch = "switch"
    search_wireless = "wireless"
    search_notConfigVersion = "Not"


    for i in range(len(listDevices)):
        for j in range(len(listDevices[i])):
            if listDevices[i][j] is not None and search_wireless in listDevices[i][j]:
                listDevices[i].append(availableWireless)
                listDevices[i].append(releaseType)

            elif listDevices[i][j] is not None and search_switch in listDevices[i][j]:
                listDevices[i].append(availableSw)
                listDevices[i].append(releaseType)

            elif listDevices[i][j] is not None and search_appliance in listDevices[i][j]:
                listDevices[i].append(availableAppl)
                listDevices[i].append(releaseType)

            #Fix the "Not running current verion" string in the devices list
            elif listDevices[i][j] is not None and search_notConfigVersion in listDevices[i][j]:

                data = str(deviceModel)
                #print(data)
                if data.startswith("MR"):
                    listDevices[i].append(availableWireless)
                    listDevices[i].append(releaseType)

                elif data.startswith("MX"):
                    listDevices[i].append(availableAppl)
                    listDevices[i].append(releaseType)

                elif data.startswith("MS"):
                    listDevices[i].append(availableSw)
                    listDevices[i].append(releaseType)

    #Check responses
    #print(response)
    #print(responseDevices)
    #print(listDevices)

    # Put the info into a Pretty Table
    table = PrettyTable()
    table.title = "Firmware Version"
    table.field_names=["Name", "Serial", "Model",  "Current Version", "Available Version", "Release Type"]
    table.align["Name"] = "l"
    table.align["Current Version"] = "l"
    table.align["Available Version"] = "l"
    for row in listDevices:
        table.add_row(row)
    print(table)
    print()

    return(table)

