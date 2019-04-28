#include "gymic_modules.h"

// Iterates over running processes
int getModulesCount(void)
{
	int c = 0;
	struct list_head *list;
    struct module *mod;
    struct module *mine = THIS_MODULE;

    list_for_each(list, &mine->list)
    {
      c++;
    }
	return c;
}

void getModulesOut(char* out)
{
	//int c = getProcessesCount();
	//struct task_struct *task;
	struct list_head *list;
    struct module *mod;
    struct module *mine = THIS_MODULE;

    char buf[40];
    snprintf(buf, 40, "%s\n", &mine->name);
    strcat(out, buf);
    list_for_each(list, &mine->list)
    {
      mod = list_entry(list, struct module, list);
      //char buf[sizeof(int) +(sizeof(char)*17)+1 ];
      char buf[40];
      snprintf(buf, 40, "%s\n", mod->name);
      //printk("%s\n", mod->name);
      //sprintf(buf, "worked\n");
      strcat(out, buf);
    }
	//printk("len threads %d\n", strlen(out));
	//return threads;
	//return " ";
}
