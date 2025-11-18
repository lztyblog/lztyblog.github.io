// writefile.c - small demo for creating a file using POSIX calls
// looks a bit like a beginner wrote it deliberately :)

#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>

int main(void)
{
    int fd;
    const char *message = "This is a small test message for the OS lab file task.\n";
    /* length > 30 chars, < 150 chars, all printable ASCII */

    /* create the file with read-only permission for the owner (0400) */
    fd = open("testfile.txt", O_CREAT | O_WRONLY | O_TRUNC, 0400);

    if (fd < 0) {
        perror("open");
        return 1;
    }

    /* write the content into the file */
    ssize_t written = write(fd, message, 59); /* manually counted length */

    if (written < 0) {
        perror("write");
        close(fd);
        return 1;
    }

    close(fd);
    return 0;
}
