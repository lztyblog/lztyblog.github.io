#include <stdio.h>
#include <pthread.h>
#include <stdint.h>
#include <inttypes.h>
#include <unistd.h>

// Global variable shared between the two threads
static uint32_t volatile shared_variable = 0;

// One shared mutex (now recursive)
static pthread_mutex_t shared_mutex;

/*
 * Same helper function, but recursive mutex prevents deadlock.
 */
static void increment_shared(void)
{
    pthread_mutex_lock(&shared_mutex);   // inner lock (allowed for recursive mutex)
    shared_variable++;
    pthread_mutex_unlock(&shared_mutex);
}

void *increment(void *arg) {
  (void) arg;

  while (1) {
    pthread_mutex_lock(&shared_mutex);  // outer lock

    increment_shared();                 // inner lock, OK now

    pthread_mutex_unlock(&shared_mutex);

    usleep(1);
  }
  return NULL;
}

void *reset(void *arg) {
  (void) arg;
  uint32_t loopcounter = 0;

  while (1) {
    sleep(1);

    pthread_mutex_lock(&shared_mutex);
    printf("Loop %"PRIu32": shared_variable reset to 0, was %"PRIu32"\n",
           loopcounter++, shared_variable);
    shared_variable = 0;
    pthread_mutex_unlock(&shared_mutex);
  }
  return NULL;
}

int main() {
  pthread_t increment_thread;
  pthread_t reset_thread;

  pthread_mutexattr_t attr;

  // initialize mutex attributes
  pthread_mutexattr_init(&attr);

  // ⭐ THIS is the only change:
  // set the mutex to be RECURSIVE
  pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_RECURSIVE);

  // initialize the mutex WITH the attribute
  pthread_mutex_init(&shared_mutex, &attr);

  pthread_mutexattr_destroy(&attr);

  pthread_create(&increment_thread, NULL, increment, NULL);
  pthread_create(&reset_thread, NULL, reset, NULL);

  pthread_join(increment_thread, NULL);
  pthread_join(reset_thread, NULL);

  pthread_mutex_destroy(&shared_mutex);
  return 0;
}
