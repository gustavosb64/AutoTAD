# AutoTAD
Automatic header files creator. It creates a _header_ file after a given _filename.c_, naming it after its original name, as _filename.h_. In case a _filename.h_ already exists, autotad will scan it and keep the written comments in the new version.

* **What will be written in _filename.h_?**
  * _functions_ and _structs_ written in _filename.c_. If a function is written in _filename.h_ but it is removed from _filename.c_, it will not be kept on further executions.
  * _typedefs_ and _includes_ written in _filename.h_ will be kept upon further executions.
  * Comments written right above _functions_, _structs_ and _typedefs_ in _filename.h_ will be kept upon further executions.
  * Every file will be written following the template below (for a file named _filename.h_):
    ```
    #ifndef FILENAME_H
    #define FILENAME_H
    
    ...
    
    #endif
    ```
    
* **What arguments can be passed?**
  - *filename.c*: autotad creates header based on filename.c (".c" is not necessary. However, if it's written "_filename._", ending with '_._', autotad will not recognise the file).
  - *comment-off*: autotad does not create new automatic comment sections for new functions or structs.

  If _filename_ is passed as a parameter, autotad will search for a _filename.h_ file in the current directory. Otherwise, the function name will be asked via _standard input_, then it will search for it. It can process multiples files given via _argv_. The arguments' order does not matter.

* **Any tips?**
  - There is a section for tips and warnings later in this README.

* **Example of execution?**
  - Pretty simple and straightforward. It can be executed both through the executable file or directly by the Lua script:
  ```
  ./autotad function1.c function2 comment-off
  ```
  ```
  lua autotad.lua function1.c function2 comment-off
  ```
  - There are more detailed execution examples in the last section.

------------------------

### Functions
Functions are written in _filename.h_ keeping their parameter names from _filename.c_. They are written in the order they are read from _filename.c_. For example, if we have, in _filename.c_:
```
void function1(int i, char *c){
  ...
  return;
}

int function2(){
  ...
  return 0;
}
```
This will be written in _filename.h_:
```
/*
 * Comment section
*/
void function1(int i, char *c);

/*
 * Comment section
*/
int function2();
```
_Note: How autotad deals with comments is detailed later._

### Structs
When a struct is read in _filename.c_, it will be defined as a type in _filename.h_. Structs are always written in *filename.h* like their names in *filename.c* with its first letter capitalized. For example, if we have, in _filename.c_:
```
struct str_example{
  int i;
  float f;
};
```
This will be written in _filename.h_:
```
/*
 * Comment section
*/
typedef struct str_example Str_example;
```

### Typedefs and includes
Typedefs written directly in _filename.h_ (other than those defined by structs) are also kept on further executions, along their comments. However, autotad will **not** write in _filename.h_ a typedef defined in _filename.c_. The same applies to _includes_ written in _filename.h_
```
// This is in filename.h and it WILL be kept upon further executions
typedef int elem;
```
They are always written on the top of _filename.h_, before structs and functions. _Includes_ are written before typedefs.

### Private structures
Writing *AUTOTAD_PRIVATE* in a comment in *filename.c* makes autotad ignore the next function or structure. For example, in _filename.c_:
```
/* AUTOTAD_PRIVATE */
struct str_example{
  int i;
  float f;
};

//AUTOTAD_PRIVATE
void function2(){
  ...
  return;
}

void function3(){
  ...
  return;
}
```
Only function3 will be written in _filename.h_. Writing it inside a _function_ or _struct_ will have no effect.

### Comments
If _filename.h_ doesn't exist, a new file will be created. Otherwise, autotad will scan the whole file and store all comments with their respective _functions_, _structs_ or _typedefs_ as keys in a dictionary. These comments will be rewritten in the new _filename.h_ along their respective key.

Comments written in _filename.c_ will **not** be written in _filename.h_.

By default, the header file is created writing a comment section above every new function or struct read in the .c file. An example is shown below.
```
/*
 * Comment section
*/
void function(int i, char *c);
```
This can be disabled by using _comment-off_ as an argument via _argv_ when executing the script. Notice that, once the file is written, the comment section will later be identified as _function_'s comment, so it will be copied on further executions even when using _comment-off_.

Only the comment section right above the functions, structs or typedefs will be kept after executing autotad over an existing _filename.h_ file, as shown below.
```
// This comment 
// WILL NOT
// be kept in the new file

/*
 * This comment WILL
 * be kept in the new file
*/
void function1(int i);

/* This comment 
 * WILL NOT
 * be kept in the new file
*/

// This comment WILL
// be kept in the new file
void function2(int i);
```
**An important detail about how the keys are used in the dictionaries:**
* Structs and other typedefs are stored in the dictionary using their whole line as a key. As for functions, **only their names are used as keys**. That means we can modify the parameters or the return type in _filename.c_, but, **as long as we do not change the function name, its previous comment will be kept on further executions**.

------------------------

### Tips and warnings
* **Avoid declaring functions and structs with a curly brace below the function's name.** I generally assume every function, loop or any other structure will be declared with the first curly brace in line. For example, instead of writing:
 ```
    void function()
    {
      ...
      return;
    }
 ```
   Write it like this:
 ```
    void function(){
      ...
      return;
    }
 ```
    Writing them differently will result in wrong output.
* **Avoid using both curly braces in a single line**. Curly braces are used for scope control, and I generally assume every function, loop or any other structure with its own scope to use at least two different lines, so writing them in a single line might result in unexpected output. For example, instead of writing:
 ```
  while(condition){ }
 ```
   Write it like this:
 ```
  while(condition){ 
  }
 ```
   However, using a single line _if_ without curly braces, for example, like in ```if (condition) break;``` will not cause any possible bug.
* **Be careful changing functions' names**. As stated before, you can change their return type or their parameters, but changing their name will make autotad indentify them as a new function. That said, for functions returning pointers, **avoid writing ' * ' along the function's name**, or autotad will indentify it as part of the function's name. For example, instead of writing:
```
 char *a_string_function(){
  ...
  return string;
 }
```
   Write it like this:
```
 char* a_string_function(){
  ...
  return string;
 }
```
   So there will be no possible mistake identifying what is the function's name and what is the return type.
* **Use a Makefile**. To avoid repetitive and boring commands, it is largely recommended to use this script in a Makefile before compiling all files. A simple Makefile would do:
```
  c:
    ./autotad filename.c
    gcc -o main main.c filename.c
```
So when ```make c``` is called, autotad will be executed.

------------------------

### Execution example

Given _filename.c_:
```
struct exStr{
  int i;
  char c;
};

void function1(int i){
  ...
  return;
}

//AUTOTAD_PRIVATE
void function2(int i){
  ...
  return;
}

int function3(float f){
  ...
  return 1;
}
```
After executing ```./autotad filename.c```, this will be the output in _filename.h_:
```
#ifndef FILENAME_H
#define FILENAME_H


/*
 * Comment section
*/
typedef struct exStr ExStr;

/*
 * Comment section
*/
void function1(int i);

/*
 * Comment section
*/
int function3(float f);

   
#endif
```

Changing _filename.h_ (editing comments and adding a new typedef):
```
#ifndef FILENAME_H
#define FILENAME_H


/*
 * This struct
 * is here as an example
*/
typedef struct exStr ExStr;

// this is the glorious function1
void function1(int i);

/* I'm adding this typedef here just for clarity */
typedef int elem;    

// hey another function
float function3(float f);
    
#endif
```
And changing _filename.c_ (removing _function1_ and adding _function4_):
```
struct exStr{
  int i;
  char c;
};

float function4(char *string){
  ...
  return f_var;
}

//AUTOTAD_PRIVATE
void function2(int i){
  ...
  return;
}

int function3(float f){
  ...
  return 1;
}
```
After executing ```./autotad filename.c comment-off```, the new _filename.h_ will be:

```
#ifndef FILENAME_H
#define FILENAME_H


/* I'm adding this typedef here just for clarity */
typedef int elem;    

/*
 * This struct
 * is here as an example
*/
typedef struct exStr ExStr;

void function4(int i);

// hey another function
float function3(float f);    
    
    
#endif
```
In the same fashion, multiple files can be given via _argv_: 

```./autotad filename1.c filename2.c filename3.c comment-off```

It will process each file, creating their respective header file. ```comment-off``` will be applied to all three files.
