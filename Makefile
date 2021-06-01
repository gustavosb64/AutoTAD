all:
	gcc -g -o autotad autotad.c

run:
	./autotad

debug:
	valgrind --leak-check=full --show-leak-kinds=all ./autotad
