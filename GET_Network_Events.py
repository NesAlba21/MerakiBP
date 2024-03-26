import meraki
from prettytable import PrettyTable
from collections import Counter


def getNetworkEvents(api, network_id):
    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)

    response1 = dashboard.networks.getNetworkEventsEventTypes(
        network_id
    )

    list_events = []
    list_cat =  []
    for i in response1:
        cat = i['category']
        type = i['type']
        desc = i['description']
        list_var = [cat, type, desc]
        list_events.append(list_var)
        list_c = [cat]
        list_cat.append(list_c)

    #print(list_events)

    # Put the info into a Pretty Table
    table = PrettyTable()
    table.title = "Network Events"
    table.field_names = ["Category", "type", "Description"]
    for row in list_events:
        table.add_row(row)

    only_cat = [i for sublist in list_cat for i in sublist]
    cat_counts = Counter(only_cat)
    total_cat = sum(cat_counts.values())

    cat_percent = {entry: (count/total_cat)*100 for entry, count in cat_counts.items()}
    sorted_cat_percent = dict(sorted(cat_percent.items(), key = lambda item:item[1], reverse=True)[:10])

    table_cat = PrettyTable()
    table_cat.title = "Top 10 Events"
    table_cat.field_names = ["Category", "Percentage"]
    table.align["Category"] = "l"
    table.align["Percentage"] = "l"
    for cat, pct in sorted_cat_percent.items():
        pct= round(pct,2)
        table_cat.add_row([cat, f"{pct} %"])

    print(table_cat)
    return(table_cat)