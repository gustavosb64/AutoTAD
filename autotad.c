#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define READLINE_BUFFER 4096

char *readline(FILE *stream, FILE *dest_file, int *check_scope) {
    char *string = 0;
    int pos = 0; 

	do{
        if (pos % READLINE_BUFFER == 0) {
            string = (char *) realloc(string, (pos / READLINE_BUFFER + 1) * READLINE_BUFFER);
        }
        string[pos] = (char) fgetc(stream);
    }while(string[pos++] != '\n' && string[pos-1] != '\r' && !feof(stream));

    string[pos-1] = 0;
    string = (char *) realloc(string, pos--);
    if (strlen(string) < 1) return string;

    if (string[pos-1] == '{'){
        if (*check_scope == 0 && string[pos-1] == '{'){
            string[pos-1] = ';';
            pos++;
            string = (char *) realloc(string, pos+1);
            string[pos-1] = '\n'; 
            string[pos] = 0;
            fwrite(string, sizeof(char), strlen(string), dest_file);
        }
        *check_scope = *check_scope + 1;
    }
    else if (string[pos-1] == '}') *check_scope = *check_scope - 1;

    return string;
}

int main(int argc, char *argv[]){
    FILE *dest_file = fopen("out_file", "w+");
    int check_scope = 0;

    char *filename = readline(stdin, dest_file, &check_scope);

    /*opening source file for reading
    */
    FILE *src_file = fopen(filename, "r");
    if (src_file == NULL){
        printf("ARQUIVO INEXISTENTE!\n");
        free(filename);
        return 0;
    }

    /*opening destination file for writing
    */
    int cont =0;
    char *string; 
    while (!feof(src_file)){
        string = readline(src_file, dest_file, &check_scope);
        free(string);
    }
 
    free(filename);

    fclose(src_file);
    fclose(dest_file);

    return 0;
}
