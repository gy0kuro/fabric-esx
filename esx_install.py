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
# fab <fonction> (-P -z <nombre instances en parallele> - option P seule conseillee) -f <script>.py
#
#

import fabric.contrib.files
import os.path
from fabric.api import *
#from fabric.contrib.files import append
from fabric.colors import *
import commands

env.roledefs['esx2install'] = ['YOUR IP OR FQDN']

env.user="root"
env.skip_bad_hosts=False
env.timeout=30
env.shell = "/bin/sh -c"


# ROLE AJOUT VLAN

@roles('')

def ajout_vlan():

      with settings(
      #hide('stderr', 'stdout'),
      abort_on_prompts=False
      ):

            run('esxcli network vswitch standard portgroup add -p PORTGROUP NAME -v vSwitch0 && esxcli network vswitch standard portgroup set --vlan-id=VLAN ID --portgroup-name="PORTGROUP NAME"')
            run('esxcli network vswitch standard portgroup set --vlan-id=VLAN ID --portgroup-name="PORTGROUP NAME"')
            run('esxcli network vswitch standard portgroup list | grep vSwitch0 | grep VLAN ID')


# ROLE INSTALLATION ESXi
# prerequis  :
#   - avoir installed ESXi
#   - avoir modified le vSwitch0 en vSwitch1 dans /etc/vmware/esx.cfg


@roles('esx2install')

