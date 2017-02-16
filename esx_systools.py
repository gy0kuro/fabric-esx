#
##
# Script de configuration ESXi / tgr 04122014.1 (v1) / ddm 09.04.2015.4
##
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

env.roledefs['esx2test'] = ['all']

#env.roledefs['clusterpizza'] = ['boba','athos','idefix','obelix','jango']
#env.roledefs['clusterlamewestmere'] = ['atlanta, detroit, trinity']
#env.roledefs['clusterlamesandyblade1'] = ['chicago','neo','niobe']
#env.roledefs['clusterlamesandyblade1'] = ['boston','dallas','denver']
env.roledefs['all'] = ['boba','athos','idefix','obelix','jango','atlanta','detroit','trinity','chicago','neo','niobe','boston','dallas','denver']

env.user="root"
env.skip_bad_hosts=True
env.timeout=30
env.shell = "/bin/sh -c"


#
# FONCTION DE COLLECTE DE DONNEES
# OK pour RHEL a tester pour Debian likes

csvio='portgroup.nfo'

@roles('all')

def grabinfos():

        with settings(
        #hide('warnings', 'running', 'stderr','stdout'),
        hide('stderr','stdout'),
        warn_only=True
        ):

                #target = open(csvio, 'a')

                run('esxcli system hostname get |grep "Host Name:"')
                run('esxcli network vswitch standard portgroup list |grep -i racine')


                #target.write("\n")
                #target.write(hostname+"\n"+portgroup_list+"\n")

        #target.close()



#
# AJOUT PORTGROUP SUR VSWITCH
#

@roles()

def esx_porgroup_install():

        with settings(
        hide('stderr','stdout'),
        warn_only=True
        ):

             #esxcli network vswitch standard portgroup add -p WebEtabPriv -v vSwitch1
             #esxcli network vswitch standard portgroup set --vlan-id=236 --portgroup-name="WebEtabPriv"

             #nomvswitch = prompt('Saisir un nom du vSwitch (case sensitive) : ')
             #nomportgroup = prompt('Saisir un nom du portgroup : ')

             #run('esxcli network vswitch standard portgroup add -p '+nomporgroup+' -v '+nomvswitch+'')
             #run('esxcli network vswitch standard portgroup set --vlan-id=11 --portgroup-name="'+nomporgroup+'"')

            run('esxcli network vswitch standard portgroup add -p network_mgt -v vSwitch0')
            run('esxcli network vswitch standard portgroup set --vlan-id=11 --portgroup-name="network_mgt"')


#
# GRAB INFOS SUR HOTES ESXi
#

#@roles('all')

#def esxgrabinfos():

 #       with settings(
   #     hide('running'),
        #warn_only=True
    #    ):



            # verification protocole utilise pour SSH
            #run('cat /etc/ssh/sshd_config |grep Protocol')

            # 
            #run('esxcli hardware platform get')

            # conf hostname
            #run('esxcli system hostname get')

            # vmnic
            #run('for i in $(seq 0 7); do esxcli network nic stats get -n vmnic$i |grep -B3 "Bytes"; done')

            # vmk et portgroups
            #run('esxcli network ip interface list |grep -A4 vmk')

            # liste LUNS
            #run('esxcli storage core device list |grep "Display Name:"')

            # liste adapters ISCSI
            #run('esxcli iscsi adapter target list')

            #  listing des VMs
            #run('esxcli vm process list')

###
#     FIX
###
#
#
#@roles()
#
#def fixdeploy():
#
        #with settings(
        #hide('stderr','stdout'),
        #warn_only=True
        #):
