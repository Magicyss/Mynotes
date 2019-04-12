# 安装 Tomcat
官网下载 *.tar.gz* 格式的安装包  
切换到 /usr/lib目录下：
```shell
cd /usr/lib
```
并新建tomcat目录：
```shell
sudo mkdir tomcat
```
解压并移到新建的jdk目录：
```shell
sudo tar -zxvf apache-tomcat-9.0.17.tar.gz -C /usr/lib/tomcat
```
现在先修改一下tomcat文件夹的使用权限，否则可能在当前用户下不能进入bin目录：
```shell
cd /usr/lib
sudo chmod 777 -R tomcat
```
进入/tomcat/apache-tomcat-8.5.9/bin，编辑文件 *startup.sh* ，在最后一行之前加入如下信息：
```shell
#set java environment
export JAVA_HOME=/usr/lib/jdk/jdk-12
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:%{JAVA_HOME}/lib:%{JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH

#tomcat
export TOMCAT_HOME=/usr/lib/tomcat/apache-tomcat-9.0.17
```


如果要关闭tomcat，需要先在文件shutdown.sh对应位置添加信息：
```shell
#set java environment
export JAVA_HOME=/usr/lib/jdk/jdk-12
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:%{JAVA_HOME}/lib:%{JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH

#tomcat
export TOMCAT_HOME=/usr/lib/tomcat/apache-tomcat-9.0.17
```

然后执行如下命令即可：
```shell
sudo ./shutdown.sh
```
如果要设置为tomcat开机自启动，需要编辑文件/etc/rc.local，这里存放着开机自启动的程序。
```shell
sudo vi /etc/rc.local
```
在最后一行之前加入如下信息：（配置你自己的tomcat的startup.sh文件的路径）
```shell
#set java environment
export JAVA_HOME=/usr/lib/jdk/jdk-12
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:%{JAVA_HOME}/lib:%{JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH

/usr/lib/tomcat/apache-tomcat-9.0.17/bin/startup.sh
```
接下来修改端口从8080修改到80  
在Ubuntu下，只修改了server.xml文件后发现无法访问到服务。  
我们需要使用authbind来对端口进行配置
```shell
sudo apt-get install authbind
```
然后配置80端口:
```shell
sudo touch /etc/authbind/byport/80
```
接下来再启动tomcat就可以访问到80的服务了:
```shell
sude ./startup.sh
sudo authbind --deep ./catalina.sh start
```