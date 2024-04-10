
import meraki
from prettytable import PrettyTable

"""This function pull the top SSIDs on the Organization 
https://developer.cisco.com/meraki/api-v1/get-organization-summary-top-ssids-by-usage/"""
def get_top_ssid_by_usage(api, orgId):
    def mb_togb_to_tb(mb):
        gb = mb/1024
        if gb >= 1024:
            tb= gb/1024
            return tb, "TB"
        else:
            return gb, "GB"


    timespan = 2628288 #One month

    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)
    response = dashboard.organizations.getOrganizationSummaryTopSsidsByUsage(
        orgId, timespan=timespan)
    listTopSsids = []
    for topSsids in response:
        topSsidName = (topSsids["name"])
        topSsidUsage = round(topSsids["usage"]["total"])
        usage, unit = mb_togb_to_tb(topSsidUsage)
        usageRounded = f"{round(usage, 2)} {unit}"
        topSsidPrct = (topSsids["usage"]["percentage"])
        topSsidClients = (topSsids["clients"]["counts"]["total"])
        listTopSsidsVar = [topSsidName, usageRounded, topSsidClients, topSsidPrct]
        listTopSsids.append(listTopSsidsVar)




    # Put the info into a Pretty Table
    table = PrettyTable()
    table.title = "Top Ssids By Usage"
    table.field_names = ["Name", "Usage", "Clients", "% Usage"]
    for row in listTopSsids:
        table.add_row(row)
    print(table)
    return(table)
