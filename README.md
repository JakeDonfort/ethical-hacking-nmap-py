<h1 align="center">Nmap in Python</h1>

<h2>Description</h2>

<p>
    This is a simple Python project aimed at simulating the <strong>Nmap</strong> tool with support for <strong>proxy</strong> and <strong>threading</strong>. It's a port scanner that uses the <strong>TCP protocol</strong> and is compatible with both <strong>IPV4</strong> and <strong>IPV6 addresses</strong>. The project displays if the port is open, the server version if available, and other relevant information. It's a straightforward and user-friendly project for those looking to learn more about networks and information security
</p>

<h2>Compatible and Tested</h2>

<ul>

  <li>Kali Linux</li>

  <li>Termux (Android)</li>

</ul>

<h2>How to install nmap.py in Termux</h2>

<h4>Configuring the Environment</h4>

```
termux-setup-storage
```
```
apt-get -y update && apt-get upgrade -y
```
```
apt-get  install python3 -y
```
```
apt-get install python-pip -y
```
```
apt-get install git -y
```

<h4>Installing nmap.py</h4>

```
git clone https://github.com/JakeDonfort/ethical-hacking-nmap-py/
```
```
cd ethical-hacking-nmap-py
```
```
pip3 install -r REQUIREMENTS.txt
```
```
python3 nmap.py --help
```

<div align="center">

![nmap.py example image](https://github.com/JakeDonfort/ethical-hacking-nmap-py/blob/main/src/assets/example2.jpg)
![nmap.py example image](https://github.com/JakeDonfort/ethical-hacking-nmap-py/blob/main/src/assets/example3.jpg)

</div>

<h2>Note on the use of port scanning</h2>

<p>
The use of port scanning can be useful for network and system administration, but it can also be used for malicious purposes. A port scan is a technique used to determine which ports on a system are open and available for connection. This can be useful for a network administrator who wants to check for vulnerabilities in their network, but it can also be used by attackers to discover entry points for an attack.
</p>

<p>
For this reason, the use of port scanning is considered illegal in many countries, unless it is performed with explicit permission from the owner or administrator of the system or network being scanned. Additionally, some Internet Service Provider (ISP) companies prohibit the use of port scanning on their network.
</p>

<p>
In summary, the use of port scanning can be useful for legitimate purposes, but it can also be dangerous if used inappropriately or without authorization. It is important to use it with caution and consider the ethical and legal implications before using it.
</p>

