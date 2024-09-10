#!/bin/bash


for i in {0..555767}; do
wu_name="pano121_1.00_$i"
  echo "create_work: ${wu_name}"
  bin/create_work --appname pano121 \
    --wu_template templates/pano121_in \
    --result_template templates/pano121_out \
    --command_line "--start ${i*184} --end ${(i+1)*184}" \
    --wu_name "${wu_name}" \
    --min_quorum 2 \
    --credit 2500

done