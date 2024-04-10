import meraki
from prettytable import PrettyTable


def get_top_sw_by_energy_usage(api, orgId):
    timespan = 2628288 #One month

    #Convert Joules to Watts
    def joules_to_watts(joules, timespan):
        return joules/timespan, "W"

    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)


    response = dashboard.organizations.getOrganizationSummaryTopSwitchesByEnergyUsage(
        orgId, timespan=timespan
    )
    print(response)

    list_sw = []
    for i in response:
        network = i["network"]["name"]
        nameSw = i ["name"]
        model = i["model"]
        usageJoules = i["usage"]["total"]
        usageWatts, unit = joules_to_watts(usageJoules, timespan)
        usageW = f"{round(usageWatts,2)} {unit}"

        list_var = [network, nameSw, model, usageW]
        list_sw.append(list_var)

    table = PrettyTable()
    table.title = "Top Switches By Energy Usage"
    table.field_names = ["Network", "Sw Name", "Sw Model", "Usage"]
    for row in list_sw:
        table.add_row(row)

    print(table)
    return(table)