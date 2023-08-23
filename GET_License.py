import meraki
from prettytable import PrettyTable

def getLicence(api, orgId):

    dashboard = meraki.DashboardAPI(api, output_log=False, print_console=False)


    response = dashboard.organizations.getOrganizationLicensesOverview(
        orgId
    )


    list_licence = []

    status = response['status']
    expData = response['expirationDate']
    deviceCounts = response['licensedDeviceCounts']

    list_var = [deviceCounts, expData]
    list_licence.append(list_var)

    # Put the info into a Pretty Table
    table = PrettyTable()
    table.title = "Licensing details"
    table.field_names = ["Device Model", "Quantity"]
    for device, quantity in deviceCounts.items():
        table.add_row([device, quantity])
    table.align["Device Model"] = "l"
    table.align["Quantity"] = "r"

    # Add Expiration Date column to the table
    expDate = [expData for i in range(len(table.rows))]
    table.add_column("Expiration Date", expDate)

    # Add Status column to the table
    statuses = [status for i in range(len(table.rows))]
    table.add_column("Status", statuses)
    print(table)

    return (table)

