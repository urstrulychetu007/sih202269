"Camera 1", 0)
    thread2 = camThread("Camera 2", 1)
    thread1.start()
    thread2.start()