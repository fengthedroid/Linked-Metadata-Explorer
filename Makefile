install:
	tar xvfz Ssearch.tar.gz
	
run:
	Python start.py
	
tar:
	tar cvfz Ssearch.tar.gz *
	
clean:
	rm Ssearch.tar.gz