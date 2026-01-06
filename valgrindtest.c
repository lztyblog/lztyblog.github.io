#include <stdio.h>
#include <stdlib.h>

static void bad_function(int *ptr)
{
    int *buffer = malloc(10 * sizeof *buffer);
    if (buffer == NULL) {
        return;
    }

    /* do something small with the buffer, but never free it (leak) */
    buffer[0] = 123;

    /* wrong: free memory owned by caller */
    free(ptr);

    /* leak: buffer is not freed */
}

int main(void)
{
    int *value = malloc(sizeof *value);
    if (value == NULL) {
        fprintf(stderr, "malloc failed\n");
        return 1;
    }

    *value = 42;

    bad_function(value);   /* frees value (wrong) + leaks buffer */
    bad_function(value);   /* invalid free + leaks another buffer */

    /* use-after-free (read) */
    printf("value is %d\n", *value);

    /* invalid free (double free) */
    free(value);

    return 0;
}
