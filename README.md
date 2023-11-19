### MASQUERADE

This repository provides a compiled version of @jromwu's [masquarede](https://github.com/jromwu/masquerade) and a Python module for running server/proxy/client on Linux.

First clone the repository:
```bash
cd ~
sudo git clone https://github.com/dx2102/masque-linux.git
```

To run it on your local machine:
```bash
python test.py
```

To run it on separate nodes:

1. server
```bash
python main_experiment.py server
```
2. proxy
```bash
chmod +x src/proxy.sh
./src/proxy.sh
```
3. client
```bash
python main_experiment.py client [SERVER_IP_ADDR] [PROXY_IP_ADDR] "$(hostname -i)"
```

Application structure of the current deployment:

```
-----------------CLIENT-----------------               ------PROXY------             -----SERVER----
| echo client <-- TCP --> masque client | <-- QUIC --> | masque server | <-- TCP --> | echo server |
----------------------------------------               -----------------             ---------------
```
<!-- ![](/assets/masquerade_str.drawio.png) -->
