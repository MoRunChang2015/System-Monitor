#!/bin/bash

tar -zcvf agent.tar.gz .

docker build . -f dockerfile -t agent:1.0
