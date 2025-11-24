// sharedmem.c : Shared memory + fork + mmap + urandom exercise

#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <fcntl.h>
#include <stdlib.h>

int main(void) {
    // Create shared memory for one 64-bit integer
    uint64_t *shared =
        mmap(NULL, sizeof(uint64_t),
             PROT_READ | PROT_WRITE,
             MAP_SHARED | MAP_ANONYMOUS,
             -1, 0);

    if (shared == MAP_FAILED) {
        perror("mmap");
        exit(EXIT_FAILURE);
    }

    pid_t pid = fork();

    if (pid < 0) {
        perror("fork");
        exit(EXIT_FAILURE);
    }

    // ---------------------------
    //           CHILD
    // ---------------------------
    if (pid == 0) {
        sleep(1);   // give parent time to write

        printf("Child  PID = %" PRIdMAX
               ", value read = 0x%" PRIx64 "\n",
               (intmax_t)getpid(), *shared);

        munmap(shared, sizeof(uint64_t));
        exit(EXIT_SUCCESS);
    }

    // ---------------------------
    //           PARENT
    // ---------------------------
    int fd = open("/dev/urandom", O_RDONLY);
    if (fd < 0) {
        perror("open /dev/urandom");
        exit(EXIT_FAILURE);
    }

    uint64_t num = 0;

    ssize_t r = read(fd, &num, sizeof(num));
    if (r != sizeof(num)) {
        perror("read /dev/urandom");
        close(fd);
        exit(EXIT_FAILURE);
    }
    close(fd);

    // print the parent's info
    printf("Parent PID = %" PRIdMAX
           ", random value = 0x%" PRIx64 "\n",
           (intmax_t)getpid(), num);

    // write to shared memory
    *shared = num;

    // wait for child
    wait(NULL);

    munmap(shared, sizeof(uint64_t));
    return 0;
}
