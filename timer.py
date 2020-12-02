import time

# Variables à utiliser dans les autres fichiers
max_time = 180.0
timer = max_time
timer_paused = True

# Variables de calculs
time_last_frame=time.time()
timer_end = time.time()+max_time


def flip_timer():
    """
    Return le sablier et met le jeu en pause pour parler.
    """
    global timer, timer_end, timer_paused

    timer=max_time-timer
    timer_end=time.time()+timer


def update_timer():
    """
    Met à jour le timer.
    """
    global timer_end, timer_paused, timer, time_last_frame

    delta_time=time.time()-time_last_frame

    if timer_paused:
        timer_end+=delta_time

    else:
        timer=timer_end-time.time()

    time_last_frame=time.time()

def set_timer(value):
    global timer, timer_end
    update_timer()
    timer = value
    timer_end = time.time()+timer