#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

#define BUFSIZE 128

/* safe_write: keep calling write() until all data is written, or error */
static int safe_write(int fd, const char *buffer, size_t length)
{
    size_t total = 0;

    while (total < length) {
        ssize_t written = write(fd, buffer + total, length - total);
        if (written < 0) {
            return -1;   /* error */
        }
        total += (size_t)written;
    }

    return 0;            /* success */
}

/* Return pointer to basename part of argv[0] (after final '/') */
static const char *get_invocation_name(const char *path)
{
    const char *slash = strrchr(path, '/');
    if (slash == NULL) {
        return path;
    }
    return slash + 1;
}

int main(int argc, char const * argv[]) {

  if (argc > 2) {
    dprintf(2, "Usage: %s [filename]\n", argv[0]);
    exit(1);
  }
  
  int fd = 0;
  if (argc == 2) {
    fd = open(argv[1], O_RDONLY);
    if (fd < 0) {
      perror(argv[1]);
      exit(fd);
    }
  }

  // Your code goes here!

  /* Work out how we were invoked, like Busybox:
     only look at the part after the last '/' */
  const char *progname = get_invocation_name(argv[0]);

  int do_upper = 0;
  int do_lower = 0;

  if (strcmp(progname, "upper") == 0) {
      do_upper = 1;
  } else if (strcmp(progname, "lower") == 0) {
      do_lower = 1;
  } else {
      dprintf(2,
              "Error: invocation name must be 'upper' or 'lower' (got '%s').\n",
              progname);
      exit(1);
  }

  char buffer[BUFSIZE];
  ssize_t nread;

  /* Main loop: read → convert → write */
  while ((nread = read(fd, buffer, BUFSIZE)) > 0) {

      /* Convert in-place */
      for (ssize_t i = 0; i < nread; i++) {
          unsigned char c = (unsigned char)buffer[i];

          if (do_upper) {
              if (c >= 'a' && c <= 'z') {
                  buffer[i] = (char)(c - ('a' - 'A'));
              }
          } else if (do_lower) {
              if (c >= 'A' && c <= 'Z') {
                  buffer[i] = (char)(c + ('a' - 'A'));
              }
          }
      }

      /* Write out using safe_write to handle partial writes */
      if (safe_write(1, buffer, (size_t)nread) < 0) {
          perror("write");
          exit(1);
      }
  }

  if (nread < 0) {
      perror("read");
      exit(1);
  }

  return 0;
}
