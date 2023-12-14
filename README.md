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

Run echo server:
```bash
python tcp_echo_server.py
```
2. proxy

Run masquerade server:
```bash
chmod +x src/masque_server.sh
./src/masque_server.sh
```
3. client

First run masquerade client:
```bash
chmod +x src/masque_client.sh
./src/masque_client.sh "$PROXY_IP_ADDR"
```
In a new terminal, change the `"$SERVER_IP_ADDR"` accordingly and run echo client:
```bash
python tcp_echo_client.py "$SERVER_IP_ADDR" "$(hostname -i)"
```

To test bit overhead of inner QUIC
Run QUIC file server and client: 
```bash
python quic_file_server.py
python quic_file_client.py
```

Application structure of the current deployment:

```
---------------CLIENT---------------              ------PROXY------             --------SERVER--------
| Client <-- TCP --> MASQUE Client | <-- QUIC --> | MASQUE Server | <-- TCP --> | Application Server |
------------------------------------              -----------------             ----------------------
```
<!-- ![](/assets/masquerade_str.drawio.png) -->
