#include <stdio.h>
#include "../../Helper/include/stopwatch.h"
#include <fstream>
#include <iostream>
#include <cstdio>
#include <iomanip>
using namespace std;

double close_latency(Stopwatch &sw, fstream &fs) {
    sw.start();
    fs.close();
    double close_latency = sw.elapsed_microseconds();
    sw.reset();
    return close_latency;
}

double read_latency(Stopwatch &sw, fstream &fs) {
    fs.seekg(0);
    char buffer[4];
    sw.start();
    fs.read(buffer, 4);
    double read_latency = sw.elapsed_microseconds();
    sw.reset();
    return read_latency;
}

double write_latency(Stopwatch &sw, fstream &fs) {
    sw.start();
    fs.write("Test", 4);
    fs.flush();
    double write_latency = sw.elapsed_microseconds();
    sw.reset();
    return write_latency;
}

double open_latency(Stopwatch &sw, fstream &fs, const char *filename) {
    sw.start();
    fs.open(filename, ios::in | ios::out | ios::trunc);
    double open_latency = sw.elapsed_microseconds();
    sw.reset();
    return open_latency;
}

void run_iterations(int iterations, Stopwatch &sw, fstream &fs, const char *filename, const char *outfile) {
    double open, read, write, close;
    ofstream csv(outfile);
    if (!csv.is_open()) {
        cerr << "Error opening output file" << endl;
        return;
    }
    csv << "Run,Open (µs),Write (µs),Read (µs),Close (µs)" << endl;
    for (int i = 0; i < iterations; i++) {
        open = open_latency(sw, fs, filename);
        write = write_latency(sw, fs);
        read = read_latency(sw, fs);
        close = close_latency(sw, fs);
        csv << i + 1 << "," << open << "," << write << "," << read << "," << close << endl;
        remove(filename);
    }
    csv.close(); 
}

int main() {
    Stopwatch sw;
    const char *tempFileName="tempfile.txt";
    const char *outfile = "latency.csv";
    fstream fs;
    int iterations = 100000;
    cout << "Measuring file operation latencies over " << iterations << " iterations each." << endl;
    run_iterations(iterations, sw, fs, tempFileName, outfile);
    cout << "Finished." << endl;
    return 0;
}
    