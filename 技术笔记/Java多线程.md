# Java多线程

## 第一阶段 基础部分

1. Java应用程序的main函数是一个线程，是被JVM启动的时候调用，线程的名字叫main

2. 实现一个线程，必须创建Thread实例， override run方法， 并且调用start方法

3. 在JVM启动后，实际上有多个线程，但是至少有一个非守护线程

4. 当你调用start方法的时候，此时至少有两个线程，一个是调用你的线程，还有一个执行run方法的线程

5. 线程的生命周期分为new，runnable，running，blocked，terminated

6. 创建线程对象Thread，默认有一个线程名，以Thread-开头，从0开始

  构造函数 Thread()

  Thread-0  Thread-1

7. 如果在构造Thread的时候没有传递Runnable或者没有复写Thread的run方法，该Thread将不会调用任何东西，如果传递了Runnable接口的实例或者复写了Thread的run方法，则会执行该方法的逻辑单元（逻辑代码）

8. 如果构造线程对象时未传入ThreadGroup，Thread会默认获取父线程的ThreadGroup作为该线程的ThreadGroup，此时子线程和父线程将会在同一个ThreadGroup。

9. 构造Thread的时候传入stacksize代表着该线程占用的stack的大小，如果没有指定stacksize的大小，默认是0,0代表忽略该参数，该参数会被JNI函数去使用，需要注意：该参数在一些平台有效，在一些平台则无效。

   Thread()
   Allocates a new Thread object .
   Thread (Runnable target)
   Allocates a new Thread object.
   Thread (Runnable target， String name )
   Allocates a new Thread object .
   Thread (String name)
   Allocates a new Thread object .

   Thread (ThreadGroup group, Runnable target)
   Allocates a newI Thread object.
   Thread (ThreadGroup group， Runnable target， String name)
   Allocates a new Thread object so that it has target as its run object， has the specified name as its name, and belongs to the thread group referred to by group.
   Thread (ThreadGroup group, Runnable target, String name,
   long stackSize)
   Allocates a new Thread object so that it has target as
   its run object, has the specified name as its name, and belongs to the thread group referred to by group，and has the specified stack size.
   Thread (ThreadGroup group, String name)
   Allocates a new Thread object .

   10. setDaemon需要放置在start之前，这个操作是设置守护线程，让父线程结束的时候顺带结束子线程，例如心跳检测时使用。

   11. 不要企图利用优先级来控制线程的运行，不稳定。

   12. join是让子线程完成之后才继续父线程。比如在线程B中调用了线程A的join()方法，直到线程A执行完毕后，才会继续执行线程B。

   13. 优雅地关闭一个线程：

       ```java
       public class ThreadCloseGraceful {
           private static class Worker extends Thread {
               private volatile boolean start = true;
               @Override
               public void run() {
                   while (start) {
                       //TODO
                   }
               }
               public void shutdown() {
                   this.start = false;
               }
           }
           public static void main(String[] args) {
               Worker worker = new Worker();
               worker.start();
               try {
                   Thread.sleep(10000);
               } catch (InterruptedException e) {
                   e.printStackTrace();
               }
               worker.shutdown();
           }
       }
       ```

       ```java
       public class ThreadCloseGraceful2 {
           private static class Worker extends Thread {
       
               @Override
               public void run() {
                   while (true) {
                       if (Thread.interrupted()) {
                           break;
                       }
                   }
                   //TODO
               }
           }
           public static void main(String[] args) {
               Worker worker = new Worker();
               worker.start();
       
               try {
                   Thread.sleep(3000);
               } catch (InterruptedException e) {
                   e.printStackTrace();
               }
               worker.interrupt();
           }
       }
       ```

这两种方法在TODO中如果有会导致线程blocked的操作，就不能进入判断部分，这时直接打断就会有问题了。

14. 强制打断线程：

    将任务放置在子线程，设置子线程为守护线程，然后打断主线程

15. 线程1持有锁a，想要锁b，线程2持有锁b，想要锁a，构成死锁。

16. sleep和wait的区别

sleep是Thread的方法，wait是Object的方法

sleep不会释放锁，但是wait会释放当前锁，并将Object放到等待队列中

sleep方法不需要同步，但是wait需要

