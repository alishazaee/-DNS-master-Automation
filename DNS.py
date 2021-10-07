#!/usr/bin/python
from string import Template
import os
import subprocess

print("this might take a few seconds ... ")
os.system("yum install redhat-lsb-core -y > /dev/null 2>&1")


OS=subprocess.getoutput("cat /etc/os-release | grep ^NAME | sed -r 's/NAME=//g' | sed -r 's/\"//g'")
if OS.lower().find("ubuntu") != -1 :
    namedconf="/etc/bind/named.conf.local"
    allzones="/var/cache/bind/"
    state=subprocess.getoutput("dpkg -l | grep bind")
    if state != 0 :
       print("Installing Bind Package ... wait few seconds")
       os.system("apt install bind9 -y > /dev/null 2>&1")
  

elif OS.lower().find("centos") != -1  :
    namedconf="/etc/named.conf"
    allzones="/var/named/"
    state=subprocess.getoutput("rpm -qa | grep bind")
    if state != 0  :
       print("Installing Bind Package ... wait few seconds")
       os.system("yum install bind -y > /dev/null 2>&1")
	


print("insert the Domain name : (example : alishazaee.ir) ") 
domain=input()
print("insert Zone file name : (example ali.ir.master ) ")
zonefile=input()
print("Master DNS server IP address : ")
dnsip=input()
print("webserver Address : (example : 183.168.10.50) ")
www=input()
print("mail server: (example : 183.168.10.50) ")
mail=input()

os.system("dnssec-keygen -a HMAC-SHA256 -b 256 -n HOST -r /dev/urandom slaves > /dev/null ")
allowslave=subprocess.getoutput("cat Kslaves.*.key | awk {'print $7'}")
os.system("rm -rf Ks*")

zone={
        'domain' : domain,
        'type'   : 'master',
        'file' : zonefile+'.db',
        'allow' :  allowslave
        }

soa={
        'domain' : domain+'.',
        'ns'     : "ns1."+domain+'.',
        'dnsip'  : dnsip,
        'www'    : www,
        'TTL'    : "$TTL",
        'mail'   : mail
        }

with open ('zone' , 'r') as f:
    src = Template(f.read())
    result=src.substitute(zone)
    with open(namedconf, "a") as file_object:
                file_object.write(result)


with open ('sample.db' , 'r') as f:
    src = Template(f.read())
    result=src.substitute(soa)
    with open(("{file1}{file2}.db".format(file1=allzones,file2=zonefile)), "w") as file_object:
                file_object.write(result)

os.system("systemctl restart named")
