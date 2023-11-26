#!/bin/bash
log_level=debug
masque_server_port=4433
export RUST_LOG=$log_level
echo "starting masque server..."
chmod +x bin/server
./bin/server "$(hostname -i)":"$masque_server_port"