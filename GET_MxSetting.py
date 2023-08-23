import meraki
from prettytable import PrettyTable

def getMxSettings(api, network_id):
    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)

    response = dashboard.appliance.getNetworkApplianceSettings(network_id)


    clientTrackingMethod = response['clientTrackingMethod']
    deploymentMode = response['deploymentMode']

    table = PrettyTable()
    table.title = "Deployment Mode"
    table.field_names = ['Mode', 'Client Tracking Method']
    table.add_row([deploymentMode, clientTrackingMethod])
    print(table)

    return (table)
