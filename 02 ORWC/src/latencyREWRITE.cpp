#include <windows.h>
#include <stdio.h>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <cstdint>
#include <utility>
#include "../../Helper/include/stopwatch.h"
using namespace std;

double measure_write_latency(Stopwatch &sw, HANDLE h) {
    sw.start();
    DWORD written;
    WriteFile(h, "Test", 4, &written, NULL);
    //FlushFileBuffers(h);
    double write_latency = sw.elapsed_microseconds();
    sw.reset();
    return written == 4 ? write_latency : -1.0;
}

double measure_read_latency(Stopwatch &sw, HANDLE h) {
    SetFilePointer(h, 0, NULL, FILE_BEGIN);
    char buffer[4];
    DWORD read;
    sw.start();
    ReadFile(h, buffer, 4, &read, NULL);
    double read_latency = sw.elapsed_microseconds();
    sw.reset();
    return read == 4 ? read_latency : -1.0;
}

double measure_close_latency(Stopwatch &sw, HANDLE h) {
    sw.start();
    CloseHandle(h);
    double close_latency = sw.elapsed_microseconds();
    sw.reset();
    return close_latency;
}

void measure_orwc_pipeline(Stopwatch &sw, int iterations, const char *tempfile, const char *outfile) {
    double open, read, write, close;
    ofstream csv(outfile);
    if (!csv.is_open()) {
        cerr << "Error opening output file" << endl;
        return;
    }
    csv << "Run,Open (µs),Write (µs),Read (µs),Close (µs)" << endl;
    for (int i = 0; i < iterations; i++) {
        sw.start();
        HANDLE h = CreateFileA(
            tempfile,
            GENERIC_READ | GENERIC_WRITE,
            0,
            NULL,
            CREATE_ALWAYS,
            FILE_ATTRIBUTE_NORMAL,
            NULL
        );
        open = sw.elapsed_microseconds();
        sw.reset();   
        write = measure_write_latency(sw, h);
        read = measure_read_latency(sw, h);
        close = measure_close_latency(sw, h);
        csv << i + 1 << "," << fixed << setprecision(3) 
            << open << "," << write << "," << read << "," << close << endl;
        remove(tempfile);
    }
    csv.close();
}

int main() {
    Stopwatch sw;
    int iterations = 100000;
    const char *tempfile = "tempfile.txt";
    const char *outfile="latency_win.csv";
    cout << "Measuring file operation latencies over " << iterations << " iterations each." << endl;
    measure_orwc_pipeline(sw, iterations, tempfile, outfile);
    cout << "Finished." << endl;
    return 0;
}
