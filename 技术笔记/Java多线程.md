# Java多线程

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

15. 

