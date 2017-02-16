#
##
# Script de configuration ESXi / tgr 04122014.1 (v1) / ddm 09.04.2015.4
##
#     Timer installation ESX : 3 minutes
#
# Documentation :
#
#     https://github.com/fabric/fabric/issues/369     execution specifique hors /bin/bash
#     https://pubs.vmware.com/vsphere-50/index.jsp#com.vmware.vcli.ref.doc_50/esxcli_network.html
#     https://pubs.vmware.com/vsphere-50/index.jsp?topic=%2Fcom.vmware.vcli.ref.doc_50%2Fesxcli_network.html
#     https://pubs.vmware.com/vsphere-51/index.jsp#com.vmware.vcli.migration.doc/cos_upgrade_technote.1.9.html?resultof=%2522%2565%2573%2578%2563%2566%2567%252d%2576%2573%2577%2569%2574%2563%2568%2522%2520
#     VMWare tools : 
#                       https://www.null-byte.org/development/vmware-tools-on-linux-centos-6-x/
#                       http://steronius.blogspot.be/2013/01/install-vmware-tools-via-repository-for.html
##
# Synthaxe / utilisation - attention aux threads paralleles
#
# fab <fonction> (-P -z <nombre instances en parallele> - option P seule conseillee) -f matice_systools.py
#
#

import fabric.contrib.files
import os.path
from fabric.api import *
#from fabric.contrib.files import append
from fabric.colors import *
import commands

env.roledefs['esx2install'] = ['']

env.user="root"
env.skip_bad_hosts=False
env.timeout=30
env.shell = "/bin/sh -c"

#
# INSTALLATION ESXi
# prerequs  :
#   - avoir installed ESXi
#   - avoir modified le vSwitch0 en vSwitch1 dans /etc/vmware/esx.cfg
#

@roles('')

def ajout_vlan():

      with settings(
      #hide('stderr', 'stdout'),
      abort_on_prompts=False
      ):

#            run('esxcli network vswitch standard portgroup add -p Adriatic -v vSwitch0 && esxcli network vswitch standard portgroup set --vlan-id=901 --portgroup-name="Adriatic"')
#            run('esxcli network vswitch standard portgroup set --vlan-id=901 --portgroup-name="Adriatic"')
#            run('esxcli network vswitch standard portgroup list | grep vSwitch0 | grep 901')


@roles('esx2install')

