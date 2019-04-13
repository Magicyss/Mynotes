# UFW-防火墙
几条极简指令  
查看防火墙状态
```shell
sudo ufw status
```
防火墙启动（注意在开启之前允许你的22端口，否则会断开ssh）
```shell
sudo ufw enable
```
允许22端口
```shell
sudo ufw allow 22
```
删除已经添加过的规则
```shell
sudo ufw delete allow 22
```
只打开使用tcp/ip协议的22端口：
```shell
sudo ufw allow 22/tcp
```