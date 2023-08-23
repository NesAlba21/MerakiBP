import meraki
from prettytable import PrettyTable

def getSnmp(api, orgId):
    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)

    response = dashboard.organizations.getOrganizationSnmp(orgId)

    snmpV2 = response['v2cEnabled']
    snmpV3 =  response['v3Enabled']
    peerIps = response['peerIps']
    hostname = response['hostname']
    snmpPort = response['port']
    v3AuthMode = response['v3AuthMode']
    v3PrivMode = response['v3PrivMode']


    if snmpV2 == True:
        v2CommunityString = response['v2CommunityString']
        table = PrettyTable()
        table.title = "SNMP"
        table.field_names = ['V2', 'Hostname', 'Port', 'Peers']
        table.add_row([snmpV2, hostname, snmpPort, peerIps])


    elif snmpV3 == True:
        table = PrettyTable()
        table.title = "SNMP"
        table.field_names = ['V3', 'Auth mode', 'Privacy mode', 'Hostname', 'Port', 'Peers']
        table.add_row([snmpV3,v3AuthMode, v3PrivMode,  hostname, snmpPort, peerIps])


    else:
        table = PrettyTable()
        table.title = "SNMP"
        table.field_names = ['v2', 'v3', 'Hostname', 'Port']
        table.add_row(['Disabled', 'Disbaled', hostname, snmpPort])

    print(table)
    return (table)

