sh ovs_connect.sh
sh flow_del.sh
sh topo_del.sh
echo "topo deleted!"

cd openvswitch-2.7.0
sh ovsinstall.sh

echo "ovs installed!"

cd ..
rm flowlet_log.txt
touch flowlet_log.txt
echo "file inited!"

sh topo_setup.sh
echo "topo setup!"

sh flow_setup.sh
echo "add flow!"
echo "ok! init finshed!"
