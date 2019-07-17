#include "user.h"
#include <unistd.h>

/* Protocol family, consistent in both kernel prog and user prog. */
#define MYPROTO NETLINK_USERSOCK
/* Multicast group, consistent in both kernel prog and user prog. */
#define MYMGRP 21

<<<<<<< HEAD
=======
// Define constant variables
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
#define TCP_SERVER_IP "192.168.17.1"
#define LIME_PORT 1235
#define SLEEP_INTERVAL 500000

<<<<<<< HEAD
double dumpPeriod = 14;
=======
double dumpPeriod = 16;
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537



int open_netlink(void)
{
    // Initialize variable
    int sock;
    struct sockaddr_nl addr;
    int group = MYMGRP;

    // Creating socket
    sock = socket(AF_NETLINK, SOCK_RAW, MYPROTO);
    if (sock < 0) {
        printf("sock < 0.\n");
        return sock;
    }

    memset((void *) &addr, 0, sizeof(addr));
    addr.nl_family = AF_NETLINK;
    addr.nl_pid = getpid();

    // Bind socket
    if (bind(sock, (struct sockaddr *) &addr, sizeof(addr)) < 0) {
        printf("bind < 0.\n");
        return -1;
    }

    if (setsockopt(sock, 270, NETLINK_ADD_MEMBERSHIP, &group, sizeof(group)) < 0) {
        printf("setsockopt < 0\n");
        return -1;
    }

    return sock;
}

// Get the Data from kernel, Collect the data from user and send it to remote server
void read_event(int sock)
{
    // Initialize variables
    struct sockaddr_nl nladdr;
    struct msghdr msg;
    struct iovec iov;
    char buffer[65536];
<<<<<<< HEAD
    //buffer[0] = '\0';
=======
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
    int ret;
	
    iov.iov_base = (void *) buffer;
    iov.iov_len = sizeof(buffer);
    msg.msg_name = (void *) &(nladdr);
    msg.msg_namelen = sizeof(nladdr);
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;
<<<<<<< HEAD
	
=======

	// Get data from the kernel
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
    ret = recvmsg(sock, &msg, 0);
    if (ret < 0)
        printf("ret < 0.\n");
    else
    {
	sprintf(buffer, "%s", NLMSG_DATA((struct nlmsghdr *) &buffer));
<<<<<<< HEAD
	int type = checkType(buffer);

	
	
	//char header[9] = "headerTag";
	
	
	
	
	if(type == 1)
	{
		
		//sendOverSocket("", header);
=======
	// Check the data type and enter the corresponding routine
	int type = checkType(buffer);
	
	// The data sent from kernel is processes
	if(type == 1)
	{

>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
		char kernProcTag[16] = "kernelProcesses";
		// Send kernel processes to remote server
		sendOverSocket(buffer, kernProcTag);
		char footer[7] = "EndData";
		sendOverSocket("", footer);
		sleep(1);
<<<<<<< HEAD
		getUserProcesses();
		//sendOverSocket("", header);
=======
		// Collect and Send user processes to remote server
		getUserProcesses();
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
		char finishProc[7] = "finish";
		char finishProcTag[19] = "gymic_finish_proc";
		sendOverSocket(finishProc, finishProcTag);
		sendOverSocket("", footer);
<<<<<<< HEAD
		getUserNetwork();
		//sendOverSocket("", header);
=======

		// Collect and Send user network to remote server
		getUserNetwork();
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
		char finishNet[7] = "finish";
		char finishNetworkTag[17] = "gymic_finish_net";
		sendOverSocket(finishNet, finishNetworkTag);
		sendOverSocket("", footer);
		sleep(1);
		// Open a listener and wait for a message to see if memdump is 			needed
        	socketForMemdump();
		sleep(1);
		
	}
	// The data sent from kernel is Threads
	if(type == 2)
	{
		char footer[7] = "EndData";
<<<<<<< HEAD
		//sendOverSocket("", header);		
=======
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
		char kernThreadTag[14] = "kernelThreads";
		// Send kernel threads to remote server
		sendOverSocket(buffer, kernThreadTag);
		sendOverSocket("", footer);
		sleep(1);
<<<<<<< HEAD
		getUserThreads();
		//sendOverSocket("", header);
=======
		// Collect and Send user threads to remote server
		getUserThreads();
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
		char finishThreadTag[21] = "gymic_finish_thread";
		char finishThread[7] = "finish";
		sendOverSocket(finishThread, finishThreadTag);
		sendOverSocket("", footer);
		sleep(1);
<<<<<<< HEAD
	}
	if(type == 3)
	{
		char footer[7] = "EndData";
		//sendOverSocket("", header);
		char kernModuleTag[14] = "kernelModules";
		sendOverSocket(buffer, kernModuleTag);
		sendOverSocket("", footer);
		sleep(1);
		getSysModules();
		getUserModules();
		//sendOverSocket("", header);
		char finishMod[7] = "finish";
		char finishModuleTag[17] = "gymic_finish_mod";
		sendOverSocket(finishMod, finishModuleTag);
		sendOverSocket("", footer);
		// Open a listener and wait for a message to see if memdump is 			needed
        	socketForMemdump();
		sleep(1);
	}
=======
	}
	// The data sent from kernel is modules
	if(type == 3)
	{
		char footer[7] = "EndData";
		char kernModuleTag[14] = "kernelModules";
		// Send kernel modules ro remote server
		sendOverSocket(buffer, kernModuleTag);
		sendOverSocket("", footer);
		sleep(1);
		// Collect and Send sys modules to remote server
		getSysModules();
		// Collect and Send user modules to remote server
		getUserModules();
		char finishMod[7] = "finish";
		char finishModuleTag[17] = "gymic_finish_mod";
		sendOverSocket(finishMod, finishModuleTag);
		sendOverSocket("", footer);
		// Open a listener and wait for a message to see if memdump is 			needed
        	socketForMemdump();
		sleep(1);
	}
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
    }
}