def esxfreshinstall():

        with settings(
        #hide('stderr', 'stdout'),
        abort_on_prompts=False
        ):


            # VARIABLES A TUNER

            ip_hb = 'YOUR IP ADDRESS'
            ip_vmotion = 'YOUR IP ADDRESS'

            ip_iscsi1 = 'YOUR IP ADDRESS'
            ip_iscsi2 = 'YOUR IP ADDRESS'
            ip_iscsi3 = 'YOUR IP ADDRESS'
            ip_iscsi4 = 'YOUR IP ADDRESS'

            serveurdns1 = 'YOUR IP ADDRESS'
            serveurdns2 = 'YOUR IP ADDRESS'
            serveurntp = 'YOUR IP ADDRESS'
            serveurlog = 'YOUR IP ADDRESS'

            # SUPPRESSION DES SHELLS WARNINGS
            run('esxcli system settings advanced set -i 1 -o /UserVars/SuppressShellWarning')

            # PROMPT DU NOM DE L'ESX
            hostname = prompt('Saisir le nom d ESX (en miniscules) : ')

            # REGLAGE HOSTNAME
            run('esxcli system hostname set --host='+hostname+'')

            # REGLAGE DNS
            run('esxcli network ip dns server add -s '+serveurdns1+'')
            run('esxcli network ip dns server add -s '+serveurdns2+'')
            run('esxcli network ip dns search add -d "YOUR DOMAIN SEARCH"')

            # CONFIG NTP (a fixer - envoyer un fichier deja formate)
            run('rm /etc/ntp.conf')
            put('/home/tom/.bin/DSIN-AMS/ESX/ntp.conf','/etc/')
            run('sed -i -e "s/xxx/'+serveurntp+'/g" /etc/ntp.conf')
            run('chmod 644 /etc/ntp.conf && chmod -t /etc/ntp.conf')
            run('/sbin/chkconfig ntpd on')

            # CONFIG SNMP
            run('esxcli system snmp set --communities public')
            run('esxcli system snmp set --enable true')

            # CONFIG SYSLOG
            run('esxcli system syslog config set --loghost="'+serveurlog+'"')
            run('esxcli system syslog reload')

            # CONFIG FIREWALL
            run('esxcli network firewall ruleset set --ruleset-id=syslog --enabled=true')
            run('esxcli network firewall refresh')

            # AJOUT VSWITCH0
            run('esxcli network vswitch standard add -v vSwitch0')

            # ATTRIBUTION VMNIC AU SWITCH1
            #run('esxcli network vswitch standard uplink add -u vmnic2 -v vSwitch1')
            #run('esxcli network vswitch standard uplink add -u vmnic3 -v vSwitch1')
            run('esxcli network vswitch standard policy failover set -a vmnic2,vmnic3 -v vSwitch1')

            # ATTRIBUTION VMNIC AU SWITCH0
            run('esxcli network vswitch standard uplink add -u vmnic0 -v vSwitch0')
            run('esxcli network vswitch standard uplink add -u vmnic1 -v vSwitch0')
            run('esxcli network vswitch standard policy failover set -a vmnic0,vmnic1 -v vSwitch0')

            # DESACTIVATION DU FCOE SUR LES INTERFACES
            run('esxcli fcoe nic disable -n=vmnic0')
            run('esxcli fcoe nic disable -n=vmnic1')
            run('esxcli fcoe nic disable -n=vmnic2')
            run('esxcli fcoe nic disable -n=vmnic3')

            # AJOUT DES PORTGROUPS
            run('esxcli network vswitch standard portgroup add -p YOUR-VSWITCH-NAME -v vSwitch1')
            # ...

            # CONFIG VLAN-ID POUR TOUS LES PORTGROUPS AJOUTES
            run('esxcli network vswitch standard portgroup set --vlan-id=1 --portgroup-name="YOUR-VSWITCH-NAME"')


            # DEFINITION DU TYPE DE MULTIPATH - NMP : Native Multipathing Plugin - SATP : Storage Array Type Plugin - VMW_SATP_EQL : SATP pour Dell EqualLogic iSCSI
            run('esxcli storage nmp satp set --default-psp=VMW_PSP_RR --satp=VMW_SATP_EQL')

            # REGLAGE MTU JUMBO VSWITCH1 (anciennement esxcfg-vswitch --mtu=9000 ${VS:-vSwitch1})
            run('esxcli network vswitch standard set -m 9000 -v vSwitch1')

            # REGLAGE AUTRE VSWITCH1 (ancienncement esxcfg-vswitch --set-cdp both ${VS:-vSwitch1})
            run('esxcli network vswitch standard set -c both -v vSwitch1')

            # HB ISCSI
            run('esxcfg-vmknic -a -i '+ip_hb+' -n 255.255.255.0 --mtu=9000 VMkernel-iscsi-heartbeat')
            run('esxcli network vswitch standard portgroup set --portgroup-name=VMkernel-iscsi-heartbeat --vlan-id=78')

            # VMOTION
            run('esxcfg-vmknic -a -i '+ip_vmotion+' -n 255.255.255.224 VMkernel')
            run('esxcli network vswitch standard portgroup set --portgroup-name=VMkernel --vlan-id=YOUR-VLAN-ID')

            # AJOUT ISCSI1 AU SWITCH1
            run('esxcfg-vswitch -A iSCSI-1 vSwitch1')
            run('esxcfg-vmknic -a -i '+ip_iscsi1+' -n 255.255.255.0 -m 9000 iSCSI-1')
            run('esxcli network vswitch standard portgroup set --portgroup-name=iSCSI-1 --vlan-id=YOUR-VLAN-ID')
            run('esxcfg-vswitch -p iSCSI-1 -N vmnic3 vSwitch1')
            # ...

            # VOIR OU LES AJOUTER
            
            #esxcli network vswitch standard portgroup policy failover set --active-uplinks=vmnic2 --portgroup-name="iSCSI-1"

            # RECUPERATION VMK VIA LISTING VMKERNEL
            run('vim-cmd hostsvc/vmotion/vnic_set vmk2')

            # AJOUT DES EQL AU DATASTORE
            run('esxcli iscsi software set -e true')
            run('esxcli iscsi adapter list')

            # RECUPERATION NOM VMHBA APRES AVOIR RESCAN
            vmhba = run("esxcfg-scsidevs -a | awk ' /iscsi_vmk/ { print $1 }'")
            run('esxcli iscsi networkportal add -n vmk3 -A '+vmhba+'')
            run('esxcli iscsi networkportal add -n vmk4 -A '+vmhba+'')
            run('esxcli iscsi networkportal add -n vmk5 -A '+vmhba+'')
            run('esxcli iscsi networkportal add -n vmk6 -A '+vmhba+'')

            # AJOUT EQLx
            run('esxcli iscsi adapter discovery sendtarget add -A '+vmhba+' --address=YOURIPADDRESS')
            run('esxcli iscsi adapter discovery sendtarget auth chap set --direction=uni --authname=AUTHNAME --secret=ITSASECRET --level=preferred -A '+vmhba+' --address=YOURIPADDRESS')

            # RESCAN DE LA CHAINE ISCSI
            run('esxcli storage core adapter rescan --adapter='+esxcli+'')

