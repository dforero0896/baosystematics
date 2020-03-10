CC=g++
CFLAGS=-fopenmp
apply_systematics: apply_systematics.cpp
	$(CC) $(CFLAGS) -o apply_systematics apply_systematics.cpp `gsl-config --cflags --libs`
clean:
	rm apply_systematics
