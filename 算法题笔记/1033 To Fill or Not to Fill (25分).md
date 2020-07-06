# 1033 To Fill or Not to Fill (25分)

题目描述：

```
With highways available, driving a car from Hangzhou to any other city is easy. But since the tank capacity of a car is limited, we have to find gas stations on the way from time to time. Different gas station may give different price. You are asked to carefully design the cheapest route to go.
```

Input Specification:

```
Each input file contains one test case. For each case, the first line contains 4 positive numbers: C_max(≤ 100), the maximum capacity of the tank; D (≤30000), the distance between Hangzhou and the destination city; D_avg(≤20), the average distance per unit gas that the car can run; and N (≤ 500), the total number of gas stations. Then N lines follow, each contains a pair of non-negative numbers: P_i, the unit gas price, and D_i(≤D), the distance between this station and Hangzhou, for i=1,⋯,N. All the numbers in a line are separated by a space.
```

Output Specification:

```
For each test case, print the cheapest price in a line, accurate up to 2 decimal places. It is assumed that the tank is emstationy at the beginning. If it is impossible to reach the destination, print The maximum travel distance = X where X is the maximum possible distance the car can run, accurate up to 2 decimal places.
```

Sample Input 1:

```
50 1300 12 8
6.00 1250
7.00 600
7.00 150
7.10 0
7.20 200
7.50 400
7.30 1000
6.85 300
```

Sample Output 1:

```
749.17
```

Sample Input 2:

```
50 1300 12 2
7.10 0
7.00 600
```

Sample Output 2:

```
The maximum travel distance = 1200.00
```

首先说一下思路，典型的贪心问题，所以应该找尽可能便宜的油站，按照油价的从低到高排序之后，分情况讨论，在车辆可以到达的历程里寻找尽可能便宜的油站作为补给，来进行加油：

1.历程里有比当前加油站更便宜或者等价的加油站，那么二话不说，直接只加到刚好到达便宜加油站的油；

2.如果历程里都没有比当前加油站更便宜或者等价的加油站，那门选择历程里最便宜的加油站，在当前加油站加满油，再赶过去；

3.如果历程里没有加油站了，那么就把邮箱的油跑完，就算是最终的结果了。

所以有了第一个版本，然而，第一个版本是有问题的：

```c++
#include <iostream>
#include <cstdio>
#include <math.h>
#include <algorithm>
#include <string>

using namespace std;
typedef long long ll;
const double eps = 1e-8;
struct station{
    double x;
    double y;
}info[1000];
bool cmp(station a,station b) {
        return a.y<b.y;
}

int main() {

    int c=0,d=0,average=0,n=0,i=0;

    while (scanf("%d %d %d %d", &c,&d,&average,&n) != EOF) {//邮箱容积 目的地距离 单位油能跑多远 总共多少加油站
        for (i = 0; i < n; i++) {
            scanf("%lf %lf", &info[i].x,&info[i].y);
        }
        info[n].x=9999;
        info[n].y=d;
        sort(info,info+n,cmp);
        if (info[0].y!=0){
            printf("The maximum travel distance = 0.00\n");
            return 0;
        }
        double oilDistance=c*average;//满邮箱最远跑多远
        double resultDistance=0.0;
        double cost=0.0;
        double distanceRemain=0.0;//跑完某段之后邮箱剩下多少距离可以跑
        int tempPosition=-1;//临时位置，记录下一个可能的值
        int nowPosition=0;
        double minPrice=999999;
        int flag=0;//0表示有最优解,需要输出最优解
        while(nowPosition<n){
            minPrice=99999;
            for (i = 1+nowPosition; i <=n&&info[i].y<=info[nowPosition].y+oilDistance; i++) {
                if(info[i].x<=minPrice){
                    minPrice=info[i].x;
                    tempPosition=i;
                    if(info[i].x<=info[nowPosition].x){
                        break;
                    }
                }
            }
            if(tempPosition!=-1){
                if(minPrice<=info[nowPosition].x){
                    //如果下一站比现在的价格低，那么应该只加到刚好到站的油量
                    cost+=((info[tempPosition].y-info[nowPosition].y-distanceRemain)/average*info[nowPosition].x);
                    resultDistance=info[tempPosition].y;
                    distanceRemain=0;//刚好用完
                }else{//下一站比现在贵，所以应该尽可能加现在便宜的，满上
                    cost+=((oilDistance-distanceRemain)/average*info[nowPosition].x);
                    distanceRemain=oilDistance-(info[tempPosition].y-info[nowPosition].y);
                    resultDistance=info[tempPosition].y;
                }
                nowPosition=tempPosition;
                tempPosition=-1;
                continue;
            } else{
                flag=1;
                break;
            }

        }
        if(flag==0){
            printf("%.2f\n",cost);
        }else{
            printf("The maximum travel distance = %.2f\n",resultDistance+oilDistance);
        }
    }
    return 0;
}
```

