PACKAGE = semsearch.tar.gz
TAR = tar
INTERPRETER = Python
EXECUTABLE = start.py
# default install directory
# only support one directory level
DIR = semsearch/

# default port is 8000
PORT ?= 8000

install:
	mkdir -p $(DIR)
	$(TAR) xvfz $(PACKAGE) -C $(DIR)
	
exec:
	cd $(DIR) && $(INTERPRETER) $(EXECUTABLE) $(PORT) && cd ..
	
tar:
	cd $(DIR) && $(TAR) cvfz ../$(PACKAGE) * && cd ..
	
clean:
	rm $(PACKAGE)