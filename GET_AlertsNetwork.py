import time
import meraki

from prettytable import PrettyTable

def getAlertsNetwork(api, network_id):
    dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)

    response = dashboard.networks.getNetworkAlertsSettings(
        network_id
    )
    responseWebhook = dashboard.networks.getNetworkWebhooksHttpServers(
        network_id
    )
    # Remove the square brackets
    response['defaultDestinations']['emails'] = ', '.join(response['defaultDestinations']['emails'])

    list_alarms = []
    alerts = response['alerts']
    allAdmins_default = response['defaultDestinations']['allAdmins']
    snmp_default = response['defaultDestinations']['snmp']
    emails_default = response['defaultDestinations']['emails']
    webhookid_default = response['defaultDestinations']['httpServerIds']

    if not emails_default:
        emails_default = None

    if not webhookid_default:
        name1 = None
    else:

        name1 = None
        for i in webhookid_default:
            for d in responseWebhook:
                id_Webhook = (d['id'])
                if id_Webhook == i:
                    name1 = d['name']
                    break
            if name1 is not None:
                break

    list_alarms_default = [emails_default, allAdmins_default, snmp_default, name1]

    for data in alerts:
        type = (data['type'])
        status = (data['enabled'])
        emails = (data['alertDestinations']['emails'])
        allAdmins = (data['alertDestinations']['allAdmins'])
        snmp = (data['alertDestinations']['snmp'])
        webhook = (data['alertDestinations']['httpServerIds'])
        name = None
        for d in responseWebhook:
            id_Webhook = (d['id'])
            if id_Webhook == webhook:
                # If the 'id' value matches, save the value of the 'name' key
                name = d['name']


        list_var = [type, status, emails, allAdmins, snmp, name]
        list_alarms.append(list_var)

    # Put Default Alerts into a Pretty Table
    table1 = PrettyTable()
    table1.title = "Network alerts default config"
    table1.field_names = ["Emails", "All Admins", "snmp", "Webhook"]
    table1.add_row(list_alarms_default)
    print(table1)
    print("")
    time.sleep(0.5)


    # Put Alerts into a Pretty Table
    table = PrettyTable()
    table.title = "Network individual alerts config"
    table.field_names = ["Alarm Type", "Enabled", "Emails", "All Admins", "snmp", "Webhook"]
    for row in list_alarms:
        table.add_row(row)
    print(table)

    return (table1, table)
