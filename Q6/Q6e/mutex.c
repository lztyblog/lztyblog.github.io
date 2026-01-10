#include <time.h>
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include <stdint.h>

static uint32_t shared = 0;
static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;

static void do_increment(void) {
    pthread_mutex_lock(&m);
    shared++;
    pthread_mutex_unlock(&m);
}

static void* increment_thread(void* arg) {
    (void)arg;
    while (1) {
        struct timespec ts={0,100};
	nanosleep(&ts, NULL);
        pthread_mutex_lock(&m);
        do_increment();
        pthread_mutex_unlock(&m);
    }
    return NULL;
}

static void* reset_thread(void* arg) {
    (void)arg;
    while (1) {
        sleep(1);
        pthread_mutex_lock(&m);
        printf("shared = %u\n", (unsigned)shared);
        shared = 0;
        pthread_mutex_unlock(&m);
    }
    return NULL;
}

int main(void) {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, increment_thread, NULL);
    pthread_create(&t2, NULL, reset_thread, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    return 0;
}

