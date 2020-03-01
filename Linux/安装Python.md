# 安装Python

系统为Cent OS 7 64位  

首先需要安装相关依赖  

```shell
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
```

下载Python的安装包  

可以直接下载好tgz文件，用ftp传给主机  

```shell
wget https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz
```

 解压tgz 

```shell
tar -xvf Python-3.7.6.tgz
```

 创建python3的文件路径 

```shell
mkdir /usr/local/python3
```

编译（在解压的文件夹下）

```shell
./configure --prefix=/usr/local/python3
```

安装（在解压的文件夹下 ）

```shell
make&make install
```

创建新版本软连接

修改旧版本

* 这里会带来一些问题，在之后使用yum安装包是，由于系统原来使用的是Python2.7，所以会出现报错的情况，需要修改两处 /usr/bin/yum 以及 /usr/libexec/urlgrabber-ext-down ， 将第一行"#!/usr/bin/python" 改为 "#!/usr/bin/python_bak"即可 

```shell
mv /usr/bin/python /usr/bin/python_bak
```

创建新的软连接

```shell
ln -s /usr/local/python3/bin/python3 /usr/bin/python
```

检查python的版本

```
python -V
```

配置pip3

```shell
vim ~/.bash_profile
```

```shell
# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
        . ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/bin:/usr/local/python3/bin

export PATH
```

让修改操作生效

```shell
source ~/.bash_profile
```

更新pip3

```shell
pip3 install --upgrade pip
```