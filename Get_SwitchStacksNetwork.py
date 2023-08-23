import meraki
from prettytable import PrettyTable

def getSwitchStack(api, network_id):
    try:

        dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)

        response = dashboard.switch.getNetworkSwitchStacks(
            network_id
        )

        # Remove square brackets from productTypes
        for item in response:
            item['serials'] = ', '.join(item['serials'])

        list_stacks = []
        if not response:
            name = "None"
            serials = "None"
            list_var = [name, serials]
            list_stacks.append(list_var)


        else:
            for data in response:
                name = (data['name'])
                serials = (data['serials'])
                list_var = [name, serials]
                list_stacks.append(list_var)

        # Put Default Alerts into a Pretty Table
        table = PrettyTable()
        table.title = "Network Switch Stacks"
        table.field_names = ["Stack name", "Stack Members"]
        for row in list_stacks:
            table.add_row(row)
        print(table)


    except meraki.APIError as e:
        print(e)

        table = PrettyTable()
        table.title = "Network Switch Stacks"
        table.field_names = ["Stack name", "Stack Members"]
        table.add_row(["None", "No MS in this network"])
        print(table)

    return (table)

