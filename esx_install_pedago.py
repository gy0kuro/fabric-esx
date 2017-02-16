# ! /usr/bin/python
# coding: utf8
##
# Script de configuration ESXi PEDAGO / tgr 04122014.1 (v1) / ddm 09.04.2015.4
##
# Documentation :
#
#     https://github.com/fabric/fabric/issues/369     execution specifique hors /bin/bash
#     https://pubs.vmware.com/vsphere-50/index.jsp#com.vmware.vcli.ref.doc_50/esxcli_network.html
#     https://pubs.vmware.com/vsphere-50/index.jsp?topic=%2Fcom.vmware.vcli.ref.doc_50%2Fesxcli_network.html
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
import unicodedata

env.roledefs['esx2install'] = ['194.254.103.21']

env.user="root"
env.skip_bad_hosts=True
env.timeout=30
env.shell = "/bin/sh -c"

#
# INSTALLATION ESXi
# prerequs  :
#   - avoir installed ESXi
#
#   GW  :   194.254.103.97
#   DNS :   194.199.46.5
#   DNS :   194.199.46.6
#

@roles('esx2install')

def esxfirewallon():

        with settings(
        #hide('stderr', 'stdout'),
        abort_on_prompts=False
        ):

            # FIREWALL
            # 
            # http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=2008226
            #
            # desactivation temporaire du FW pour ne pas scier la branche sur laquelle on est assise

            run('esxcli network firewall set --enabled false')
            #
            # CHAMPS FIREWALL TRUE
            run('esxcli network firewall ruleset set -r vSphereClient -a true')
            run('esxcli network firewall ruleset set --allowed-all false -r vSphereClient')
            run('esxcli network firewall ruleset allowedip add -r vSphereClient -i 194.254.103.19')
            #
            run('esxcli network firewall ruleset set -r webAccess -a true')
            run('esxcli network firewall ruleset set --allowed-all false -r webAccess')
            run('esxcli network firewall ruleset allowedip add -r webAccess -i 194.254.103.19')
            #
            run('esxcli network firewall ruleset set -r sshServer -a true')
            run('esxcli network firewall ruleset set --allowed-all false -r sshServer')
            run('esxcli network firewall ruleset allowedip add -r sshServer -i 194.199.47.66')
            run('esxcli network firewall ruleset allowedip add -r sshServer -i 194.254.103.19')
            run('esxcli network firewall ruleset allowedip add -r sshServer -i 194.254.103.20')
            run('esxcli network firewall ruleset allowedip add -r sshServer -i 194.254.103.21')
            run('esxcli network firewall ruleset allowedip add -r sshServer -i 194.254.103.22')
            #
            run('esxcli network firewall ruleset set -r vMotion -a true')
            run('esxcli network firewall ruleset set --allowed-all false -r vMotion')
            run('esxcli network firewall ruleset allowedip add -r vMotion -i 194.254.103.19')
            run('esxcli network firewall ruleset allowedip add -r vMotion -i 194.254.103.20')
            run('esxcli network firewall ruleset allowedip add -r vMotion -i 194.254.103.21')
            run('esxcli network firewall ruleset allowedip add -r vMotion -i 194.254.103.22')
            #
            run('esxcli network firewall ruleset set -r iSCSI -a true')
            run('esxcli network firewall ruleset set --allowed-all false -r iSCSI')
            # md1200
            run('esxcli network firewall ruleset allowedip add -r iSCSI -i 192.168.130.101')
            run('esxcli network firewall ruleset allowedip add -r iSCSI -i 192.168.131.101')
            run('esxcli network firewall ruleset allowedip add -r iSCSI -i 192.168.132.101')
            run('esxcli network firewall ruleset allowedip add -r iSCSI -i 192.168.133.101')
            run('esxcli network firewall ruleset allowedip add -r iSCSI -i 192.168.130.102')
            run('esxcli network firewall ruleset allowedip add -r iSCSI -i 192.168.131.102')
            run('esxcli network firewall ruleset allowedip add -r iSCSI -i 192.168.132.102')
            run('esxcli network firewall ruleset allowedip add -r iSCSI -i 192.168.133.102')
            # eql
            run('esxcli network firewall ruleset allowedip add -r iSCSI -i 172.26.178.206')

            run('esxcli network firewall ruleset set -r dns -a true')
            run('esxcli network firewall ruleset set -r ntpClient -a true')
            run('esxcli network firewall ruleset set -r CIMHttpServer -a true')
            run('esxcli network firewall ruleset set -r CIMHttpsServer -a true')
            run('esxcli network firewall ruleset set -r CIMSLP -a true')
            run('esxcli network firewall ruleset set -r vpxHeartbeats -a true')
            run('esxcli network firewall ruleset set -r faultTolerance -a true')
            run('esxcli network firewall ruleset set -r NFC -a true')
            run('esxcli network firewall ruleset set -r HBR -a true')
            run('esxcli network firewall ruleset set -r rdt -a true')
            run('esxcli network firewall ruleset set -r dynamicruleset -a true')
            # CHAMPS FIREWALL FALSE
            run('esxcli network firewall ruleset set -r snmp -a false')
            run('esxcli network firewall ruleset set -r updateManager -a false')
            run('esxcli network firewall ruleset set -r activeDirectoryAll -a false')
            run('esxcli network firewall ruleset set -r ftpClient -a false')
            run('esxcli network firewall ruleset set -r httpClient -a false')
            run('esxcli network firewall ruleset set -r gdbserver -a false')
            run('esxcli network firewall ruleset set -r DVFilter -a false')
            run('esxcli network firewall ruleset set -r DHCPv6 -a false')
            run('esxcli network firewall ruleset set -r DVSSync -a false')
            run('esxcli network firewall ruleset set -r syslog -a false')
            run('esxcli network firewall ruleset set -r IKED -a false')
            run('esxcli network firewall ruleset set -r WOL -a false')
            run('esxcli network firewall ruleset set -r vSPC -a false')
            run('esxcli network firewall ruleset set -r remoteSerialPort -a false')
            run('esxcli network firewall ruleset set -r vprobeServer -a false')
            run('esxcli network firewall ruleset set -r sshClient -a false')
            run('esxcli network firewall ruleset set -r nfsClient -a false')
            run('esxcli network firewall ruleset set -r dhcp -a false')
            #
            # reactivation du FW puis (useless?)refresh
            run('esxcli network firewall set --enabled true')
            run('esxcli network firewall refresh')



