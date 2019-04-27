#include "user.h"

/* Protocol family, consistent in both kernel prog and user prog. */
#define MYPROTO NETLINK_USERSOCK
/* Multicast group, consistent in both kernel prog and user prog. */
#define MYMGRP 21

#define TCP_SERVER_IP "192.168.254.1"
#define LIME_PORT 1235

#define SLEEP_INTERVAL 500000

int open_netlink(void)
{
    int sock;
    struct sockaddr_nl addr;
    int group = MYMGRP;

    sock = socket(AF_NETLINK, SOCK_RAW, MYPROTO);
    if (sock < 0) {
        printf("sock < 0.\n");
        return sock;
    }

    memset((void *) &addr, 0, sizeof(addr));
    addr.nl_family = AF_NETLINK;
    addr.nl_pid = getpid();

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

void read_event(int sock)
{
    struct sockaddr_nl nladdr;
    struct msghdr msg;
    struct iovec iov;
    char buffer[65536];
    char saveBuff[65536];
    int ret;
	
    iov.iov_base = (void *) buffer;
    iov.iov_len = sizeof(buffer);
    msg.msg_name = (void *) &(nladdr);
    msg.msg_namelen = sizeof(nladdr);
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;
	
    //printf("Ok, listening.\n");
    ret = recvmsg(sock, &msg, 0);
    if (ret < 0)
        printf("ret < 0.\n");
    else
    {
	//char buffer[65536];
	//printf("nl %s", NLMSG_DATA((struct nlmsghdr *) &buffer));
	sprintf(buffer, "%s", NLMSG_DATA((struct nlmsghdr *) &buffer));
	//printf("buf %s", buffer);
	int type = checkType(buffer);
	memcpy(saveBuff, buffer, 65536);
	//printf("%s", buffer);
	if(type == 1)
	{
		
		//int* processesK = parseProcesses(buffer);
		getUserProcesses();
		char kernProcTag[16] = "kernelProcesses";
		sendOverSocket(buffer, kernProcTag);
		printf("%s\n","got the user processes");
		int* networkU = getUserNetwork();
		printf("%s\n","got the user Network");
		int* modulesU = getUserModules();
		printf("%s\n","got the user Modules");
		char finishProcTag[19] = "gymic_finish_proc";
		char finish[7] = "finish";
		sendOverSocket(finish, finishProcTag);

		//compareProc(processesK, processesU);
	}
	if(type == 2)
	{
		//Thread* threadsK = parseThreads(saveBuff);
		getUserThreads();
		char kernThreadTag[14] = "kernelThreads";
		sendOverSocket(buffer, kernThreadTag);
		char finishThreadTag[21] = "gymic_finish_thread";
		char finish[7] = "finish";
		sendOverSocket(finish, finishThreadTag);
		//compareThreads(threadsK, threadsU);
	}
    } 
}

int checkType(char* in)
{
	
	if(strncmp(in, "processes", strlen("processes")) == 0)
	//if(strstr(in, "processes"))
	{
		return 1;
	}
	//if(strstr(in, "threads"))
	if(strncmp(in, "threads", strlen("threads")) == 0)	
	{
		return 2;
	}
	return 0;
}

Thread* parseThreads(char* buffer)
{
	char subbuff[5];
	memcpy(subbuff, buffer, strstr(buffer, "threads")-buffer);
	int len = atoi(subbuff);
	Thread* threads = (Thread*)malloc(sizeof(Thread) * len + 1);
	buffer = strstr(buffer, "threads") + 7;
	int i = 0;
	char *pt; 
    	pt = strtok (buffer,",");
    	while (pt != NULL) {
		char pid[sizeof(pt)];
		char tid[sizeof(pt)];
		char* sub = strstr(pt, " ");
		memcpy(pid, pt, sub-pt);
		memcpy(tid, sub + 1, strlen(sub));
		int pidInt = atoi(pid);	
        	int tidInt = atoi(tid);
		threads[i].iPid = pidInt;
		threads[i].iTid = tidInt;
        	pt = strtok (NULL, ",");
		i++;
	}
	return &threads[0];	
}

Thread* getUserThreads(void)
{
	FILE *in=NULL;
	char *ln = NULL;
	size_t len = 0;
   	char temp[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	memset(temp, 0 , sizeof(temp));
	char buf123[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	memset(buf123, 0 , sizeof(buf123));	
	char userThreadTag[12] = "userThreads";
   	Thread thrlist[65536];
   	in=popen("ps -AT -o pid:1,spid:1", "r");
  	//fgets(temp, 255, in);
	//char* prev[255];
	//fgets(temp, 255, in);
	int i = 0;
	for(i = 0; i < 65536; i++)
	{
		thrlist[i].iPid = -1;
		thrlist[i].iTid = -1;
	}
	i = 0;
	while(fgets(temp,sizeof(temp),in) !=NULL)
	{
		//strcat(temp," userThread");
		//printf("%s\n",temp);
		//i++;
		//printf("%d\n", i);
		strcat(buf123,temp);
	}
	/*while(strcmp(temp,prev) != 0)
	{
		strcpy(prev, temp);
		char subbuff[255];
		char pid[255];
		char tid[255];
		memcpy(subbuff, temp, strstr(temp, "\n")-temp);
		char* space = strstr(subbuff, " ");
		memcpy(pid, subbuff, space-subbuff);
		int pidInt = atoi(pid);
		memcpy(tid, space + 1, strlen(subbuff) - strlen(space));
		int tidInt = atoi(tid);
		thrlist[i].iPid = pidInt;
		thrlist[i].iTid = tidInt;
		fgets(temp, 255, in);
		i++;
	}	
	Thread* thrres = (Thread*)malloc(sizeof(Thread) * i + 1);
	for(int k = 0; k < i; k++)
	{
		thrres[k].iPid = thrlist[k].iPid;
		thrres[k].iTid = thrlist[k].iTid;
	}*/
	sendOverSocket(buf123, userThreadTag);
	//free(ln);
	pclose(in);
	//free(in);
	//strcat(buf123,"\0");
	//return &thrres[0];*/
	return 0;
}

void compareThreads(Thread* threadK, Thread* threadU)
{
	printf("****** Threads ******\n");
	bool equal = true;
	int cK = 0;
	int cU = 0;
	printf("K-Pid\tK-Tid\tU-Pid\tU-Tid\n");
	while(threadK[0].iPid != NULL && threadU[0].iPid != NULL)
	{
		cK++;
		cU++;
		//printf("%d\t%d\t%d\t%d\n", threadK[0].iPid, threadK[0].iTid, threadU[0].iPid, threadU[0].iTid);
		if(threadK[0].iPid != threadU[0].iPid || threadK[0].iTid != threadU[0].iTid)
			equal = false;
		threadK++;
		threadU++;
	}
	if(threadK[0].iPid != NULL)
	{
		while(threadK[0].iPid != NULL)
		{
			cK++;
			printf("%d\t%d\n", threadK[0].iPid, threadK[0].iTid);
			threadK++;
		}
	}
	else if(threadU[0].iPid != NULL)
	{
		while(threadU[0].iPid != NULL)
		{
			cU++;
			printf("\t\t%d\t%d\n", threadU[0].iPid, threadU[0].iTid);
			threadU++;
		}
	}
	else
	{
		printf("*\t*\t*\t*\n");
	}
	printf("Kernel threads count: %d\nUser threads count: %d\n", cK, cU);
	printf("Found confict: %s\n", equal ? "false" : "true");
	printf("*********************\n");

}
int* parseProcesses(char* buffer)
{
	char subbuff[5];
	memcpy(subbuff, buffer, strstr(buffer, "processes")-buffer);
	int len = atoi(subbuff);
	int* processes = malloc(sizeof(int) * len + 1);
	buffer = strstr(buffer, "processes") + 9;
	int i = 0;
	char *pt;
    	pt = strtok (buffer,",");
    	while (pt != NULL) {
        	int a = atoi(pt);
		processes[i] = a;
        	pt = strtok (NULL, ",");
		i++;
	}
	return &processes[0];
}

int* getUserProcesses(void)
{	
   	FILE *in2=NULL;
   	char temp2[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	memset(temp2, 0 , sizeof(temp2));
	char buf1234[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	memset(buf1234, 0 , sizeof(buf1234));
   	int* prolist[65536];
	char userProcTag[12] = "userProcess";
   	//in=popen("ps -Ao pid:1", "r");
	in2=popen("ps -Ao pid:1,comm:2", "r");
	//in=popen("netstat", "r");
  	//fgets(temp, 255, in);
	//char* prev[255];
	//fgets(temp, 255, in);
	//printf("%s",in);
	//pclose(in);
	int i = 0;
	for(i = 0; i < 65536; i++)
	{
		prolist[i] = -1;
	}
	i = 0;
	//strcpy(buf123 , "");
	while(fgets(temp2,sizeof(temp2),in2) !=NULL)
	{
		//printf("%s\n",temp);
		//i++;
		//printf("%d\n", i);
		strcat(buf1234,temp2);
	}
	//strcat(buf123 , "");
	//printf("%s",buf1234);
	sendOverSocket(buf1234, userProcTag);
	
	/*while(strcmp(temp,prev) != 0)
	{
		strcpy(prev, temp);
		char subbuff[8192];
		memcpy(subbuff, temp, strstr(temp, "\n")-temp);
		int pid = atoi(subbuff);
		prolist[i] = pid;
		fgets(temp, 8192, in);
		i++;
	}	
	int* prores = malloc(sizeof(int) * i + 1);
	for(int k = 0; k < i; k++)
	{
		prores[k] = prolist[k];
	}*/
	//return &prores[0];
	return 0;
}

int* getUserNetwork(void)
{
   	FILE *in=NULL;
   	char temp[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	char buf12[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	//in=popen("ps -Ao pid:1,comm:2", "r");
	in=popen("netstat -naptu", "r");
	int i = 0;
	while(fgets(temp,sizeof(temp),in) !=NULL)
	{
		//printf("%s\n",temp);
		//i++;
		//printf("%d\n", i);
		strcat(buf12,temp);
	}
	printf("%s\n",buf12);
	sendOverSocket(buf12);
	return 0;
}

int* getUserModules(void)
{
   	FILE *in=NULL;
   	char temp[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	char buf12[65536*(sizeof(int)+(sizeof(char)*17)+1)];
	//in=popen("ps -Ao pid:1,comm:2", "r");
	in=popen("lsmod", "r");
	int i = 0;
	while(fgets(temp,sizeof(temp),in) !=NULL)
	{
		//printf("%s\n",temp);
		//i++;
		//printf("%d\n", i);
		strcat(buf12,temp);
	}
	printf("%s\n",buf12);
	sendOverSocket(buf12);
	return 0;
}

void compareProc(int* procK, int* procU)
{
	printf("****** Processes ******\n");
	bool equal = true;
	int cK = 0;
	int cU = 0;
	printf("Kernel\tUser\n");
	while(procK[0] != 0 && procU[0] != 0)
	{
		cK++;
		cU++;
		//printf("%d\t%d\n", procK[0], procU[0]);
		if(procK[0] != procU[0])
			equal = false;
		procK++;
		procU++;
	}
	if(procK[0] != 0)
	{
		while(procK[0] != 0)
		{
			cK++;
			printf("%d\n", procK[0]);
			procK++;
		}
	}
	else if(procU[0] != 0)
	{
		while(procU[0] != 0)
		{
			cU++;
			printf("\t%d\n", procU[0]);
			procU++;
		}
	}
	else
	{
		printf("*\t*\n");
	}
	printf("Kernel processes count: %d\nUser processes count: %d\n", cK, cU);
	printf("Found confict: %s\n", equal ? "false" : "true");
	printf("***********************\n");
}
void sendOverSocket(char* data, char* tag)
{	
	int sock;
	struct sockaddr_in server;
	char server_reply[2000];
	//strcat(tag, "\n");
	strcat(tag,data);
	printf("%s", tag);
	//Create Socket
	usleep(SLEEP_INTERVAL);
	sock = socket(AF_INET , SOCK_STREAM , 0);
	if (sock == -1 )
	{
		printf("Could not create socket");
	}
	puts("Socket created");
	
	//server.sin_addr.s_addr = inet_addr("192.168.1.246");
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

	
		//printf("Enter message :");
		//scanf("%s", message);

		//send some data
	if( send(sock , tag , strlen(tag) , 0) < 0 )
	{
		puts("Send failed");
		return 1;
	}
		
	//REcieve a reply from the server
	//if( recv(sock , server_reply, 2000, 0) < 0)
	//{
	//	puts("recv failed");
	//	
	//}
	//puts("Server reply:");
	//puts(server_reply);
	
	close(sock);
	puts("Socket Closed\n");
	return 0;
}

void socketForMemdump()
{
#include<stdio.h>
#include<string.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include<unistd.h>

int main(int argc , char *argv[])
{
	int socket_desc , client_sock, c , read_size;
	struct sockaddr_in server , client;
	char client_message[2000];

	//Create socket
	socket_desc = socket(AF_INET, SOCK_STREAM , 0);
	if (socket == -1)
	{
		printf("Could not create socket")
	}
	puts("Socket created")
	//Prepare the sockaddr_in structure
	server.sin_family = AF_INET;
	server.sin_addr.s_addr = INADDR_ANY;
	server.sin_port=htons(8888);

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


	//Recieve a message from client
	while( (read_size = recv(client_sock, client_message , 2000 , 0)) > 0)
	{
		if (strcmp(client_message,"yes")==0)
		{
            take_dump()
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

	return 0;
}


void take_dump() {
    int fd;
    size_t image_size;
    struct stat st;
    void *image;
    char cwd[PATH_MAX];
    char ko_module[9] = "/lime.ko";
    char params[26];
    sprintf(params, "%s%d%s", "path=tcp:", LIME_PORT, " format=lime");


    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        strcat(cwd, ko_module);
        fd = open(cwd, O_RDONLY);
        fstat(fd, &st);
        image_size = st.st_size;
        image = malloc(image_size);
        read(fd, image, image_size);
        close(fd);
        if (init_module(image, image_size, params) != 0) {
            printf("Error loading module.\n");
        }
        else {
            printf("Loaded module successfully.\n");
        }
        free(image);
    }
    else {
        printf("getcwd failed.\n");
    }
}

int main(int argc, char *argv[])
{	
   
    int nls;
    nls = open_netlink();
    if (nls < 0)
        return nls;

    printf("$$$$ WELCOME $$$$\nDon't forget to choose parameters in main file!\nPlease insert the module!\n");
    for (;;)
        read_event(nls);
	
    return 0;
}
