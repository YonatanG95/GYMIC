obj-m		:= gymic.o

gymic-objs := gymic_main.o gymic_syscalls.o gymic_process.o netlink.o

KERN_SRC	:= /lib/modules/$(shell uname -r)/build/
KVER ?= $(shell uname -r)
PWD			:= $(shell pwd)

modules:
	make -C $(KERN_SRC) M=$(PWD) modules
	make -C $(PWD)/Lime M=$(PWD) symbols
	mv $(PWD)/Lime/lime-$(KVER).ko $(PWD)/lime.ko

install:
	make -C $(KERN_SRC) M=$(PWD) modules_install
	depmod -a

clean:
	make -C $(KERN_SRC) M=$(PWD) clean
