import meraki

from MerakiAPI import apiInit
from GET_orgs import getOrgs
from GET_NetworksBind import getNetworksBind

api = apiInit()
orgId, table = getOrgs(api)
network_id, selected_option,  table = getNetworksBind(api, orgId)

def firmwareUpgrade(api, network_id):
    dashboard = meraki.DashboardAPI(api, output_log=False, print_console=False)

    response = dashboard.networks.updateNetworkFirmwareUpgrades(
        network_id,
        timezone='America/Los_Angeles',
        products={'appliance': {'nextUpgrade': {'time': '2023-04-10T22:43:00Z', 'toVersion': {'id': '2402'}}, 'participateInNextBetaRelease': False}}
    )

    print(response)

firmwareUpgrade(api, network_id)