#
            #run ('vim-cmd solo/registervm /vmfs/volumes/519b9360-1f8b3e02-0ef0-90b11c2feb6c/rec-pp-etab/rec-pp-etab.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/51c422da-413a4ea8-a8e8-90b11c2feb6c/rec-superviseur/rec-superviseur.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/5194b8ba-afec78bc-b83a-90b11c2feb6c/rec-pp-cdt/rec-pp-cdt.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/5194b8ba-afec78bc-b83a-90b11c2feb6c/rec-pp-proxy/rec-pp-proxy.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/5194b8ba-afec78bc-b83a-90b11c2feb6c/rec-transpmf/rec-transpmf.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/51c422da-413a4ea8-a8e8-90b11c2feb6c/rec-pp-deb6-panel3/rec-pp-deb6-panel3.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/5194b8ba-afec78bc-b83a-90b11c2feb6c/rec-pp-willy/rec-pp-willy.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/5194b8ba-afec78bc-b83a-90b11c2feb6c/rec-owncloud-pp/rec-owncloud-pp.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/522f3285-68a5a114-9ac3-90b11c2feb6c/San80/San80.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/5194b8ba-afec78bc-b83a-90b11c2feb6c/rec-pp-spipmutu/rec-pp-spipmutu.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/5194b8ba-afec78bc-b83a-90b11c2feb6c/rec-pp-dotclearmutu/rec-pp-dotclearmutu.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/5257aeeb-cfc75140-8f5a-90b11c2feb6c/rec-pp-wordpressmutu/rec-pp-wordpressmutu.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/5257aeeb-cfc75140-8f5a-90b11c2feb6c/rec-pp-glpi/rec-pp-glpi.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/5194b8ba-afec78bc-b83a-90b11c2feb6c/rec-svrlog/rec-svrlog.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/528c8af7-baed8b24-1e84-90b11c2feb6c/rec-pp-frontal1-blogs/rec-pp-frontal1-blogs.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/5257aeeb-cfc75140-8f5a-90b11c2feb6c/rec-pp-cache/rec-pp-cache.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/528c8af7-baed8b24-1e84-90b11c2feb6c/rec-pp-reverse-proxy-glpi/rec-pp-reverse-proxy-glpi.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/5257aeeb-cfc75140-8f5a-90b11c2feb6c/rec-induschef/rec-induschef.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/5257aeeb-cfc75140-8f5a-90b11c2feb6c/rec-pp-agora/rec-pp-agora.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/5194b8ba-afec78bc-b83a-90b11c2feb6c/rec-pp-vpn/rec-pp-vpn.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/528c8af7-baed8b24-1e84-90b11c2feb6c/rec-pp-glpi-db2/rec-pp-glpi-db2.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/519b9360-1f8b3e02-0ef0-90b11c2feb6c/rec-suprvision/rec-suprvision.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/533bcdef-29b884be-10e4-90b11c2feb6c/rec-edt/rec-edt.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/51c422da-413a4ea8-a8e8-90b11c2feb6c/rec-pp-panel/rec-pp-panel.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/533bce43-7b1ba564-af11-90b11c2feb6c/vSphere Data Protection 6.0/vSphere Data Protection 6.0.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/533bcdef-29b884be-10e4-90b11c2feb6c/rec-vdrmat1/rec-vdrmat1.vmx')
            #run ('vim-cmd solo/registervm /vmfs/volumes/528c8af7-baed8b24-1e84-90b11c2feb6c/ubuntu_int_grafik/ubuntu_int_grafik.vmx')


#
#     RENOMMAGE RECURSIF VM (NOM > ARBO > FICHIERS > CONTENUS FICHIERS)
#

#@roles()

#def rename_vm():

  #      with settings(
   #     hide('stderr','stdout'),
    #    warn_only=True
    #    ):

            #    
            #oldname_vm = "" 
            #newname_vm = ""

            # RENOMMAGE DOSSIER
            #run('mv')
            # RENOMMAGE FICHIERS DE VM
            #run('vmkfstools -E '+oldname_vm+'.vmdk '+newname_vm+'.vmdk')
            # RENOMMAGE VM DANS LES FICHIERS
            #run('')
            # RENOMMAGE VM DANS LA CONF
            #run('')

            #for i in arborescence do
                  #remplacer occurence
            #with open("out.txt", "wt") as fout:
           #       with open("Stud.txt", "rt") as fin:
             #           for line in fin:
             #                 fout.write(line.replace('A', 'Orange'))

              #    nvram = "proxy4.ac-amiens.fr.nvram"
              #    displayName = "proxy4.ac-amiens.fr"
              #    extendedConfigFile = "proxy4.ac-amiens.fr.vmxf"
              #    scsi0:0.fileName = "proxy4.ac-amiens.fr.vmdk"
              #    sched.swap.derivedName = "/vmfs/volumes/52d8f7ba-88976e4c-462f-d4ae522ab936/proxy4.ac-amiens.fr/proxy4.ac-amiens.fr-ad8e201a.vswp"

            # REDEMARRAGE VM
            #run('')


#
# AJOUT DES VMWARE TOOLS
#
#     Pour centos
#     tests faire pour Ubuntu / Debian

#@roles()

#def esx_vmwaretools_install():

 #       with settings(
  #      hide('stderr','stdout'),
   #     warn_only=True
   #     ):

            # installation via yum pour centos 6.6 & ESX 5.5
            # yum -y install http://packages.vmware.com/tools/esx/5.5latest/rhel6/x86_64/vmware-tools-esx-9.4.12-1.el6.x86_64.rpm

            
            # lancement de install avec options par defaut (no)
            # vmware-config-tools.pl -d

                  # oubli ?
                  # yum -y install vmware-tools-esx-nox ??

            # exclusion des MAJ
            # yum -x 'vmware-tools*' -x 'kmod-vmware-tools*' update

            # ajout du chkconfig ?
