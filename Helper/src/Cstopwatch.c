#include "../include/Cstopwatch.h"

Stopwatch stopwatch() {
    Stopwatch sw;
    QueryPerformanceFrequency(&sw.frequency_);
    return sw;
}

void start(Stopwatch *sw) {
    QueryPerformanceCounter(&sw->start_time_);
    sw->is_running_ = true;
}

void reset(Stopwatch *sw) {
    sw->start_time_ = (LARGE_INTEGER){0};
    sw->is_running_ = false;
}

double elapsed_microseconds(Stopwatch *sw) {
    QueryPerformanceCounter(&sw->end_time_);
    sw->elapsed_ = (double)(sw->end_time_.QuadPart - sw->start_time_.QuadPart);
    return (sw->elapsed_ / sw->frequency_.QuadPart) * 1000000.0;
}

bool is_running(Stopwatch *sw) {
    return sw->is_running_;
}