import meraki
from prettytable  import PrettyTable


def mtu(api, network_id):
    try:
        dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)
        response = dashboard.switch.getNetworkSwitchMtu(network_id)
        defaultMtu = response['defaultMtuSize']
        overrides = response['overrides']
        if not overrides:
            mtuOverride = "No overrides"
            switches = "No overrides"
        else:
            switches = overrides['switches']
            mtuOverride = overrides['mtuSize']

        if defaultMtu == 9578 == mtuOverride:
            defaultBp = "Good"
        elif defaultMtu == 9578 != mtuOverride:
            defaultBp = "Default MTU meets the best practices"
        elif defaultMtu != 9578 == mtuOverride:
            defaultBp = "Override MTU meets the best practices"
        else:
            defaultBp = "Fail"

        table = PrettyTable()
        table.title = "Network MTU configuration"
        table.field_names = ["Default MTU", "Overrides swithes", "Override MTU", "Best Practice"]
        table.add_row([defaultMtu, switches, mtuOverride, defaultBp])
        print(table)
    except meraki.APIError as e:
        print(e)
        table = PrettyTable()
        table.title = "Network MTU configuration"
        table.field_names = ["Default MTU", "Overrides swithes", "Override MTU", "Best Practice"]
        table.add_row(["None", "None", "None", "None"])
        print(table)

    return (table)