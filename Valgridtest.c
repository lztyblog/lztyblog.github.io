#include <stdio.h>
#include <stdlib.h>

static void bad_function(int *ptr)
{
    /* 这块内存从来没有被释放 -> 每次调用都会泄漏一次 */
    int *buffer = malloc(10 * sizeof *buffer);

    if (buffer == NULL) {
        /* 偷懒：这里直接返回，不处理 ptr */
        return;
    }

    buffer[0] = 123;      /* 随便用一下，避免 -Wall 报告没用到 */
    *ptr = buffer[0];     /* 读写一下传进来的指针 */

    /* 错误 1：释放调用者传进来的指针 */
    free(ptr);

    /* 错误 2：忘记释放 buffer，造成内存泄漏 */
    /* free(buffer);  // 本来应该有，但我们故意不写 */
}

int main(void)
{
    int *value = malloc(sizeof *value);

    if (value == NULL) {
        fprintf(stderr, "malloc failed\n");
        return 1;
    }

    *value = 42;

    /* 第一次调用：释放了 value，并泄漏了 buffer */
    bad_function(value);

    /* 第二次调用：再次 free 同一个指针 -> invalid free #1 */
    bad_function(value);

    /* use-after-free：value 早就被 free 了，还在用它 */
    printf("value is %d\n", *value);

    /* 再次 free 已经 free 过两次的指针 -> invalid free #2 */
    free(value);

    return 0;
}
