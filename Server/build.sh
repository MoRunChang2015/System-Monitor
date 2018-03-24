#/bin/bash

tar -zcvf server.tar.gz .

docker build . -f dockerfile -t server:1.0
