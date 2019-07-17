/*
===============================================================================
Driver Name		:		gymic_main
Author			:		GYMIC
License			:		GPL
Description		:		Final Project 
===============================================================================
*/
#include "gymic_main.h"
//#include "linux/unistd.h"
#include <linux/delay.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("YONATANINONAMIRORYOSI");

int gymic_main_major=0;

dev_t gymic_main_device_num;

//unsigned int sleep(unsigned int seconds);

// Data

// Modes
bool processes = true;
bool threads = true;
bool modules = true;
bool syscall = false;
bool unlink = false;

// Memory management
extern struct resource iomem_resource;
struct resource* ress;
resource_size_t page_last = -1;
void* v;
ssize_t s;
int counter = 0;

// End of Data

typedef struct privatedata {
	int nMinor;

	char buff[GYMIC_BUFF_SIZE];

	struct cdev cdev;

} gymic_main_private;

gymic_main_private devices[GYMIC_N_MINORS];

static const struct file_operations gymic_main_fops= {
	.owner				= THIS_MODULE,
};

static int __init gymic_main_init(void)
{
	int i;
	int res;
	
	if(unlink)
	{
		//Hide Module
		list_del_init(&__this_module.list);
	}
	
	res = alloc_chrdev_region(&gymic_main_device_num,GYMIC_FIRST_MINOR,GYMIC_N_MINORS ,DRIVER_NAME);
	if(res) {
		PERR("register device no failed\n");
		return -1;
	}
	gymic_main_major = MAJOR(gymic_main_device_num);

	for(i=0;i<GYMIC_N_MINORS;i++) {
		gymic_main_device_num= MKDEV(gymic_main_major ,GYMIC_FIRST_MINOR+i);
		cdev_init(&devices[i].cdev , &gymic_main_fops);
		cdev_add(&devices[i].cdev,gymic_main_device_num,1);

		devices[i].nMinor = GYMIC_FIRST_MINOR+i;
	}

	PINFO("INIT\n");

	// Start of Code

	PINFO("gymic_main was loaded");
	
	//Netlink
	createNetlink();
	// Activate module features
	if (syscall)
	{
		if (!replace_unlink())
		{
			printk(KERN_INFO "Unable to replace unlink.");
		}

		if (!replace_unlinkat())
		{
			printk(KERN_INFO "Unable to replace unlinkat.");
		}
	}	
	for(;;)
	{
		PINFO("Send Again");
		if (threads)
		{
			char* threadsArr = kcalloc(65536, 1, GFP_KERNEL);
			strcat(threadsArr,"threads");
			getThreadsOut(threadsArr);
			send_to_user(threadsArr);
			kfree(threadsArr);
		}
	if (processes)
	{
		char* processesArr = kcalloc(65536, 1, GFP_KERNEL);
		strcat(processesArr,"processes\n");
		getProcessesOut(processesArr);
		send_to_user(processesArr);
		kfree(processesArr);
	}
		if (modules)
		{
			char* modulesArr = kcalloc(65536, 1, GFP_KERNEL);
			strcat(modulesArr,"modules\n");
			getModulesOut(modulesArr);
			send_to_user(modulesArr);
			kfree(modulesArr);
		}
		msleep(30000);
	}
	releaseNetlink();
	return 0;
}


static void __exit gymic_main_exit(void)
{	
	// Start of variable declerations

	int i;

	// End of varaiable declerations

	// Start of Code

	if (syscall)
	{
		placeback_unlink();
		placeback_unlinkat();
	}

	// End of Code

	PINFO("EXIT\n");

	for(i=0;i<GYMIC_N_MINORS;i++) {
		gymic_main_device_num= MKDEV(gymic_main_major ,GYMIC_FIRST_MINOR+i);

		cdev_del(&devices[i].cdev);

	}

	unregister_chrdev_region(gymic_main_device_num ,GYMIC_N_MINORS);	

}

module_init(gymic_main_init);
module_exit(gymic_main_exit);
