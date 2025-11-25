// mutex.c - normal mutex that deadlocks when locked twice
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <unistd.h>
#include <pthread.h>

static volatile uint32_t shared_variable = 0;
static pthread_mutex_t shared_mutex;

/*
 * New helper function: increments the shared variable.
 * This function also locks the same mutex, so if the caller
 * already holds the mutex we will deadlock with a normal mutex.
 */
static void increment_shared(void)
{
    pthread_mutex_lock(&shared_mutex);   // inner lock
    ++shared_variable;
    pthread_mutex_unlock(&shared_mutex); // inner unlock
}

static void *increment(void *arg)
{
    (void)arg;

    while (true) {
        pthread_mutex_lock(&shared_mutex);  // outer lock
        increment_shared();                 // inner lock → deadlock
        pthread_mutex_unlock(&shared_mutex);

        usleep(1);
    }

    return NULL;
}

static void *reset(void *arg)
{
    (void)arg;

    unsigned int counter = 0;

    while (true) {
        sleep(1);

        pthread_mutex_lock(&shared_mutex);
        uint32_t snapshot = shared_variable;
        shared_variable = 0;
        pthread_mutex_unlock(&shared_mutex);

        printf("Loop %u: shared_variable reset, was %u\n",
               counter++, snapshot);
        fflush(stdout);
    }

    return NULL;
}

int main(void)
{
    pthread_t t1, t2;

    if (pthread_mutex_init(&shared_mutex, NULL) != 0) {
        perror("pthread_mutex_init");
        return 1;
    }

    pthread_create(&t1, NULL, increment, NULL);
    pthread_create(&t2, NULL, reset, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    pthread_mutex_destroy(&shared_mutex);
    return 0;
}
