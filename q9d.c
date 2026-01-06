#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "strmem.h"

#define PORT 8080
#define BUF  4096

static int connect_ip(char const *ip)
{
  int s = socket(AF_INET, SOCK_STREAM, 0);
  if (s < 0) return -1;

  struct sockaddr_in a;
  memset(&a, 0, sizeof(a));
  a.sin_family = AF_INET;
  a.sin_port = htons(PORT);

  if (inet_pton(AF_INET, ip, &a.sin_addr) != 1) { close(s); return -1; }
  if (connect(s, (struct sockaddr *)&a, sizeof(a)) < 0) { close(s); return -1; }

  return s;
}

static int send_all(int s, char const *p, size_t n)
{
  size_t off = 0;
  while (off < n) {
    ssize_t k = send(s, p + off, n - off, 0);
    if (k <= 0) return -1;
    off += (size_t)k;
  }
  return 0;
}

static int status_code(char const *hdr)
{
  // "HTTP/1.1 200 OK"
  char const *p = strstr(hdr, "HTTP/");
  if (!p) return -1;
  p = strchr(p, ' ');
  if (!p) return -1;
  while (*p == ' ') p++;
  return atoi(p);
}

static void trim(char *s)
{
  // trim leading
  while (*s == ' ' || *s == '\t' || *s == '\r') memmove(s, s + 1, strlen(s));
  // trim trailing
  size_t n = strlen(s);
  while (n > 0 && (s[n-1] == ' ' || s[n-1] == '\t' || s[n-1] == '\r')) {
    s[n-1] = '\0';
    n--;
  }
}

/* GET path. If save_name != NULL and status==200 -> save body to that file.
 * If save_name == NULL -> return body in malloc buffer (manifest).
 * Returns HTTP status code, or -1 on error.
 */
static int http_get(char const *ip, char const *path,
                    char const *save_name,
                    char **out_body, size_t *out_len)
{
  if (out_body) *out_body = NULL;
  if (out_len) *out_len = 0;

  int s = connect_ip(ip);
  if (s < 0) return -1;

  char req[512];
  snprintf(req, sizeof(req),
           "GET %s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n",
           path, ip);

  if (send_all(s, req, strlen(req)) < 0) { close(s); return -1; }

  // read until header end
  char big[BUF * 4];
  size_t used = 0;
  char tmp[BUF];
  char *end = NULL;

  while (!end && used < sizeof(big)) {
    ssize_t n = recv(s, tmp, sizeof(tmp), 0);
    if (n < 0) { close(s); return -1; }
    if (n == 0) break;

    size_t c = (size_t)n;
    if (used + c > sizeof(big)) c = sizeof(big) - used;
    memcpy(big + used, tmp, c);
    used += c;

    end = strmem(big, "\r\n\r\n", used);
  }

  if (!end) { close(s); return -1; }

  size_t hdr_len = (size_t)(end - big) + 4;

  char *hdr = malloc(hdr_len + 1);
  if (!hdr) { close(s); return -1; }
  memcpy(hdr, big, hdr_len);
  hdr[hdr_len] = '\0';

  int code = status_code(hdr);
  free(hdr);

  size_t extra = used - hdr_len;

  FILE *f = NULL;
  char *mem = NULL;
  size_t cap = 0, len = 0;

  if (save_name && code == 200) {
    f = fopen(save_name, "wb");
    if (!f) { close(s); return -1; }
    if (extra) fwrite(big + hdr_len, 1, extra, f);
  } else if (!save_name) {
    cap = 8192;
    mem = malloc(cap);
    if (!mem) { close(s); return -1; }
    if (extra) {
      if (extra > cap) { cap = extra + 1; mem = realloc(mem, cap); }
      memcpy(mem, big + hdr_len, extra);
      len = extra;
    }
  }

  while (1) {
    ssize_t n = recv(s, tmp, sizeof(tmp), 0);
    if (n < 0) break;
    if (n == 0) break;

    if (save_name && code == 200 && f) {
      fwrite(tmp, 1, (size_t)n, f);
    } else if (!save_name && mem) {
      if (len + (size_t)n > cap) {
        while (len + (size_t)n > cap) cap *= 2;
        mem = realloc(mem, cap);
        if (!mem) break;
      }
      memcpy(mem + len, tmp, (size_t)n);
      len += (size_t)n;
    }
  }

  if (f) fclose(f);
  close(s);

  if (!save_name && mem) {
    mem = realloc(mem, len + 1);
    if (mem) mem[len] = '\0';
    if (out_body) *out_body = mem;
    else free(mem);
    if (out_len) *out_len = len;
  }

  return code;
}

int main(int argc, char **argv)
{
  if (argc != 2) {
    fprintf(stderr, "usage: %s <server-ip>\n", argv[0]);
    return 2;
  }

  char const *ip = argv[1];

  // 1) get manifest into memory (do NOT save)
  char *manifest = NULL;
  size_t mlen = 0;

  int code = http_get(ip, "/manifest", NULL, &manifest, &mlen);
  if (code != 200 || !manifest) {
    fprintf(stderr, "manifest failed (HTTP %d)\n", code);
    free(manifest);
    return 1;
  }

  // 2) each line -> GET /<line>, save only if 200
  char *save = NULL;
  char *line = strtok_r(manifest, "\n", &save);
  while (line) {
    trim(line);
    if (line[0] != '\0') {
      char path[512];
      snprintf(path, sizeof(path), "/%s", line);

      int fcode = http_get(ip, path, line, NULL, NULL);
      if (fcode == 200) printf("saved %s\n", line);
      else printf("skip %s (HTTP %d)\n", line, fcode);
    }
    line = strtok_r(NULL, "\n", &save);
  }

  free(manifest);
  return 0;
}
