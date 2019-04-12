# 安装 JDK
---
官网下载 *.tar.gz* 格式的安装包  
切换到 /usr/lib目录下：
```shell
cd /usr/lib
```
并新建jdk目录：
```shell
sudo mkdir jdk
```
解压并移到新建的jdk目录：
```shell
sudo tar -zxvf jdk-12_linux-x64_bin.tar.gz -C /usr/lib/jdk
```
配置java环境变量
这里是将环境变量配置在etc/profile，即为所有用户配置JDK环境。  
使用命令打开/etc/profile文件
```shell
sudo vi /etc/profile
```
在末尾添加以下几行文字：
```shell
#set java env
export JAVA_HOME=/usr/lib/jdk/jdk-12
export JRE_HOME=${JAVA_HOME}/jre    
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib    
export PATH=${JAVA_HOME}/bin:$PATH
```
执行命令使修改立即生效
```shell
source /etc/profile 
```
测试安装是否成功  
在终端输入，出现版本号则表示安装成功
```shell
java -version
```
结果：
```shell
ubuntu@VM-0-11-ubuntu:~$ java -version
java version "12" 2019-03-19
Java(TM) SE Runtime Environment (build 12+33)
Java HotSpot(TM) 64-Bit Server VM (build 12+33, mixed mode, sharing)
```