@roles('esx2install')

def esxfirewalloff():

        with settings(
        #hide('stderr', 'stdout'),
        abort_on_prompts=False
        ):

            run('esxcli network firewall set --enabled false')
            run('esxcli network firewall ruleset allowedip remove -r vSphereClient -i 194.254.103.19')
            run('esxcli network firewall ruleset allowedip remove -r vSphereClient -i 194.199.47.66')
            run('esxcli network firewall ruleset set -r vSphereClient -a false')
            run('esxcli network firewall ruleset set --allowed-all true -r vSphereClient')

            run('esxcli network firewall ruleset allowedip remove -r webAccess -i 194.254.103.19')
            run('esxcli network firewall ruleset allowedip remove -r webAccess -i 194.199.47.66')
            run('esxcli network firewall ruleset set -r webAccess -a false')
            run('esxcli network firewall ruleset set --allowed-all true -r webAccess')

            run('esxcli network firewall ruleset allowedip remove -r sshServer -i 194.199.47.66')
            run('esxcli network firewall ruleset allowedip remove -r sshServer -i 194.254.103.19')
            run('esxcli network firewall ruleset allowedip remove -r sshServer -i 194.254.103.20')
            run('esxcli network firewall ruleset allowedip remove -r sshServer -i 194.254.103.21')
            run('esxcli network firewall ruleset allowedip remove -r sshServer -i 194.254.103.22')
            run('esxcli network firewall ruleset set -r sshServer -a false')
            run('esxcli network firewall ruleset set --allowed-all true -r sshServer')

            run('esxcli network firewall ruleset allowedip remove -r vMotion -i 194.254.103.19')
            run('esxcli network firewall ruleset allowedip remove -r vMotion -i 194.254.103.20')
            run('esxcli network firewall ruleset allowedip remove -r vMotion -i 194.254.103.21')
            run('esxcli network firewall ruleset allowedip remove -r vMotion -i 194.254.103.22')
            run('esxcli network firewall ruleset set -r vMotion -a false')
            run('esxcli network firewall ruleset set --allowed-all true -r vMotion')

            run('esxcli network firewall ruleset allowedip remove -r iSCSI -i 192.168.130.101')
            run('esxcli network firewall ruleset allowedip remove -r iSCSI -i 192.168.131.101')
            run('esxcli network firewall ruleset allowedip remove -r iSCSI -i 192.168.132.101')
            run('esxcli network firewall ruleset allowedip remove -r iSCSI -i 192.168.133.101')
            run('esxcli network firewall ruleset allowedip remove -r iSCSI -i 192.168.130.102')
            run('esxcli network firewall ruleset allowedip remove -r iSCSI -i 192.168.131.102')
            run('esxcli network firewall ruleset allowedip remove -r iSCSI -i 192.168.132.102')
            run('esxcli network firewall ruleset allowedip remove -r iSCSI -i 192.168.133.102')
            run('esxcli network firewall ruleset allowedip remove -r iSCSI -i 172.26.178.206')
            run('esxcli network firewall ruleset set -r iSCSI -a false')
            run('esxcli network firewall ruleset set --allowed-all true -r iSCSI')

            run('esxcli network firewall ruleset set -r dns -a true')
            run('esxcli network firewall ruleset set -r ntpClient -a true')
            run('esxcli network firewall ruleset set -r CIMHttpServer -a true')
            run('esxcli network firewall ruleset set -r CIMHttpsServer -a true')
            run('esxcli network firewall ruleset set -r CIMSLP -a true')
            run('esxcli network firewall ruleset set -r vpxHeartbeats -a true')
            run('esxcli network firewall ruleset set -r faultTolerance -a true')
            run('esxcli network firewall ruleset set -r NFC -a true')
            run('esxcli network firewall ruleset set -r HBR -a true')
            run('esxcli network firewall ruleset set -r rdt -a true')
            run('esxcli network firewall ruleset set -r dynamicruleset -a true')
            run('esxcli network firewall ruleset set -r snmp -a false')
            run('esxcli network firewall ruleset set -r updateManager -a false')
            run('esxcli network firewall ruleset set -r activeDirectoryAll -a false')
            run('esxcli network firewall ruleset set -r ftpClient -a false')
            run('esxcli network firewall ruleset set -r httpClient -a false')
            run('esxcli network firewall ruleset set -r gdbserver -a false')
            run('esxcli network firewall ruleset set -r DVFilter -a false')
            run('esxcli network firewall ruleset set -r DHCPv6 -a false')
            run('esxcli network firewall ruleset set -r DVSSync -a false')
            run('esxcli network firewall ruleset set -r syslog -a false')
            run('esxcli network firewall ruleset set -r IKED -a false')
            run('esxcli network firewall ruleset set -r WOL -a false')
            run('esxcli network firewall ruleset set -r vSPC -a false')
            run('esxcli network firewall ruleset set -r remoteSerialPort -a false')
            run('esxcli network firewall ruleset set -r vprobeServer -a false')
            run('esxcli network firewall ruleset set -r sshClient -a false')
            run('esxcli network firewall ruleset set -r nfsClient -a false')
            run('esxcli network firewall ruleset set -r dhcp -a false')
            run('esxcli network firewall set --enabled true')
            run('esxcli network firewall refresh')


