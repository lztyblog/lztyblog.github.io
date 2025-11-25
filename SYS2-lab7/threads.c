#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>

void *first(void *arg) {
  return NULL;
}

void *second(void *arg) {
  return NULL;
}

int main(void) {

  pthread_t thread1_id, thread2_id;

  printf("Creating threads...\n");
  
  pthread_create(&thread1_id, NULL, first, NULL);
  pthread_create(&thread2_id, NULL, second, NULL);

  pthread_join(thread1_id, NULL);
  printf("Joined thread 1\n");
  pthread_join(thread2_id, NULL);
  printf("Joined thread 2\n");
  
  printf("Done.\n");
  return 0;
}

