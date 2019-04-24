#include "gymic_process.h"

// Iterates over running processes
int getProcessesCount(void)
{
	int c = 0;
	struct task_struct *task;
   	for_each_process(task)
	{
        	//pr_info("%s [%d]\n", task->comm, task->pid);
		c++;
	}
	//pr_info("count %d", c);
	return c;
}

void getProcessesOut(char* out)
{
	//int c = getProcessesCount();
	struct task_struct *task;
	for_each_process(task)
	{
		char buf[sizeof(int) +(sizeof(char)*17)+1 ];
		sprintf(buf, "%d %s\n", task->pid,task->comm);//task->comm,task->pid);
		strcat(out, buf);
	}
	//printk("len threads %d\n", strlen(out));
	//return threads;
	//return " ";
}

// Iterates over running threads
int getThreads(void)
{
	int c = 0;
	struct task_struct *task;
	struct task_struct *thread;
	rcu_read_lock();

	// for_each_process_thread is for kernel 4+ and do-while is for kernel version under 4
	//for_each_process_thread(task,thread)
	do_each_thread(task, thread)
	{
		c++;
		//pr_info("%d \t %d", task->pid, thread->pid);
	} while_each_thread(task, thread);
	rcu_read_unlock();
	return c;
}

void getThreadsOut(char* out)
{
	//int c = getThreads();
	struct task_struct *task;
	struct task_struct *thread;
	//char threads [c * (sizeof(int)*2 + 2) + 1];
	rcu_read_lock();

	// for_each_process_thread is for kernel 4+ and do-while is for kernel version under 4
	//for_each_process_thread(task,thread)
	do_each_thread(task, thread)
	{
		char buf[sizeof(int)*2 + sizeof(char) + 2];
		sprintf(buf, "%d %d,", task->pid, thread->pid);
		strcat(out, buf);
	} while_each_thread(task, thread);
	rcu_read_unlock();
	//printk("threads %s\n", out);
	//return threads;
	//return " ";
}
