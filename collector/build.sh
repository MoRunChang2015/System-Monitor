#!/bin/bash

tar -zcvf collector.tar.gz .

docker build . -f dockerfile -t collector:1.0
