#!/bin/bash

ip rule add fwmark 1 lookup 100
ip route add local 0.0.0.0/0 dev lo table 100