#!/bin/sh

sudo /home/pentaho/data-integration/kitchen.sh -file=pdi/load_INT.kjb -level=Minimal
echo "INT load Successful: $(date)" >> /home/pentaho/data-integration/pdi/INT_load.log
