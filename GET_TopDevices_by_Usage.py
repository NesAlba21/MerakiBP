import meraki
from prettytable import PrettyTable


def get_top_devices_by_usage(api,orgId):
    def mb_togb_to_tb(mb):
        gb = mb/1024
        if gb >= 1024:
            tb= gb/1024
            return tb, "TB"
        else:
            return gb, "GB"

    timespan = 2628288 #One month


    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)


    response = dashboard.organizations.getOrganizationSummaryTopDevicesByUsage(
        orgId, timespan= timespan
    )

    list_devices = []
    for i in response:
        name = i["name"]
        model = i["model"]
        usageTotal = round(i["usage"]["total"])
        usage, unit = mb_togb_to_tb(usageTotal)
        usageRounded = f"{round(usage, 2)} {unit}"
        usagePercentage = round(i["usage"]["percentage"], 2)
        clients = i["clients"]["counts"]["total"]
        listvar = [name, model, clients,  usageRounded, usagePercentage]
        list_devices.append(listvar)

    top10 =list_devices[:10]

    table = PrettyTable()
    table.title = "Top Devices by Usage in the Organization"
    table.field_names = ["Name", "Model", "Clients", "Usage", "% Usage"]
    for row in top10:
        table.add_row(row)
    print(table)

    return(table)