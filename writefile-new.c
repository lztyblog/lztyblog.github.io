// writefile.c : create testfile.txt with specific permissions using POSIX syscalls

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>      // open()
#include <unistd.h>     // write(), close()
#include <sys/stat.h>   // mode constants
#include <sys/types.h>  // mode_t
#include <errno.h>
#include <string.h>     // strerror()

int main(void) {
    const char *filename = "testfile.txt";

    const char *message = "This is a simple test file for the OS lab exercise.";
    const size_t msg_len = 51;  // strlen(message)，

       权限：S_IRUSR == 0400，
    int fd = open(filename,
                  O_WRONLY | O_CREAT | O_TRUNC,
                  S_IRUSR);

    if (fd < 0) {
        fprintf(stderr, "open() failed: %s\n", strerror(errno));
        return EXIT_FAILURE;
    }

    ssize_t total_written = 0;

    while ((size_t)total_written < msg_len) {
        ssize_t n = write(fd,
                          message + total_written,
                          msg_len - (size_t)total_written);
        if (n < 0) {
            fprintf(stderr, "write() failed: %s\n", strerror(errno));
            close(fd);
            return EXIT_FAILURE;
        }
        total_written += n;
    }

    if (close(fd) < 0) {
        fprintf(stderr, "close() failed: %s\n", strerror(errno));
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
