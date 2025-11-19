#ifndef CSTOPWATCH
#define CSTOPWATCH

#include <windows.h>
#include <stdbool.h>

typedef struct {
    LARGE_INTEGER start_time_;
    LARGE_INTEGER end_time_;
    LARGE_INTEGER frequency_;
    double elapsed_;
    bool is_running_;
} Stopwatch;

Stopwatch stopwatch();
void start(Stopwatch *sw);
void reset(Stopwatch *sw);
double elapsed_microseconds(Stopwatch *sw);
bool is_running(Stopwatch *sw);

#endif // CSTOPWATCH