#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "../../Helper/include/Cstopwatch.h"

double close_latency(Stopwatch *sw, HANDLE h) {
    start(sw);
    CloseHandle(h);
    double close_latency = elapsed_microseconds(sw);
    reset(sw);
    return close_latency;
}

double read_latency(Stopwatch *sw, HANDLE h) {
    SetFilePointer(h, 0, NULL, FILE_BEGIN);
    char buffer[4];
    start(sw);
    DWORD read;
    ReadFile(h, buffer, 4, &read, NULL);
    double read_latency = elapsed_microseconds(sw);
    reset(sw);
    return read == 4 ? read_latency : -1.0;
}

double write_latency(Stopwatch *sw, HANDLE h) {
    DWORD written;
    start(sw);
    WriteFile(h, "Test", 4, &written, NULL);
    //FlushFileBuffers(h);
    double write_latency = elapsed_microseconds(sw);
    reset(sw);
    return written == 4 ? write_latency : -1.0;
}

void run_iterations(int iterations, Stopwatch *sw, const char *filename, const char *outfile) {
    double open, read, write, close;
    FILE *file = fopen(outfile, "w");
    if (file == NULL) {
        printf("Error opening output file\n");
        return;
    }
    fprintf(file, "Run,Open,Write,Read,Close\n");
    HANDLE h = CreateFileA(
            filename,
            GENERIC_READ | GENERIC_WRITE,
            0,
            NULL,
            CREATE_ALWAYS,
            FILE_ATTRIBUTE_NORMAL,
            NULL
    );
    CloseHandle(h);
    for (int i = 0; i < iterations; i++) {
        start(sw);
        HANDLE h = CreateFileA(
            filename,
            GENERIC_READ | GENERIC_WRITE,
            0,
            NULL,
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL,
            NULL
        );
        open = elapsed_microseconds(sw);
        reset(sw);        
        write = write_latency(sw, h);
        read = read_latency(sw, h);
        close = close_latency(sw, h);
        
        fprintf(file, "%d,%.3f,%.3f,%.3f,%.3f\n", i + 1, open, write, read, close);
        
        //remove(filename);
    }
    remove(filename);
    fclose(file); 
}

int main() {
    Stopwatch sw = stopwatch();
    const char *tempFileName = "tempfile.txt";
    const char *outfile = "../Results/latencyWinAPIc.csv";
    int iterations = 100000;
    printf("Measuring file operation latencies over %d iterations each.\n", iterations);
    run_iterations(iterations, &sw, tempFileName, outfile);
    printf("Finished.\n");
    return 0;
}
