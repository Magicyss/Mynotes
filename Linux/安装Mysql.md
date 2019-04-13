# 安装 Mysql
Ubuntu上安装mysql非常简单只需要几条命令就可以完成。
```shell
sudo apt-get install mysql-server
sudo apt-get install mysql-client
sudo apt-get install libmysqlclient-dev
```
命令检查之后，如果看到有mysql 的socket处于 listen 状态则表示安装成功
```shell
sudo netstat -tap | grep mysql
```
登陆mysql数据库可以通过如下命令：
```shell
mysql -u root -p 
```
## 实现远程控制mysql
首先编辑文件 */etc/mysql/mysql.conf.d/mysqld.cnf* 编辑配置文件就输入命令
```shell
sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf
```
接下来登录本地MySQL，查看所有用户
```shell
use mysql;
select host,user from user;
```
结果如下：
```shell
mysql> select host,user from user;
+-----------+------------------+
| host      | user             |
+-----------+------------------+
| localhost | debian-sys-maint |
| localhost | mysql.session    |
| localhost | mysql.sys        |
| localhost | root             |
+-----------+------------------+
4 rows in set (0.00 sec)
````
新建用户magicy
```shell
CREATE USER 'magicy'@'localhost' IDENTIFIED BY '123456';
select host,user from user;
```
结果：
```shell
mysql> select host,user from user;
+-----------+------------------+
| host      | user             |
+-----------+------------------+
| localhost | debian-sys-maint |
| localhost | magicy           |
| localhost | mysql.session    |
| localhost | mysql.sys        |
| localhost | root             |
+-----------+------------------+
5 rows in set (0.00 sec)
```
给新用户权限：
```shell
GRANT ALL PRIVILEGES ON *.* TO 'magicy'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
FLUSH PRIVILEGES; 
```
退出mysql后重启mysql
```shell
sudo service mysql restart
```
在Windows下的Navicat中连接时出现1045错误，先点测试连接就好了，具体原因未知。