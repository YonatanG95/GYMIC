#include "gymic_modules.h"

// Iterates over modules
void getModulesOut(char* out)
{
<<<<<<< HEAD
	struct list_head *list;
    struct module *mod;
    struct module *mine = THIS_MODULE;

    char buf[40];
    snprintf(buf, 40, "%s\n", &mine->name);
    strcat(out, buf);
=======
    //Initialize necessary variables
	struct list_head *list;
    struct module *mod;
    struct module *mine = THIS_MODULE;
    char buf[40];

    //Save our moudle name in buffer
    snprintf(buf, 40, "%s\n", &mine->name);
    strcat(out, buf);
    //Iterate through modules list in kernel and saves them in buffer
>>>>>>> 6822e19c7faec9cf86b53209f17710a59e9fa537
    list_for_each(list, &mine->list)
    {
      mod = list_entry(list, struct module, list);
      char buf[40];
      snprintf(buf, 40, "%s\n", mod->name);
      strcat(out, buf);
    }
}
