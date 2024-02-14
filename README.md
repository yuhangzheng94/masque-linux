### MASQUERADE

This project aim to reproduce the paper Evaluation of QUIC-based MASQUE Proxying https://dl.acm.org/doi/pdf/10.1145/3488660.3493806

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

1. Server

Run echo server or file server:
```bash
python tcp_echo_server.py
```
or
```bash
python tcp_file_server.py
```
2. Proxy

Run MASQUE server:
```bash
chmod +x src/masque_server.sh
./src/masque_server.sh
```
3. client

First run MASQUE client:
```bash
chmod +x src/masque_client.sh
./src/masque_client.sh "$PROXY_IP_ADDR"
```
In a new terminal, change the `"$SERVER_IP_ADDR"` accordingly and run echo client or file client:
```bash
python tcp_echo_client.py "$SERVER_IP_ADDR" "$(hostname -i)"
```
or
```bash
python tcp_file_server.py "$SERVER_IP_ADDR" "$(hostname -i)"
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
