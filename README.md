# AutoTAD
Automatic ADT files creator.

Arguments:

  - *file_name.c*: autotad creates header based on file_name.c (".c" is not necessary)
  
  - *comment-off*: autotad does not create new automatic comment sections for functions

Writing *AUTOTAD_PRIVATE* in a comment in *file_name.c* makes autotad ignore the next function.

Structs are always written in *file_name.h* as the struct name in *file_name.c* capitalized:
  - *struct strName{};* => *typedef struct strName StrName;*
