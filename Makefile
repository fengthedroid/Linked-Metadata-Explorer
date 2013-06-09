PACKAGE = Ssearch.tar.gz
TAR = tar
INTERPRETER = Python
EXECUTABLE = start.py

install:
	$(TAR) xvfz $(PACKAGE)
	
exec:
	$(INTERPRETER) $(EXECUTABLE)
	
tar:
	$(TAR) cvfz $(PACKAGE) *
	
clean:
	rm $(PACKAGE)