上面代码的问题在于，到了最后一站，由于我初始化的价格设置的比较大，所以会导致最后一站也跑到尽可能加便宜的油这一分支，导致结果出错，所以在上方的if中可以可以改成：

```c++
if(minPrice<=info[nowPosition].x || tempPosition==n)
```

然后在PAT官网测试下来，发现无法通过测试用例4，然后通过查询得知用例四的特点是在后面的加油站一个比一个贵，也就是会导致进入尽可能加便宜的油这一分支，所以加的油就超过了终点站需要油，所以价格超了，由此又在else里面添加了一个分支：

```c++
if(info[nowPosition].y+oilDistance>info[n].y) {
    cost+=((info[n].y-info[nowPosition].y-distanceRemain)/average*info[nowPosition].x);
    resultDistance=info[n].y;
    tempPosition=n;
    distanceRemain=0;
    break;
}
```

所以，这时可以通过了整个PAT的测试集，但是代码实在是不好看，不够优雅，然后我发现一个问题，我为什么会把最后终点站的价格设置的那么高？把它改成0，上面两个问题就都解决了[摊手]：

```c++
#include <iostream>
#include <cstdio>
#include <math.h>
#include <algorithm>
#include <string>
using namespace std;
typedef long long ll;
const double eps = 1e-8;
struct station{
    double x;
    double y;
}info[10000];
bool cmp(station a,station b) {
        return a.y<b.y;
}
int main() {
    int c=0,d=0,average=0,n=0,i=0;
    while (scanf("%d %d %d %d", &c,&d,&average,&n) != EOF) {//邮箱容积 目的地距离 单位油能跑多远 总共多少加油站
        for (i = 0; i < n; i++) {
            scanf("%lf %lf", &info[i].x, &info[i].y);
        }
        info[n].x = 0;
        info[n].y = d;
        sort(info, info + n, cmp);
        if (info[0].y != 0) {
            printf("The maximum travel distance = 0.00\n");
            return 0;
        }
        double oilDistance = c * average;//满邮箱最远跑多远
        double resultDistance = 0.0;
        double cost = 0.0;
        double distanceRemain = 0.0;//跑完某段之后邮箱剩下多少距离可以跑
        int tempPosition = -1;//临时位置，记录下一个可能的值
        int nowPosition = 0;
        double minPrice = 999999;
        while (nowPosition < n) {
            minPrice = 99999;
            for (i = 1 + nowPosition; i <= n && info[i].y <= info[nowPosition].y + oilDistance; i++) {
                if (info[i].x <= minPrice) {
                    minPrice = info[i].x;
                    tempPosition = i;
                    if (info[i].x <= info[nowPosition].x) {
                        break;
                    }
                }
            }
            if (tempPosition != -1) {
                if (minPrice <= info[nowPosition].x) {
                    //如果下一站比现在的价格低，那么应该只加到刚好到站的油量;终点站也是一样
                    cost += ((info[tempPosition].y - info[nowPosition].y - distanceRemain) / average *
                             info[nowPosition].x);
                    resultDistance = info[tempPosition].y;
                    distanceRemain = 0;//刚好用完
                } else {//下一站比现在贵，所以应该尽可能加现在便宜的，满上
                    cost += ((oilDistance - distanceRemain) / average * info[nowPosition].x);
                    distanceRemain = oilDistance - (info[tempPosition].y - info[nowPosition].y);
                    resultDistance = info[tempPosition].y;
                }
                nowPosition = tempPosition;
                tempPosition = -1;
                continue;
            } else {
                break;
            }
        }
        if (nowPosition == n) {
            printf("%.2f\n", cost);
        } else {
            printf("The maximum travel distance = %.2f\n", resultDistance + oilDistance);
        }

    }
    return 0;
}
```