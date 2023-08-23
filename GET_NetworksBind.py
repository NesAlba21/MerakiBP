import meraki
from prettytable import PrettyTable


def getNetworksBind(api, orgId):

    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)
    response = dashboard.organizations.getOrganizationNetworks(
        orgId, total_pages='all'
    )

    # Remove square brackets from productTypes
    for item in response:
        item['productTypes'] = ', '.join(item['productTypes'])



    list_data = []
    list_data2 = []
    for data in response:
        networkName = (data['name'])
        networkType = (data['productTypes'])
        networkTz = (data['timeZone'])
        netId = (data['id'])

        if 'configTemplateId' not in data:
            data['configTemplateId'] = 'none'

        networkId = (data['configTemplateId'])

        # Loop through responseTemplates dashboard and check if the 'id' value matches
        responseTemp = dashboard.organizations.getOrganizationConfigTemplates(
            orgId
        )
        name = None
        for d in responseTemp:
            if d['id'] == networkId:
                # If the 'id' value matches, save the value of the 'name' key
                name = d['name']

        list_var = [networkName, networkType, name, networkTz]
        list_var2 = [networkName, netId]
        list_data.append(list_var)
        list_data2.append(list_var2)

    list_data2.sort()
    list_clean = []
    print("List the networks that the user has privileges on the organization.")
    for i in list_data2:
        new_networks = {'name': i[0], 'id': i[1] }
        list_clean.append(new_networks)

    # Create Menu from list data
    for i , option in enumerate(list_clean):
        print(f"[{i+1}] {option['name']} ")
    while True:
        choice = int(input("Enter the network number of your choice: "))
        if choice > 0 and choice <= len(list_clean):
            selected_option = list_clean[choice - 1]
            network_id = selected_option['id']
            print(f"[i]. You have selected '{selected_option['name']}'  network.")
            print("")

            # Put the info into a Pretty Table
            table = PrettyTable()
            table.title = "Networks details"
            table.field_names=["Network Name", "Type", "Binded template", "Time Zone"]
            for row in list_data:
                table.add_row(row)
            break
            #print(table)

        else:
            print("Invalid Option")

    return (network_id, selected_option,  table)




