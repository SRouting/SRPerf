sut_rcv_iface="enp129s0f0"
sut_snd_iface="enp129s0f1"
/usr/local/sbin/ethtool -K ${sut_rcv_iface} gro off
/usr/local/sbin/ethtool -K ${sut_rcv_iface} gso off
/usr/local/sbin/ethtool -K ${sut_rcv_iface} tso off
/usr/local/sbin/ethtool -K ${sut_rcv_iface} lro off
/usr/local/sbin/ethtool -K ${sut_rcv_iface} rx off tx off

/usr/local/sbin/ethtool -K ${sut_snd_iface} gro off
/usr/local/sbin/ethtool -K ${sut_snd_iface} gso off
/usr/local/sbin/ethtool -K ${sut_snd_iface} tso off
/usr/local/sbin/ethtool -K ${sut_snd_iface} lro off
/usr/local/sbin/ethtool -K ${sut_snd_iface} rx off tx off
