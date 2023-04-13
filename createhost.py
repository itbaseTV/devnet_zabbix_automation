
#author: HCM Engineer
#content: create host in zabbix from csv
 
from pyzabbix import ZabbixAPI
import csv
from progressbar import ProgressBar, Percentage, ETA, ReverseBar, RotatingMarker, Timer

zapi = ZabbixAPI("http://192.168.88.30/zabbix")
zapi.login(user="Admin", password="zabbix")

arq = csv.reader(open('hosts.csv'))

linhas = sum(1 for linha in arq)

f = csv.reader(open('hosts.csv'), delimiter=',')
bar = ProgressBar(maxval=linhas,widgets=[Percentage(), ReverseBar(), ETA(), RotatingMarker(), Timer()]).start()
i = 0

for [hostname,ip,host_group_name,template_name] in f:
    
    host_group = zapi.hostgroup.get(filter={"name": host_group_name})
    host_groupid = host_group[0]['groupid']
    
    template = zapi.template.get(output="extend", filter={"host": template_name})
    template_id = template[0]['templateid']
    try:
        hostcriado = zapi.host.create(
            host = hostname,
            status = 1, 
            # 1- disable host
            # 0- enable host
            interfaces=[{
                "type": 1,
                "main": "1",
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": 10050
            }],
            groups=[{
                "groupid": host_groupid
            }],
            templates=[{
                "templateid": template_id
            }]
        )
    except:
        print(hostname + "FAILED")
    i += 1
    bar.update(i)

bar.finish