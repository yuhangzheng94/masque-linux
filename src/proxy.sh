#!/bin/bash
log_level=debug
masque_server_port=8989
cd ..
export RUST_LOG=$log_level
echo "starting proxy..."
chmod +x bin/server
./bin/server "$(hostname -i)":"$masque_server_port"