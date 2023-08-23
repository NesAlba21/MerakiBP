import meraki
from prettytable import PrettyTable

def getNetworkVpn(api, network_id):

    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)


    response = dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(network_id)


    try:
        mode = response['mode']
    except KeyError:
        mode = "None"
    try:
        hubs = response['hubs']
    except KeyError:
        hubs = []

    list_subnets = []
    if not hubs:
        hubsResponse = "-"
        table3 = PrettyTable()
        table3.title = "Hubs configured for the MX "
        table3.field_names = ['Hub Id', 'Use default route']
        table3.add_row(['-','-'])
        print(table3)
    else:
        list_hubs = []
        hubsResponse = "Yes"
        for dataHub in hubs:
            hubId = (dataHub['hubId'])
            useDefaultRoute = (dataHub['useDefaultRoute'])
            listTemp =[hubId,useDefaultRoute]
            list_hubs.append(listTemp)
        table3 = PrettyTable()
        table3.title = "Hubs configured"
        table3.field_names = ['Hub Id', 'Use default route']
        for row in list_hubs:
            table3.add_row(row)
        print(table3)

    try:
        subnets = response['subnets']
    except KeyError:
        subnets = []
    if not subnets:
        subnetsResponse = "None"

    else:
        subnetsResponse = subnets
        for data in subnetsResponse:
            localSubnet = (data['localSubnet'])
            useVpn = (data['useVpn'])
            listTemp = [localSubnet, useVpn]
            list_subnets.append(listTemp)

    list_clean = []
    for i in list_subnets:
        subnetsDict = {'localSubnet': i[0], 'useVpn': i[1]}
        list_clean.append(subnetsDict)

    table = PrettyTable()
    table.title = "Site-to-Site Vpn Mode"
    table.field_names = ["Mode", "Hubs"]
    table.add_row([mode, hubsResponse])
    print(table)



    table2 = PrettyTable()
    table2.title = "Site-to-Site VPN Subnets"
    table2.field_names = ['Local Subnet', 'Use Vpn']
    for row in list_clean:
        table2.add_row([row['localSubnet'], row['useVpn']])
    print(table2)

    return(table3, table2, table)