// Check data type sent from kernel
int checkType(char* in)
{

	if(strncmp(in, "processes", strlen("processes")) == 0)
	{
		return 1;
	}
	if(strncmp(in, "threads", strlen("threads")) == 0)	
	{
		return 2;
	}
	if(strncmp(in, "modules", strlen("modules")) == 0)
	{
		return 3;
	}
	return 0;
}
// Collect and send threads from user mode
Thread* getUserThreads(void)
{
    // Initialize variables
	FILE *in=NULL;
	char *ln = NULL;
	size_t len = 0;
   	char temp[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	memset(temp, 0 , sizeof(temp));
	char buf123[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	memset(buf123, 0 , sizeof(buf123));	
	char userThreadTag[12] = "userThreads";
   	Thread thrlist[65536];
   	// Get threads
   	in=popen("ps -AT -o pid:1,spid:1", "r");

	int i = 0;
	for(i = 0; i < 65536; i++)
	{
		thrlist[i].iPid = -1;
		thrlist[i].iTid = -1;
	}
	i = 0;
	while(fgets(temp,sizeof(temp),in) !=NULL)
	{

		strcat(buf123,temp);
	}
	char footer[7] = "EndData";
<<<<<<< HEAD
	//char header[9] = "headerTag";
	//sendOverSocket("", header);
=======
	// Send threads
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
	sendOverSocket(buf123, userThreadTag);
	sendOverSocket("", footer);
	pclose(in);
	return 0;
}

<<<<<<< HEAD
=======
// Collect and send processes from user mode
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
int* getUserProcesses(void)
{
    // Initialize variables
   	FILE *in2=NULL;
   	char temp2[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	memset(temp2, 0 , sizeof(temp2));
	char buf1234[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	memset(buf1234, 0 , sizeof(buf1234));
   	int* prolist[65536];
	char userProcTag[12] = "userProcess";
<<<<<<< HEAD
=======
	// Get processes
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
	in2=popen("ps -Ao pid:1,\%cpu:1,comm,user", "r");
	int i = 0;
	for(i = 0; i < 65536; i++)
	{
		prolist[i] = -1;
	}
	i = 0;
	while(fgets(temp2,sizeof(temp2),in2) !=NULL)
	{
		strcat(buf1234,temp2);
	}
	char footer[7] = "EndData";
<<<<<<< HEAD
	//char header[9] = "headerTag";
	//sendOverSocket("", header);
=======
	// Send processes
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
	sendOverSocket(buf1234, userProcTag);
	sendOverSocket("", footer);
	return 0;
}

<<<<<<< HEAD
int* getUserNetwork(void)
{
=======
// Collect and send network data from user mode
int* getUserNetwork(void)
{
    //Initialize variables
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
   	FILE *in=NULL;
   	char temp[65536*(sizeof(int)+(sizeof(char)*17)+1)];
   	memset(temp, 0 , sizeof(temp));
	char buf12[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	memset(buf12, 0 , sizeof(buf12));
<<<<<<< HEAD
=======
	// Get network data
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
	in=popen("netstat -naptu", "r");
	char userNetTag[12] = "userNetwork";
	int i = 0;
	while(fgets(temp,sizeof(temp),in) !=NULL)
	{
		strcat(buf12,temp);
	}
	char footer[7] = "EndData";
<<<<<<< HEAD
	//char header[9] = "headerTag";
	//sendOverSocket("", header);
=======
	// Send network data
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
	sendOverSocket(buf12, userNetTag);
	sendOverSocket("", footer);
	return 0;
}

<<<<<<< HEAD
=======
// Collect and send modules from user mode
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
int* getUserModules(void)
{
   	FILE *in=NULL;
   	char temp[65536*(sizeof(int)+(sizeof(char)*17)+1)];
   	memset(temp, 0 , sizeof(temp));
	char buf12[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	memset(buf12, 0 , sizeof(buf12));
<<<<<<< HEAD
=======
	// Get modules
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
	in=popen("lsmod", "r");
	int i = 0;
	char userModTag[12] = "userModule";
	while(fgets(temp,sizeof(temp),in) !=NULL)
	{
		strcat(buf12,temp);
	}
	char footer[7] = "EndData";
<<<<<<< HEAD
	//char header[9] = "headerTag";
	//sendOverSocket("", header);
=======
	// Send modules
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
	sendOverSocket(buf12, userModTag);
	sendOverSocket("", footer);
	return 0;
}

<<<<<<< HEAD

=======
// Send the collected Data to remote server
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
void sendOverSocket(char* data, char* tag)
{	
	int sock;
	struct sockaddr_in server;
	char server_reply[2000];
	printf("%s", tag);
	strcat(tag,data);
	//Create Socket
	usleep(SLEEP_INTERVAL);
	sock = socket(AF_INET , SOCK_STREAM , 0);
	if (sock == -1 )
	{
		printf("Could not create socket");
	}
	puts("Socket created");
	
	server.sin_addr.s_addr = inet_addr(TCP_SERVER_IP);
	server.sin_family = AF_INET;
	server.sin_port = htons (1234);

	//connect to remote server
	if(connect(sock , (struct sockaddr *)&server, sizeof(server)) < 0)
	{
		perror("connection failed, error");
		return 1;
	}
	puts("Connected\n");
	
	//keep communicating with server

	//send some data
	if( send(sock , tag , strlen(tag) , 0) < 0 )
	{
		puts("Send failed");
		return 1;
	}
		
	close(sock);
	puts("Socket Closed\n");
	return 0;
}

<<<<<<< HEAD
int socketForMemdump()
{
	//Change to activate / deactivate memory dump
	dumpPeriod = dumpPeriod + 0.5;
	if (dumpPeriod < 15)
=======
// Check if memory dump is necessary and act accordingly
int socketForMemdump()
{
	//Change to activate / deactivate memory dump
	dumpPeriod = dumpPeriod + 0;
	if (dumpPeriod < 15000000)
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
   	{
        return 0;
    	}
	int socket_desc , client_sock, c , read_size;
	struct sockaddr_in server , client;
	char client_message[10];
	memset(client_message, 0, sizeof(client_message));


	//Create socket
	socket_desc = socket(AF_INET, SOCK_STREAM , 0);
	if (socket == -1)
	{
		printf("Could not create socket");
	}
	printf("Socket created");
	//Prepare the sockaddr_in structure
	server.sin_family = AF_INET;
	server.sin_addr.s_addr = INADDR_ANY;
	server.sin_port=htons(LIME_PORT);

	//Bind
	if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0)
	{
		//print the error message
		perror("bind failed. error");
		return 1;
	}


	//Listen
	listen(socket_desc , 3);

	//Accept and incoming connection

	c = sizeof(struct sockaddr_in);

	//accept connection from an incoming client
	client_sock = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c);
	if (client_sock < 0)
	{
		perror("accept failed");
		return 1;
	}

    read_size = recv(client_sock, client_message , 2000 , 0);

	//Recieve a message from client
	if( read_size > 0)
	{
		if (strcmp(client_message,"Yes")==0)
		{
		    dumpPeriod = 0;
		    close(client_sock);
		    close(socket_desc);
            take_dump();
		}

		//send the message back to client
		write(client_sock , client_message , strlen(client_message));
	}

	if(read_size == 0)
	{
		puts("Client disconnected");
		fflush(stdout);
	}
	else if(read_size == -1)
	{
		perror("recv failed");
	}
    close(socket_desc);
	return 0;
	
}

<<<<<<< HEAD

=======
// Collect memory dump
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
void take_dump() {
    // Initialize variables
    int fd;
    size_t image_size;
    struct stat st;
    void *image;
    char cwd[PATH_MAX];
    char ko_module[9] = "/lime.ko";
    char params[26];
    sprintf(params, "%s%d%s", "path=tcp:", LIME_PORT, " format=lime");

    // Use Lime to take memory dump
    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        strcat(cwd, ko_module);
        fd = open(cwd, O_RDONLY);
        fstat(fd, &st);
        image_size = st.st_size;
        image = malloc(image_size);
        read(fd, image, image_size);
        close(fd);
        if (init_module(image, image_size, params) != 0) {
            printf("Error loading module - %s.\n", strerror(errno));
        }
        else {
            printf("Loaded module successfully.\n");
        }
        free(image);
        if (delete_module("lime", O_NONBLOCK) != 0) {
            printf("Error removing module - %s.\n", strerror(errno));
        }
        else {
            printf("Removed module successfully\n");
        }
    }
    else {
        printf("getcwd failed.\n");
    }
}

<<<<<<< HEAD
int* getSysModules(void)
{
=======
// Collect and send modules from the directory /sys/module
int* getSysModules(void)
{
    // Initialize variables
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
   	FILE *in=NULL;
   	char temp[65536*(sizeof(int)+(sizeof(char)*17)+1)];
   	memset(temp, 0 , sizeof(temp));
	char buf12[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	memset(buf12, 0 , sizeof(buf12));
<<<<<<< HEAD
	//in=popen("ps -Ao pid:1,comm:2", "r");
=======
	// Get modules
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
	in=popen("ls /sys/module/*/initstate | sed -e 's/^\\/sys\\/module\\///' -e 's/\\/initstate$//'", "r");
	int i = 0;
	char sysModTag[12] = "sysModule";
	while(fgets(temp,sizeof(temp),in) !=NULL)
	{
<<<<<<< HEAD
		//printf("%s\n",temp);
		//i++;
		//printf("%d\n", i);
		strcat(buf12,temp);
	}
	//printf("%s\n",buf12);
	char footer[7] = "EndData";
	//strcat(buf12, footer);
=======
		strcat(buf12,temp);
	}
	char footer[7] = "EndData";
	// Send modules
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
	sendOverSocket(buf12, sysModTag);
	sendOverSocket("", footer);
	return 0;
}

int main(int argc, char *argv[])
{	
    // Open netlink
    int nls;
    nls = open_netlink();
    if (nls < 0)
        return nls;

    printf("Agent started...\nChoose parameters in main file!\nPlease insert the module!\n");
<<<<<<< HEAD
=======
    // Enter infinite loop of read_event
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
    for (;;)
        read_event(nls);
	
    return 0;
}
