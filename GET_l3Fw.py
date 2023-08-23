import meraki
from prettytable import PrettyTable

def getl3Fw(api,  network_id):
    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)
    # Check if the network supports wireless
    responsecheck = dashboard.networks.getNetwork(network_id)
    if "appliance" in responsecheck["productTypes"]:
        response = dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)

        list_data = []
        for data in response['rules']:
            policy = (data['policy'])
            protocol = (data['protocol'])
            srcPort = (data['srcPort'])
            srcCidr = (data['srcCidr'])
            destPort = (data['destPort'])
            destCidr = (data['destCidr'])
            syslogEnabled = (data['syslogEnabled'])
            comment = (data['comment'])
            list_Temp = (comment, policy, protocol, srcPort, srcCidr, destPort, destCidr, syslogEnabled)
            list_data.append(list_Temp)


        table = PrettyTable()
        table.title = "L3 Firewall rules"
        table.field_names = ['Description', 'policy', 'protocol', 'srcPort', 'srcCidr', 'destPort', 'destCidr', 'syslogEnabled']
        for rows in list_data:
            table.add_row(rows)

    else:
        table = PrettyTable()
        table.title = "L3 Firewall rules"
        table.field_names = ["Feature", "Settings"]
        table.add_row(["Network Product", "This network does not support appliance settings"])


    print(table)
    return (table)
