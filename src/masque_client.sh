#!/bin/bash
log_level=debug
masque_server_port=4433
masque_client_port=8989
export RUST_LOG=$log_level
echo "starting masque client"
chmod +x bin/client
./bin/client "$1:$masque_server_port" "$(hostname -i)":"$masque_client_port"