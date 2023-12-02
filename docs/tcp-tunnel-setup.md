# Setting up TCP tunneling using Python
Install `pip` in Linux:
```bash
sudo apt install python3-pip
```
Install `pytunnel` with `pip`:
```bash
pip install pytunnel
```
On proxy, run:
```bash
python -m pytunnel --bind "$PROXY_IP_ADDR":4434
```
On client, run:
```bash
python -m pytunnel --port 4433 --target "$CLIENT_IP_ADDR":8989 --server "$PROXY_IP_ADDR":4434
```