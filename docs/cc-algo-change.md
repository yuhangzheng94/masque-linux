# TCP Congestion Control Algorithm in Linux
To view current congestion control algorithm:
```bash
sysctl net.ipv4.tcp_congestion_control
```

To temporarily modify congestion control algorithm (to `reno`, for example):
```bash
sudo /sbin/sysctl -w net.ipv4.tcp_congestion_control=reno
```

Reference: https://jasonmurray.org/posts/2021/tcpcca/