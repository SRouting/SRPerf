cp ./trex_cfg.yaml /etc/trex_cfg.yaml

sh -c 'cd /opt/trex-core-2.41/scripts/ && sudo nohup ./t-rex-64 -i -c 7 --iom 0 > /tmp/trex.log 2>&1 &' > /dev/null
