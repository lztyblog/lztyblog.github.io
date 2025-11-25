#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>

static bool flag = false;

void *sender(void *arg) {
  (void) arg;
  sleep(1);
  printf("Setting the flag now.\n");
  flag = true;
  return NULL;
}

void *receiver(void *arg) {
  (void) arg;
  printf("Waiting for the flag...\n");
  while (!flag);
  printf("Flag set, exiting\n");
  return NULL;
}

int main(void) {

  pthread_t thread1_id, thread2_id;

  printf("Creating threads...\n");
  
  pthread_create(&thread1_id, NULL, sender, NULL);
  pthread_create(&thread2_id, NULL, receiver, NULL);

  pthread_join(thread1_id, NULL);
  printf("Joined thread 1\n");
  pthread_join(thread2_id, NULL);
  printf("Joined thread 2\n");
  
  printf("Done.\n");
  return 0;
}

