
import meraki
from prettytable import PrettyTable

def getOrgs(api):
    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)

    response = dashboard.organizations.getOrganizations()
    list_data = []
    for data in response:
        orgName = (data['name'])
        orgUrl = (data['url'])
        orgLic = (data['licensing']['model'])
        orgId = (data['id'])
        list_var = [orgName, orgId, orgLic, orgUrl]
        list_data.append(list_var)
    list_data.sort()


    list_clean = []
    for i in list_data:
        new_org = {'name': i[0], 'id': i[1], 'lic' : i[2], 'url' : i[3] }
        list_clean.append(new_org)

    print("[i].  List the organizations that the user has privileges on.")
    # Create Menu from list data
    for i , option in enumerate(list_clean):
        print(f"[{i+1}] {option['name']} ")

    while True:
        choice = int(input("Enter the organization number of your choice: "))
        if choice > 0 and choice <= len(list_clean):
            selected_option = list_clean[choice-1]
            selected_orgId = selected_option['id']
            selected_orgName = selected_option['name']
            selected_orgUrl = selected_option['url']
            selected_orgLic = selected_option['lic']
            print(f"[i]. You have selected '{selected_option['name']}'  organization.")
            print("")
            list_choice = [selected_orgName, selected_orgLic, selected_orgUrl]

            # Put the info into a Pretty Table
            table = PrettyTable()
            table.title = f"{selected_orgName} Organization details"
            table.field_names = ["Name", "License Model", "URL"]
            table.add_row(list_choice)
            #print(table)
            break

        else:
            print("Invalid Option")

    return (selected_orgId, table)




