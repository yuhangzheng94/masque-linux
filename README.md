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
python main.py server "$(hostname -i)"
```
2. proxy
```bash
python main.py proxy [SERVER_IP_ADDR] "$(hostname -i)"
```
3. client
```bash
python main.py client [SERVER_IP_ADDR] [PROXY_IP_ADDR]
```

Application structure of the current deployment:
![](/assets/masquerade_str.drawio.png)
