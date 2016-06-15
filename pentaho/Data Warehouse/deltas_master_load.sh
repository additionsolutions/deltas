#!/bin/sh

sudo /home/pentaho/data-integration/kitchen.sh -file=pdi/load_master_DWH.kjb -level=Minimal
echo "DWH load Successful: $(date)" >> /home/pentaho/data-integration/pdi/DWH_master_load.log
