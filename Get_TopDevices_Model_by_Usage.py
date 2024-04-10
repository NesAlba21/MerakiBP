import meraki
from prettytable import PrettyTable


def get_top_devices_Model_by_usage(api, orgId):


    def mb_togb_to_tb(mb):
        gb = mb/1024
        if gb >= 1024:
            tb= gb/1024
            return tb, "TB"
        else:
            return gb, "GB"

    timespan = 2628288 #One month


    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)


    response = dashboard.organizations.getOrganizationSummaryTopDevicesModelsByUsage(
        orgId, timespan=timespan
    )

    print(response)

    list_model = []
    for i in response:
        model = i["model"]
        count = i["count"]
        usageTotal = i["usage"]["total"]
        usageT, unit = mb_togb_to_tb(usageTotal)
        usageRoundedTotal = f"{round(usageT, 2)} {unit}"
        usageAvg = i["usage"]["average"]
        usageA, unit = mb_togb_to_tb(usageAvg)
        usageRoundedAvg = f"{round(usageA, 2)} {unit}"
        list_var = [model, count, usageRoundedTotal, usageRoundedAvg]
        list_model.append(list_var)

    top10 = list_model[:10]

    table = PrettyTable()
    table.title = "Top Devices Models by Usage in the Organization"
    table.field_names = ["Model", "Count", "Usage", "Avg Usage per Device"]
    for row in top10:
        table.add_row(row)

    print(table)
    return(table)