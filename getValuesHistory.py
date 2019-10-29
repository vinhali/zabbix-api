from zabbix.api import ZabbixAPI
from datetime import datetime, date, time, timedelta

zapi = ZabbixAPI(url='http://ip-zabbix/zabbix', user='Admin', password='zabbix')

# today minus 1 day
d = date.today() - timedelta(days = 1)

# combines the day with the midnight time
startTimestamp = int(datetime.combine(d, time(0, 0)).timestamp())
# combina o dia com o horário 23:59
endTimestamp = int(datetime.combine(d, time(23, 59)).timestamp())

groupFilter = {'name': 'Group Server Name'} # Insert Group Server Name'
itemFilter = {'name': 'Name Item'} # Insert Group Server Name'

# Get the hostgroup id by its name 
hostgroups = zapi.hostgroup.get(filter=groupFilter, output=['groupids', 'name'])

# Get the hosts of the hostgroup by hostgroup id
hosts = zapi.host.get(groupids=hostgroups[0]['groupid'])

for host in hosts:
    # Get the item info (not the values!) by item name AND host id
    items = zapi.item.get(filter=itemFilter, host=host['host'], output='extend', selectHosts=['host', 'name'])

    # for loop - for future fuzzy search, otherwise don't loop and use items[0] 
    for item in items:
        # Get item values
        values = zapi.history.get(itemids=item['itemid'], time_from=startTimestamp, time_till=endTimestamp, history=item['value_type'])
        # print history values
        for historyValue in values:
            print("Hostname:{},ItemID:{},Name:{},Key:({}),Clock:{},Value:{}".format(
                host['host'],
                item['itemid'],
                item['name'],
                item['key_'],
                str(datetime.utcfromtimestamp(int(historyValue['clock'])).strftime('%Y-%m-%d %H:%M:%S')),
                historyValue['value']))
