# 服务器HTTPS设置
在申请完证书之后，解压获得Tomcat的 *jks* 文件  
在conf目录下的server.xml文件中添加：
```shell
<Connector port="443" protocol="HTTP/1.1" SSLEnabled="true" maxThreads="150" scheme="https" secure="true" keystoreFile="conf/xxx.jks" keystorePass="xxx" clientAuth="false" sslProtocol="TLS" />
```
由于安装了authbind，所以需要配置一下443端口
```shell
sudo touch /etc/authbind/byport/443
```
接下来再启动tomcat就可以https了。
```shell
sudo ./startup.sh
sudo authbind --deep ./catalina.sh start
```