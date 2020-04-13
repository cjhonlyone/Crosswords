all: sumN
	./sumN.exe

sumN: sumN.c
	gcc sumN.c -o sumN.exe

DLX:
	g++ DLX.cpp -o DLX.exe
	g++ DLX_m.cpp -o DLX_m.exe

clean: 
	rm *.exe