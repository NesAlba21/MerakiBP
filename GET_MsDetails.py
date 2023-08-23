import meraki
from prettytable import PrettyTable

def getMsDetail(api, list_serial):

    #This function pull a specific switch information

    if not list_serial:
        table = PrettyTable()
        table.title = "Netowrk switch port status"
        table.field_names = ['Devices', "Status"]
        table.add_row(["None", "None"])
        print(table)

        table1 = PrettyTable()
        table1.title = "Netowrk switch port details"
        table1.field_names = ['Port', "Status"]
        table1.add_row(["None", "None"])
        print(table1)

    else:

        for i in list_serial:  #iterate from serial list
            serial = str(i)
            output_serial = serial.strip("[]'") #delete swuare brackets ans quotes

            dashboard = meraki.DashboardAPI(api, output_log=False, print_console=False)
            response = dashboard.switch.getDeviceSwitchPortsStatuses(output_serial)
            listMsInfo = []
            for ports in response:
                msPort = (ports["portId"])
                msUplink = (ports["isUplink"])
                msSpeed = (ports["speed"])
                msDuplex = (ports["duplex"])
                msErrors = (ports["errors"])
                msWarnings = (ports["warnings"])
                msStatus = (ports['status'])
                listMsInfoVar = [msPort, msUplink, msSpeed, msDuplex, msStatus, msWarnings]
                listMsInfo.append(listMsInfoVar)
            table = PrettyTable()
            table.title = f"{output_serial} switch port statuses"
            table.field_names = ["Port", "Uplink", "Speed", "Duplex", "Status", "Warnings"]
            for row in listMsInfo:
                table.add_row(row)
            print(table)
            print("")

            response = dashboard.switch.getDeviceSwitchPorts(output_serial)
            listMsPortInfo = []
            for ports in response:
                msPortInfoPort = (ports["portId"])
                mSPortInfoPOE = (ports["poeEnabled"])
                msPortInfoVlan = (ports["vlan"])
                msPortInfoVoiceLan = (ports["voiceVlan"])
                msPortInfoType = (ports["type"])
                msPortInfoRSTP = (ports["rstpEnabled"])
                msPortInfoSTP = (ports["stpGuard"])
                msPortInfoName = (ports["name"])
                mSPortInfoAllowedVlans = (ports["allowedVlans"])
                listMsPortInfoVar = [msPortInfoPort, mSPortInfoPOE, msPortInfoVlan, msPortInfoVoiceLan,
                                     mSPortInfoAllowedVlans, msPortInfoType, msPortInfoRSTP, msPortInfoSTP,
                                     msPortInfoName]
                listMsPortInfo.append(listMsPortInfoVar)

            table1 = PrettyTable()
            table1.title = f"{output_serial} MS port info"
            table1.field_names = ["Port", "PoE", "Vlan", "voiceVlan", "allowedVlans", "Type", "RSTP", "STP Guard", "Description"]
            for row in listMsPortInfo:
                table1.add_row(row)
            print(table1)

    return(table1, table)


