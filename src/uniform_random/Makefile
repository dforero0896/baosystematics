CC=g++
CFLAGS=-fopenmp
uniform_random: uniform_random.cpp
	$(CC) $(CFLAGS) -o uniform_random.o uniform_random.cpp `gsl-config --cflags --libs`
clean:
	rm uniform_random.o
