#include <stdio.h>
#include <pthread.h>
#include <stdint.h>
#include <inttypes.h>
#include <unistd.h>

// Global variable shared between the two threads
static uint32_t volatile shared_variable = 0;

void *increment(void *arg) {
  (void) arg;
  while (1) {
    shared_variable++;
  }
  return NULL;
}

void *reset(void *arg) {
  (void) arg;
  uint32_t loopcounter = 0;
  while (1) {
    sleep(1);
    printf("Loop %"PRIu32": shared_variable reset to 0, was %"PRIu32"\n", loopcounter++, shared_variable);
    shared_variable = 0;
  }
  return NULL;
}

int main() {
  pthread_t increment_thread;
  pthread_t reset_thread;

  // Create the two threads
  pthread_create(&increment_thread, NULL, increment, NULL);
  pthread_create(&reset_thread, NULL, reset, NULL);

  // Wait for the threads to finish (they won't due to infinite loops)
  pthread_join(increment_thread, NULL);
  pthread_join(reset_thread, NULL);

  return 0;
}
