import meraki
from prettytable import PrettyTable

def getTemplate(api, orgId):

    dashboard = meraki.DashboardAPI(api, output_log=False, print_console=False)

    response = dashboard.organizations.getOrganizationConfigTemplates(
        orgId
    )

    if not response:
        name = "None"
        productTypes = "None"
        timeZone = "None"
        list_None = [name, productTypes, timeZone]
        # Put the info into a Pretty Table
        table = PrettyTable()
        table.title = "Templates details"
        table.field_names = ["Name", "Type", "Time Zone"]
        table.add_row(list_None)
        print(table)
        print()
    else:
        # Remove square brackets from productTypes
        for item in response:
            item['productTypes'] = ', '.join(item['productTypes'])

        list_data = []
        for data in response:
            t_name = (data['name'])
            t_type = (data['productTypes'])
            t_zone = (data['timeZone'])
            list_t = [t_name, t_type, t_zone]
            list_data.append(list_t)

        list_ids = []
        for id in response:
            list_ids.append(id["id"])


        # Put the info into a Pretty Table
        table = PrettyTable()
        table.title = "Templates details"
        table.field_names=["Name", "Type", "Time Zone"]
        for row in list_data:
            table.add_row(row)
        print(table)
        print()

    return (table)



