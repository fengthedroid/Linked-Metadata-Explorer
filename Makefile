PACKAGE = Ssearch.tar.gz
TAR = tar
INTERPRETER = Python
EXECUTABLE = start.py
# default port is 8000
PORT ?= 8000

install:
	$(TAR) xvfz $(PACKAGE)
	
exec:
	$(INTERPRETER) $(EXECUTABLE) $(PORT)
	
tar:
	$(TAR) cvfz $(PACKAGE) *
	
clean:
	rm $(PACKAGE)