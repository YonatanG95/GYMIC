#include "gymic_modules.h"

// Iterates over modules
void getModulesOut(char* out)
{
	struct list_head *list;
    struct module *mod;
    struct module *mine = THIS_MODULE;

    char buf[40];
    snprintf(buf, 40, "%s\n", &mine->name);
    strcat(out, buf);
    list_for_each(list, &mine->list)
    {
      mod = list_entry(list, struct module, list);
      char buf[40];
      snprintf(buf, 40, "%s\n", mod->name);
      strcat(out, buf);
    }
}
