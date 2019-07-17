#include <linux/sched.h>
#include <net/sock.h>
#include <linux/cdev.h>
#include <linux/device.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/kdev_t.h>
#include <linux/module.h>
#include <linux/types.h>
#include <linux/uaccess.h>
#include <linux/printk.h>
#include <linux/kernel.h>
#include <linux/ioport.h>
#include <linux/string.h>
#include <linux/mm.h>
#include <linux/highmem.h>
#include "gymic_syscalls.h"
#include "gymic_process.h"
#include "gymic_modules.h"
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h> 
#include <linux/errno.h> 
#include <linux/types.h>
#include <linux/unistd.h>
#include <asm/cacheflush.h>  
#include <asm/page.h>  
#include <asm/current.h>
#include <linux/sched.h>
#include <linux/kallsyms.h>
#include "netlink.h"

#define DRIVER_NAME "gymic"
#define PDEBUG(fmt,args...) printk(KERN_DEBUG"%s:"fmt,DRIVER_NAME, ##args)
#define PERR(fmt,args...) printk(KERN_ERR"%s:"fmt,DRIVER_NAME,##args)
#define PINFO(fmt,args...) printk(KERN_INFO"%s:"fmt,DRIVER_NAME, ##args)

#define GYMIC_N_MINORS 1
#define GYMIC_FIRST_MINOR 0
#define GYMIC_BUFF_SIZE 1024

static int __init gymic_init(void);
static void __exit gymic_exit(void);
