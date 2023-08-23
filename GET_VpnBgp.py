import meraki
from prettytable import PrettyTable

def getVpnBgp(api, network_id):
    try:


        dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)

        # Check if Deployment mode is "Passthrough"
        responsecheck = dashboard.appliance.getNetworkApplianceSettings(network_id)

        if responsecheck['deploymentMode'] == 'passthrough':

            response = dashboard.appliance.getNetworkApplianceVpnBgp(network_id)
            if not response:
                # Pretty Table output
                table = PrettyTable()
                table.title = "Network Hub BGP configuration"
                table.field_names = ["Parameter", "Description"]
                table.add_row(["BGP", "No BGP configuration"])
                print(table)

            else:
                list_data = []
                list_neighbors = []
                enabled = response['enabled']
                asNumber = response['asNumber']
                ibgpHoldTimer = response['ibgpHoldTimer']
                neighbors = response['neighbors']
                for data in neighbors:
                    neighborIp = (data['ip'])
                    neighborAs = (data['remoteAsNumber'])
                    ebgpHoldTimer = (data['ebgpHoldTimer'])
                    ebgpMultihop = (data['ebgpMultihop'])
                    listVar = [neighborIp, neighborAs, ebgpHoldTimer, ebgpMultihop]
                    list_neighbors.append(listVar)


                listTemp = [enabled, asNumber, ibgpHoldTimer]
                list_data.append(listTemp)

                # Pretty Table output
                table = PrettyTable()
                table.title = "Hub BGP configuration"
                table.field_names = ["enabled", "AS number", "iBGP hold timer"]
                for row in list_data:
                    table.add_row(row)
                print(table)


                table1 = PrettyTable()
                table1.title = "Hub BGP neighbors configuration"
                table1.field_names =["Neighbor Ip", "Neignbor AS", "eBGP hold timer", "eBGP multihop"]
                for row in list_neighbors:
                    table1.add_row(row)
                print(table1)

        else:
            table = PrettyTable()
            table.title = "BGP info"
            table.field_names = ['Feature', 'Settings']
            table.add_row(['Deployment Mode', ' Mode "Routed" is configured'])
            print(table)

            table1 = PrettyTable()
            table1.title = "Hub BGP neighbors configuration"
            table1.field_names = ["Neighbor Ip", "Neignbor AS", "eBGP hold timer", "eBGP multihop"]
            table1.add_row(['-', '-', '-', '-'])
            print(table1)
    except meraki.APIError as e:
        print(e)
        table = PrettyTable()
        table.title = "Network Hub BGP configuration"
        table.field_names = ["enabled", "AS number", "iBGP hold timer"]
        table.add_row(['-', '-', '-'])
        print(table)

        table1 = PrettyTable()
        table1.title = "Hub BGP neighbors configuration"
        table1.field_names = ["Neighbor Ip", "Neignbor AS", "eBGP hold timer", "eBGP multihop"]
        table1.add_row(['-', '-', '-', '-'])
        print(table1)
    return (table1, table)

