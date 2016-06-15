#!/bin/sh

sudo /home/pentaho/data-integration/kitchen.sh -file=pdi/load_Odoo_from_INT.kjb -level=Minimal
echo "To Odoo from INT load Successful: $(date)" >> /home/pentaho/data-integration/pdi/INT_load.log