def esxfreshinstall():

        with settings(
        #hide('stderr', 'stdout'),
        abort_on_prompts=False
        ):

            #
            # VARIABLES A TUNER
            #
            ip_hb = '172.26.178.194'
            ip_vmotion = '192.168.230.55'
            #
            ip_iscsi1 = '172.26.178.195'
            ip_iscsi2 = '172.26.178.196'
            ip_iscsi3 = '172.26.178.197'
            ip_iscsi4 = '172.26.178.198'
            #
            serveurdns1 = '172.30.176.100'
            serveurdns2 = '172.30.176.245'
            serveurntp = '172.30.176.100'
            serveurlog = '172.30.176.6'

            # sup shell warnings
            run('esxcli system settings advanced set -i 1 -o /UserVars/SuppressShellWarning')

            # prompt hostname
            hostname = prompt('Saisir le nom d ESX (en miniscules) : ')
            run('esxcli system hostname set --host='+hostname+'')
            run('esxcli network ip dns server add -s '+serveurdns1+'')
            run('esxcli network ip dns server add -s '+serveurdns2+'')
            run('esxcli network ip dns search add -d "in.ac-amiens.fr"')
            run('esxcli network ip dns search add -d "ac-amiens.fr"')
            # n')
            run('rm /etc/ntp.conf')
            put('/home/tom/.bin/DSIN-AMS/ESX/ntp.conf','/etc/')
            run('sed -i -e "s/xxx/'+serveurntp+'/g" /etc/ntp.conf')
            run('chmod 644 /etc/ntp.conf && chmod -t /etc/ntp.conf')
            run('/sbin/chkconfig ntpd on')
            #run('/etc/init.d/ntpd stop')
            #run('/etc/init.d/ntpd start')
            # sn')
            run('esxcli system snmp set --communities public')
            run('esxcli system snmp set --enable true')
            # sysl')
            run('esxcli system syslog config set --loghost="'+serveurlog+'"')
            run('esxcli system syslog reload')
            # firewa')
            run('esxcli network firewall ruleset set --ruleset-id=syslog --enabled=true')
            run('esxcli network firewall refresh')
            # vswitc')
            run('esxcli network vswitch standard add -v vSwitch0')
            # attribution vmnic vswitc')
            #run('esxcli network vswitch standard uplink add -u vmnic2 -v vSwitch1')
            #run('esxcli network vswitch standard uplink add -u vmnic3 -v vSwitch1')
            run('esxcli network vswitch standard policy failover set -a vmnic2,vmnic3 -v vSwitch1')
            # attribution vmnic vswitc')
            run('esxcli network vswitch standard uplink add -u vmnic0 -v vSwitch0')
            run('esxcli network vswitch standard uplink add -u vmnic1 -v vSwitch0')
            run('esxcli network vswitch standard policy failover set -a vmnic0,vmnic1 -v vSwitch0')

            # desactivation du fcoe sur les interfaces
            run('esxcli fcoe nic disable -n=vmnic0')
            run('esxcli fcoe nic disable -n=vmnic1')
            run('esxcli fcoe nic disable -n=vmnic2')
            run('esxcli fcoe nic disable -n=vmnic3')

            # ajout portgroup
            # BOUCLER SUR UNE LISTE ARRAY
            run('esxcli network vswitch standard portgroup add -p mgtswitch -v vSwitch1')
            run('esxcli network vswitch standard portgroup add -p VMkernel -v vSwitch1')
            run('esxcli network vswitch standard portgroup add -p interco_forti_cp -v vSwitch1')
            run('esxcli network vswitch standard portgroup add -p Network_mgt -v vSwitch1')            
            run('esxcli network vswitch standard portgroup add -p wifi_msg -v vSwitch0')
            run('esxcli network vswitch standard portgroup add -p PortailCaptif -v vSwitch0')
            run('esxcli network vswitch standard portgroup add -p VMkernel-iscsi-heartbeat -v vSwitch1')
            run('esxcli network vswitch standard portgroup add -p DMZ-Infra -v vSwitch0')
            run('esxcli network vswitch standard portgroup add -p DMZ-Webapp -v vSwitch0')
            run('esxcli network vswitch standard portgroup add -p DMZ-msg -v vSwitch0')
            run('esxcli network vswitch standard portgroup add -p DMZ-Web -v vSwitch0')
            run('esxcli network vswitch standard portgroup add -p DMZ-Interco-Ext -v vSwitch0')
            run('esxcli network vswitch standard portgroup add -p WebEtab -v vSwitch0')
            run('esxcli network vswitch standard portgroup add -p WebEtabPriv -v vSwitch0')
            run('esxcli network vswitch standard portgroup add -p Racine -v vSwitch1')
            run('esxcli network vswitch standard portgroup add -p LAMP -v vSwitch1')
            run('esxcli network vswitch standard portgroup add -p LAN_860 -v vSwitch1')
            run('esxcli network vswitch standard portgroup add -p wifi_ien_ipr -v vSwitch0')
            run('esxcli network vswitch standard portgroup add -p wifi_divisions -v vSwitch0')
            run('esxcli network vswitch standard portgroup add -p wifi_dinf -v vSwitch0')
            run('esxcli network vswitch standard portgroup add -p Infra_Locales -v vSwitch1')
            run('esxcli network vswitch standard portgroup add -p Agriates -v vSwitch0')
            run('esxcli network vswitch standard portgroup add -p "Racine 172.30.191.0" -v vSwitch0')

            # Set the vlan id for the given portgroup
            run('esxcli network vswitch standard portgroup set --vlan-id=1 --portgroup-name="mgtswitch"')
            run('esxcli network vswitch standard portgroup set --vlan-id=4 --portgroup-name="VMkernel"')
            run('esxcli network vswitch standard portgroup set --vlan-id=5 --portgroup-name="interco_forti_cp"')
            run('esxcli network vswitch standard portgroup set --vlan-id=11 --portgroup-name="Network_mgt"')            
            run('esxcli network vswitch standard portgroup set --vlan-id=30 --portgroup-name="wifi_msg"')
            run('esxcli network vswitch standard portgroup set --vlan-id=31 --portgroup-name="PortailCaptif"')
            run('esxcli network vswitch standard portgroup set --vlan-id=78 --portgroup-name="VMkernel-iscsi-heartbeat"')
            run('esxcli network vswitch standard portgroup set --vlan-id=302 --portgroup-name="WebEtab"')
            run('esxcli network vswitch standard portgroup set --vlan-id=236 --portgroup-name="WebEtabPriv"')
            run('esxcli network vswitch standard portgroup set --vlan-id=460 --portgroup-name="DMZ-Infra"')
            run('esxcli network vswitch standard portgroup set --vlan-id=461 --portgroup-name="DMZ-Webapp"')
            run('esxcli network vswitch standard portgroup set --vlan-id=466 --portgroup-name="DMZ-msg"')
            run('esxcli network vswitch standard portgroup set --vlan-id=471 --portgroup-name="DMZ-Web"')
            run('esxcli network vswitch standard portgroup set --vlan-id=472 --portgroup-name="DMZ-Interco-Ext"')
            run('esxcli network vswitch standard portgroup set --vlan-id=760 --portgroup-name="Racine"')
            run('esxcli network vswitch standard portgroup set --vlan-id=851 --portgroup-name="LAMP"')
            run('esxcli network vswitch standard portgroup set --vlan-id=860 --portgroup-name="LAN_860"')
            run('esxcli network vswitch standard portgroup set --vlan-id=870 --portgroup-name="wifi_ien_ipr"')
            run('esxcli network vswitch standard portgroup set --vlan-id=872 --portgroup-name="wifi_divisions"')
            run('esxcli network vswitch standard portgroup set --vlan-id=876 --portgroup-name="wifi_dinf"')
            run('esxcli network vswitch standard portgroup set --vlan-id=885 --portgroup-name="Infra_Locales"')
            run('esxcli network vswitch standard portgroup set --vlan-id=900 --portgroup-name="Agriates"')
            run('esxcli network vswitch standard portgroup set --vlan-id=910 --portgroup-name="Racine 172.30.191.0"')

            run('esxcli storage nmp satp set --default-psp=VMW_PSP_RR --satp=VMW_SATP_EQL')

            # anciennement esxcfg-vswitch --mtu=9000 ${VS:-vSwitch1}
            run('esxcli network vswitch standard set -m 9000 -v vSwitch1')

            # ancienncement esxcfg-vswitch --set-cdp both ${VS:-vSwitch1}
            run('esxcli network vswitch standard set -c both -v vSwitch1')

            # ADRESSAGE ESX ET STOCKAGE
            #
            # AUTOMATISER LA RECUPERATION DES IP
            #

            # HB ISCSI
            run('esxcfg-vmknic -a -i '+ip_hb+' -n 255.255.255.0 --mtu=9000 VMkernel-iscsi-heartbeat')
            run('esxcli network vswitch standard portgroup set --portgroup-name=VMkernel-iscsi-heartbeat --vlan-id=78')

            # VMOTION
            run('esxcfg-vmknic -a -i '+ip_vmotion+' -n 255.255.255.224 VMkernel')
            run('esxcli network vswitch standard portgroup set --portgroup-name=VMkernel --vlan-id=4')

            # VOIR OU LES AJOUTER
            
            #esxcli network vswitch standard portgroup policy failover set --active-uplinks=vmnic2 --portgroup-name="iSCSI-1"
            #esxcli network vswitch standard portgroup policy failover set --active-uplinks=vmnic3 --portgroup-name="iSCSI-2"
            #esxcli network vswitch standard portgroup policy failover set --active-uplinks=vmnic2 --portgroup-name="iSCSI-3"
            #esxcli network vswitch standard portgroup policy failover set --active-uplinks=vmnic3 --portgroup-name="iSCSI-4"

            #
            run('esxcfg-vswitch -A iSCSI-1 vSwitch1')
            run('esxcfg-vmknic -a -i '+ip_iscsi1+' -n 255.255.255.0 -m 9000 iSCSI-1')
            run('esxcli network vswitch standard portgroup set --portgroup-name=iSCSI-1 --vlan-id=78')
            run('esxcfg-vswitch -p iSCSI-1 -N vmnic3 vSwitch1')

            #
            run('esxcfg-vswitch -A iSCSI-2 vSwitch1')
            run('esxcfg-vmknic -a -i '+ip_iscsi2+' -n 255.255.255.0 -m 9000 iSCSI-2')
            run('esxcli network vswitch standard portgroup set --portgroup-name=iSCSI-2 --vlan-id=78')
            run('esxcfg-vswitch -p iSCSI-2 -N vmnic2 vSwitch1')

            #
            run('esxcfg-vswitch -A iSCSI-3 vSwitch1')
            run('esxcfg-vmknic -a -i '+ip_iscsi3+' -n 255.255.255.0 -m 9000 iSCSI-3')
            run('esxcli network vswitch standard portgroup set --portgroup-name=iSCSI-3 --vlan-id=78')
            run('esxcfg-vswitch -p iSCSI-3 -N vmnic3 vSwitch1')

            #
            run('esxcfg-vswitch -A iSCSI-4 vSwitch1')
            run('esxcfg-vmknic -a -i '+ip_iscsi4+' -n 255.255.255.0 -m 9000 iSCSI-4')
            run('esxcli network vswitch standard portgroup set --portgroup-name=iSCSI-4 --vlan-id=78')
            run('esxcfg-vswitch -p iSCSI-4 -N vmnic2 vSwitch1')

            # recuperer vmkx via listing vmkernel appelled VMkernel
            run('vim-cmd hostsvc/vmotion/vnic_set vmk2')

            # AJOUT DES EQL AU DATASTORE
            #
            run('esxcli iscsi software set -e true')
            run('esxcli iscsi adapter list')
            # RECUPERATION NOM VMHBA APRES AVOIR RESCAN
            vmhba = run("esxcfg-scsidevs -a | awk ' /iscsi_vmk/ { print $1 }'")
            run('esxcli iscsi networkportal add -n vmk3 -A '+vmhba+'')
            run('esxcli iscsi networkportal add -n vmk4 -A '+vmhba+'')
            run('esxcli iscsi networkportal add -n vmk5 -A '+vmhba+'')
            run('esxcli iscsi networkportal add -n vmk6 -A '+vmhba+'')

            #
            run('esxcli iscsi adapter discovery sendtarget add -A '+vmhba+' --address=172.26.178.31')
            run('esxcli iscsi adapter discovery sendtarget auth chap set --direction=uni --authname=CLUSTERLAME-ESX --secret=chap-CLUSTERLAME-ESX --level=preferred -A '+vmhba+' --address=172.26.178.31')
            run('esxcli iscsi adapter discovery sendtarget add -A '+vmhba+' --address=172.26.178.47')
            run('esxcli iscsi adapter discovery sendtarget auth chap set --direction=uni --authname=CLUSTERLAME-ESX --secret=chap-CLUSTERLAME-ESX --level=preferred -A '+vmhba+' --address=172.26.178.47')
            run('esxcli iscsi adapter discovery sendtarget add -A '+vmhba+' --address=172.26.178.60')
            run('esxcli iscsi adapter discovery sendtarget auth chap set --direction=uni --authname=CLUSTERLAME-ESX --secret=chap-CLUSTERLAME-ESX --level=preferred -A '+vmhba+' --address=172.26.178.60')
            run('esxcli iscsi adapter discovery sendtarget add -A '+vmhba+' --address=172.26.178.6')
            run('esxcli iscsi adapter discovery sendtarget auth chap set --direction=uni --authname=CLUSTERLAME-ESX --secret=chap-CLUSTERLAME-ESX --level=preferred -A '+vmhba+' --address=172.26.178.6')

            #
            run('esxcli storage core adapter rescan --adapter='+vmhba+'')

            #
            run('esxcli iscsi adapter discovery sendtarget add -A '+vmhba+' --address=172.26.178.158')
            #run('esxcli iscsi adapter discovery sendtarget add -A '+vmhba+' --address=172.26.178.159')
            run('esxcli iscsi adapter discovery sendtarget add -A '+vmhba+' --address=172.26.178.183')
            #run('esxcli iscsi adapter discovery sendtarget add -A '+vmhba+' --address=172.26.178.184')
            run('esxcli iscsi adapter discovery sendtarget add -A '+vmhba+' --address=172.26.178.206')
            run('vmhba iscsi adapter discovery sendtarget add -A '+vmhba+' --address=172.26.178.219')
            run('esxcli iscsi adapter discovery sendtarget auth chap set --direction=uni --authname=EQL5-ESX --secret=chap-EQL5-ESX --level=preferred -A '+vmhba+' --address=172.26.178.158')
            #run('esxcli iscsi adapter discovery sendtarget auth chap set --direction=uni --authname=EQL6-ESX --secret=chap-EQL6-ESX --level=preferred -A '+vmhba+' --address=172.26.178.159')
            run('esxcli iscsi adapter discovery sendtarget auth chap set --direction=uni --authname=EQL7-ESX --secret=chap-EQL7-ESX --level=preferred -A '+vmhba+' --address=172.26.178.183')
            #run('esxcli iscsi adapter discovery sendtarget auth chap set --direction=uni --authname=EQL8-ESX --secret=chap-EQL8-ESX --level=preferred -A '+vmhba+' --address=172.26.178.184')
            run('esxcli iscsi adapter discovery sendtarget auth chap set --direction=uni --authname=EQL9-ESX --secret=chap-EQL9-ESX --level=preferred -A '+vmhba+' --address=172.26.178.206')
            run('esxcli iscsi adapter discovery sendtarget auth chap set --direction=uni --authname=EQL10-ESX --secret=chap-EQL10-ESX --level=preferred -A '+vmhba+' --address=172.26.178.219')
            #
            run('esxcli storage core adapter rescan --adapter='+esxcli+'')

