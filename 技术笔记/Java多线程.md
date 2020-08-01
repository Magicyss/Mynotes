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