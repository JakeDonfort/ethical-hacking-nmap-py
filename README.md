<h1 align="center">Nmap in Python</h1>

<h2>Description</h2>

<p>
    This is a simple Python project aimed at simulating the Nmap tool with support for proxy and threading. It's a port scanner that uses the TCP protocol and is compatible with both IPV4 and IPV6 addresses. The project displays if the port is open, the server version if available, and other relevant information. It's a straightforward and user-friendly project for those looking to learn more about networks and information security
</p>

<h2>Compatible and Tested</h2>

<ul>

  <li>Kali Linux</li>

  <li>Termux (Android)</li>

</ul>

![nmap example gif](https://github.com/JakeDonfort/ethical-hacking-nmap-py/blob/main/nmap_example.gif)

<h2>How to install nmap.py in Termux</h2>

<p>Configuring the Environment</p>


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

<p>Installing nmap.py</p>

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
