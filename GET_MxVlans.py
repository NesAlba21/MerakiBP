import meraki
from prettytable import PrettyTable

def getNetMxVlan(api, network_id):
    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)
    # Check if the network has Vlan enabled configured
    responsecheck = dashboard.appliance.getNetworkApplianceVlansSettings(network_id)
    vlansEnabled = responsecheck['vlansEnabled']

    if vlansEnabled == True:
        response = dashboard.appliance.getNetworkApplianceVlans(network_id)

        list_data = []
        for data in response:
            vlanId = (data['id'])
            vlanName = (data['name'])
            applianceIp = (data['applianceIp'])
            subnet = (data['subnet'])
            dhcpHandling = (data['dhcpHandling'])

            dnsServers = (data['dnsNameservers'])
            if dhcpHandling.startswith("Relay"):
                dhcpRelayServerIps  = (data['dhcpRelayServerIps'])
            else:
                dhcpRelayServerIps = "-"
            listTemp = [vlanId, vlanName, applianceIp, subnet, dhcpHandling, dhcpRelayServerIps, dnsServers]
            list_data.append(listTemp)

        # Iterate through the list and remove the square brackets and quotes from list values
        for i in range(len(list_data)):
            for j in range(len(list_data[i])):
                if isinstance(list_data[i][j], list):
                    list_data[i][j] = ', '.join(list_data[i][j]).replace('[', '').replace(']', '')
                else:
                    list_data[i][j] = str(list_data[i][j])

        table = PrettyTable()
        table.title = "MX Vlans"
        table.field_names = ['Id', 'Name', 'Appliance Ip', 'Subnet', 'Dhcp', 'DHCP Server Relay', 'DNS']
        for rows in list_data:
            table.add_row(rows)
        print(table)

    else:
        table = PrettyTable()
        table.title = "MX Vlans"
        table.field_names = ['Feature', 'Settings']
        table.add_row(['Vlans', 'Not enabled for this network'])
        print(table)

    return (table)
