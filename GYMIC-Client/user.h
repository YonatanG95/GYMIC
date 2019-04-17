#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <linux/netlink.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdbool.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

typedef struct {
    int iPid;
    int iTid;
} Thread;

int open_netlink(void);
void read_event(int sock);
int checkType(char* in);
Thread* parseThreads(char* buffer);
Thread* getUserThreads(void);
int* parseProcesses(char* buffer);
int* getUserProcesses(void);
void compareProc(int* procK, int* procU);
void compareThreads(Thread* threadK, Thread* threadU);