@roles('esx2install')

def esx_supvswitch():

        with settings(
        #hide('stderr', 'stdout'),
        abort_on_prompts=False
        ):
            vmhba = run("esxcfg-scsidevs -a | awk ' /iscsi_vmk/ { print $1 }'")

            #run('esxcli network vswitch standard remove -v vSwitch5')
            run('esxcli iscsi networkportal remove -n vmk1 -A '+vmhba+'')
            run('esxcli iscsi networkportal remove -n vmk2 -A '+vmhba+'')
            run('esxcli iscsi networkportal remove -n vmk4 -A '+vmhba+'')

            run('esxcli network vswitch standard remove -v vSwitch4')
            run('esxcli network vswitch standard remove -v vSwitch3')
            run('esxcli network vswitch standard remove -v vSwitch2')
            run('esxcli network vswitch standard remove -v vSwitch1')
            run('vim-cmd hostsvc/net/portgroup_set --portgroup-name="Management Network" vSwitch0 "Reseau de management"')
            run('esxcli network vswitch standard portgroup remove -p "Zone 194.254.103.0" -v vSwitch0')


@roles('esx2install')

def esxfreshinstall():

        with settings(
        #hide('stderr', 'stdout'),
        abort_on_prompts=False
        ):

            #
            # VARIABLES A TUNER !!!!
            #
            ip_hb = '192.168.132.101'
            ip_vmotion = '194.254.103.21'
            ip_iscsi1 = '192.168.130.249'
            ip_iscsi2 = '192.168.131.249'
            ip_iscsi_migr = '172.26.178.204'
            serveurdns1 = '194.199.46.5'
            serveurdns2 = '194.199.46.6'
            serveurntp = '194.199.46.5'
            #serveurlog = ''
            #

            # sup shell warnings
            run('esxcli system settings advanced set -i 1 -o /UserVars/SuppressShellWarning')

            # prompt hostname
            #hostname = prompt('Saisir le nom d ESX (en miniscules) : ')
            hostname = 'esx3-sandbox'
            run('esxcli system hostname set --host='+hostname+'')

            # dns
            run('esxcli network ip dns server add -s '+serveurdns1+'')
            run('esxcli network ip dns server add -s '+serveurdns2+'')
            run('esxcli network ip dns search add -d "ac-amiens.fr"')

            # ntp
            run('rm /etc/ntp.conf')
            put('/home/tom/.bin/DSIN-AMS/ESX/ntp.conf','/etc/')
            run('sed -i -e "s/xxx/'+serveurntp+'/g" /etc/ntp.conf')
            run('chmod 644 /etc/ntp.conf && chmod -t /etc/ntp.conf')

            run('/sbin/chkconfig ntpd on')
            #run('/etc/init.d/ntpd stop')
            #run('/etc/init.d/ntpd start')

            # snmp
            run('esxcli system snmp set --communities public')
            run('esxcli system snmp set --enable true')

            # syslog
            # run('esxcli system syslog config set --loghost="172.30.176.6"')
            # run('esxcli system syslog reload')

            # vswitch0 : 1 portgroup 1 vmkernel
            #chaine_unicode_vswitch0 = u"Réseau de management"
            #run('esxcfg-vmknic -a -i 194.254.103.20 -n 255.255.255.0 '+chaine_unicode_vswitch0+)

            run('esxcli network vswitch standard policy failover set -a vmnic0,vmnic1 -v vSwitch0')
            run('esxcli network vswitch standard portgroup add -p "Zone 194.254.103.0" -v vSwitch0')
            run('vim-cmd hostsvc/net/portgroup_set --portgroup-name="Reseau de management" vSwitch0 "Management Network"')
            # lignes qui suivent sont useless : ip et vmk attribues a linstallation de lesx
            #run('esxcli network ip interface add -i vmk0 --portgroup-name="Reseau de management"')
            #run('esxcli network ip interface ipv4 set -i vmk0 -I '+ip_vmotion+' -N 255.255.255.0 -t static')
            run('vim-cmd hostsvc/vmotion/vnic_set vmk0')

            # VSWITCH1 : 1 vmkernel
            # ISCSI1
            #
            print(green('CONF VSWITCH1'))
            run('esxcli network vswitch standard add -v vSwitch1')
            run('esxcli network vswitch standard portgroup add -p ISCSI1 -v vSwitch1')
            # attacher vmnic
            run('esxcli network vswitch standard uplink add --uplink-name vmnic2 --vswitch-name vSwitch1')
            #
            run('esxcli network vswitch standard policy failover set -a vmnic2 -v vSwitch1')
            run('esxcli network vswitch standard set -m 9000 -v vSwitch1')
            run('esxcli network ip interface add -i vmk1 --portgroup-name="ISCSI1"')
            run('esxcli network ip interface ipv4 set -i vmk1 -I '+ip_iscsi1+' -N 255.255.255.0 -t static')
            
            # VSWITCH2 : 1 vmkernel
            # ISCSI2
            #
            print(green('CONF VSWITCH2'))
            run('esxcli network vswitch standard add -v vSwitch2')
            run('esxcli network vswitch standard portgroup add -p ISCSI2 -v vSwitch2')
            # attacher vmnic
            run('esxcli network vswitch standard uplink add --uplink-name vmnic3 --vswitch-name vSwitch2')
            #
            run('esxcli network vswitch standard policy failover set -a vmnic3 -v vSwitch2')
            run('esxcli network vswitch standard set -m 9000 -v vSwitch2')
            run('esxcli network ip interface add -i vmk2 --portgroup-name="ISCSI2"')
            run('esxcli network ip interface ipv4 set -i vmk2 -I '+ip_iscsi2+' -N 255.255.255.0 -t static')

            # VSWITCH3 : 1 portgroup
            #
            print(green('CONF VSWITCH3'))
            run('esxcli network vswitch standard add -v vSwitch3')
            # attacher vmnic
            run('esxcli network vswitch standard uplink add --uplink-name vmnic4 --vswitch-name vSwitch3')
            run('esxcli network vswitch standard uplink add --uplink-name vmnic5 --vswitch-name vSwitch3')
            #
            run('esxcli network vswitch standard policy failover set -a vmnic4,vmnic5 -v vSwitch3')
            run('esxcli network vswitch standard portgroup add --portgroup-name="Zone 192.168.141.0/24" -v vSwitch3')

            # VSWITCH4 : 1 vmkernel
            #
            print(green('CONF VSWITCH4'))
            run('esxcli network vswitch standard add -v vSwitch4')
            run('esxcfg-vswitch -A VMkernel-Iscsi-Migration vSwitch4')
            # attacher vmnic
            run('esxcli network vswitch standard uplink add --uplink-name vmnic7 --vswitch-name vSwitch4')
            run('esxcli network vswitch standard policy failover set -a vmnic7 -v vSwitch4')
            run('esxcli network vswitch standard set -m 9000 -v vSwitch4')
            run('esxcli network ip interface add -i vmk4 --portgroup-name="VMkernel-Iscsi-Migration"')
            run('esxcli network ip interface ipv4 set -i vmk4 -I '+ip_iscsi_migr+' -N 255.255.255.0 -t static')

            # Passage des MTU en jumbo frames
            run('esxcli network ip interface set -m 9000 -i vmk1')
            run('esxcli network ip interface set -m 9000 -i vmk2')
            run('esxcli network ip interface set -m 9000 -i vmk4')
            
            # VSWITCH5 : 1 portgroup
            #
            print(green('CONF VSWITCH5'))
            run('esxcli network vswitch standard add -v vSwitch5')
            run('esxcli network vswitch standard uplink add --uplink-name vmnic6 --vswitch-name vSwitch5')
            run('esxcli network vswitch standard policy failover set -a vmnic6 -v vSwitch5')
            run('esxcli network vswitch standard portgroup add --portgroup-name="Zone 194.254.103.192/26" -v vSwitch5')

            # AJOUT DES EQL AU DATASTORE
            # RECUPERATION NOM VMHBA
            #
            #
            print(green('INTERCONNEXION SAN'))

            # ajout adaptateur software iscsi

            run('esxcli iscsi software set -e true')
            run('esxcli iscsi adapter list')

            vmhba = run("esxcfg-scsidevs -a | awk ' /iscsi_vmk/ { print $1 }'")

            run('esxcli iscsi adapter discovery rediscover -A '+vmhba+'')
            run('esxcli storage core adapter rescan --adapter='+vmhba+'')

            #

            run('esxcli iscsi networkportal add -n vmk1 -A '+vmhba+'')
            run('esxcli iscsi networkportal add -n vmk2 -A '+vmhba+'')
            run('esxcli iscsi networkportal add -n vmk4 -A '+vmhba+'')
            run('esxcli iscsi adapter discovery sendtarget add -A '+vmhba+' --address=192.168.130.101')
            #scan MD3200i
            run('esxcli storage nmp satp set --default-psp VMW_PSP_RR --satp VMW_SATP_ALUA')


            run('esxcli iscsi adapter discovery sendtarget auth chap set --direction=uni --authname=EQL9-ESX --secret=chap-EQL9-ESX --level=preferred -A '+vmhba+' --address=172.26.178.206')

            run('esxcli iscsi adapter discovery rediscover')
            run('esxcli storage core adapter rescan --adapter='+vmhba+'')

            run('esxcli storage nmp satp set --default-psp VMW_PSP_RR --satp VMW_SATP_EQL')


            # AJOUTER LE MODE CIRCULAR AUX DIFFERENTS LUNS MONTES
            #run('esxcli storage nmp device set --device naa.690b11c00008dd32000003e051934e7a --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.690b11c00008dd32000006f651c3b854 --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.690b11c00008dd55000005f7525720f2 --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.690b11c00008dd5500000600528cddf4 --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.6782bcb0006f83fb00000aa152e1d72b --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.690b11c00008dd550000062852e2ba45 --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.6782bcb0006f83fb00000aa252e1f4ae --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.690b11c00008dd55000003dc519be7fe --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.690b11c00008dd5500000578522f7edd --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.690b11c00008dd55000005795240804e --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.690b11c00008dd55000005b85245ff10 --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.690b11c00008dd55000005fa527d2620 --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.690b11c00008dd55000005fb527d2636 --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.690b11c00008dd55000005fc527d2647 --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.690b11c00008dd55000005fd527d265e --psp VMW_PSP_RR')
            #run('esxcli storage nmp device set --device naa.690b11c00008dd55000006e9534461d1 --psp VMW_PSP_RR')