sleep方法不需要被唤醒，但是wait需要（wait（10）除外）

17. 给程序添加Hook，用于做一些停止之后的工作，只要不是kill -9强杀就行。

```java
Runtime.getRuntime().addShutdownHook(new Thread(()->{
	System.out.println("The application will be exit.");
	notifyAndRelease();//做一些关闭后的操作
}));
```

18. 拿到线程run方法中的出错

    ```java
    t.setUncaughtExceptionHandler((thread, e) -> {
        System.out.println(e);
        System.out.println(thread);
    });
    t.start();
    ```

19. 查看调用的记录

```java
Arrays.asList(Thread.currentThread().getStackTrace()).stream()
        .filter(e -> !e.isNativeMethod())
        .forEach(e -> Optional.of(e.getClassName() + ":" + e.getMethodName() + ":" + e.getLineNumber())
                .ifPresent(System.out::println)
        );
```

20. ThreadGroup 能代表一组线程，同时也能包含其他的Thread groups，属于树状结构。除了初始化的Thread group，其他的Thread group都有parent。一个线程允许自己所在的Thread group相关信息，但是根据JDK的描述是不允许访问别的Thread group（测试下来，只读信息是可以访问的，比如激活线程数）。

21. 自定义线程池：

1. 任务队列
2. 拒绝策略（抛出异常，直接丢弃，阻塞，临时队列）
3. 初始化值 init（min）
4. active
5. max

min<=active<=max

## 第二阶段 多线程设计

1. 单例模式中饿汉是线程安全的，懒汉设计是导致线程出安全问题的主要因素。

2. WaitSet 

   1.所有的对象都会有一个wait set,用来存放调用了该对象wait方法之后进入block状态线程
   2.线程被notify之后，不一定立即得到执行
   3.线程从wait set中被唤醒顺序不一定是FIFO.
   4.线程被唤醒后，必须重新获取锁

3. java可能还会对你只有读操作的线程进行“优化”，认为你的程序不需要更新值。

i = 1;
i = 1+1;
cpu 1 -> main memory->i ->cache i+1 -> cache(2) - > main memory(2)
cpu 2 -> main memory->i ->cache i+1 -> cache(2) - > main memory(2)

解决方式：

1. 给数据总线加锁

   总线（数据总线， 地址总线，控制总线）

2. CPU高速缓存一致性协议 intel 提出的 MESI

核心思想

1. 当CPU写入数据的时候，如果发现该变量被共享，（也就是说，在其他CPU中也存在该变量的副本）会发出一个信号，通知其他CPU该变量的缓存无效。
2. 当其他CPU访问该变量的时候，重新导主内存进行获取。

并发编程中的个比较重要的概念

1. 原子性A 一个操作或者多个操作要么都成功要么都失败，中间不能由于任何因素中断
2. 可见性
3. 有序性 1. 重排序只要求最终一致性

在JVM中

1. 原子性
   对基本数据类型的变量读取和赋值是保证了原子性的，要么都成功，要么都失败，这些操作不可被中断

2. 可见性

   使用volatile关键字保证可见性

3. 有序性

   happens-before relationship

   3.1 在一个线程内代码的执行顺序，编写在前面的发生在编写在后面的之前

   3.2 unlock必须发生在lock之后

   3.3 volatile修饰的变量，对该变量的写操作先于该变量的读操作

   3.4 传递规则，操作A先于B，B先于C，那么A肯定先于C

   3.5 线程启动规则，start方法肯定先于线程的run

   3.6 线程中断规则，interrupt这个动作，必须发生在捕获该动作之前

   3.7 对象销毁规则，初始化必须发生在finalize之前

   3.8 线程终结规则，所有的操作都发生在线程死亡之前

### volatile关键字

一旦一个共享变量被volatile修饰，具备两层语义

1. 保证了不同线程间的可见性
2. 禁止对其进行重排序，也就是保证了有序性
3. 并未保证原子性

Volatile关键字

1. 保证重排序的是偶不会把后面的指令放到屏障的前面，也不会把前面的放到后面
2. 强制对缓存的修改操作立刻写入主存
3. 如果是写操作，他会导致其他CPU中的缓存失效

Volatile使用场景

1. 状态量标记
2. 保证线程屏障前后的一致性

