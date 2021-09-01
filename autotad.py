import sys
from os.path import exists

""" Class containing used files names """
class ClassFileNames:
    dotc_filename = ""
    adt_filename = ""

""" Gets the used files names """
def getFilesNames(FilesNames):

    if ".c" not in FilesNames.dotc_filename:
        FilesNames.dotc_filename += ".c"

    FilesNames.adt_filename = FilesNames.dotc_filename.replace(".c",".h")

    return FilesNames

""" Adapt line to be written in ADT file """
def adaptLine(line):

    #Structs are defined by typedef and named by their original name capitalized
    if "struct" in line:
        line = line.replace("{", " ").split(" ")
        struct_name = line[line.index("struct") + 1]

        line = "typedef struct " + struct_name + " " + struct_name.capitalize() + ";\n"
    else:
        line = line.replace('{',';')

    return line

""" Writes header in file """ 
def writeHeader(FilesNames, ADTFile):

    #prepares ADTFile name for writing
    header_filename = FilesNames.adt_filename.upper().replace('.','_')

    str_header = "#ifndef " + header_filename + "\n#define " + header_filename + "\n\n"

    ADTFile.write(str_header)

    return

""" Writes the contents in file """
def writeContents(DotcFile, ADTFile, comment_off, dict_functions_comments = {}, typedef_list = []):

    if comment_off == True:
        default_comment = "\n"
    else:
        default_comment = "\n/*\n * Comment section\n*/\n"

    for line in typedef_list:
        ADTFile.write("\n" + dict_functions_comments[line])
        ADTFile.write(line)

    #curly_braces_control makes the scope control to identify functions
    curly_braces_control = 0

    dotc_contents = DotcFile.readlines()
    for line in dotc_contents:

        #If "AUTOTAD_PRIVATE" is in line, curly_braces_control is changed so the next function will be ignored by the script 
        if "AUTOTAD_PRIVATE" in line and curly_braces_control == 0:
            curly_braces_control = -1 

        elif '{' in line:

            if curly_braces_control == 0:

                line = adaptLine(line)

                #If line already existed in a previous file, it's original comment is kept in the new one
                if line in dict_functions_comments:
                    str_comment_section = "\n" + dict_functions_comments[line]
                else:
                    str_comment_section = default_comment 

                ADTFile.write(str_comment_section)
                ADTFile.write(line)

            curly_braces_control += 1

        if '}' in line:
            curly_braces_control -= 1 if curly_braces_control > 0 else 0

    return

""" Writes footer in file """ 
def writeFooter(ADTFile):

    ADTFile.write("\n\n#endif")

    return

""" Writes new ADT file from scratch """ 
def writeNewADT(FilesNames, comment_off, dict_functions_comments = {}, typedef_list = []):

    """ Opening files """
    DotcFile = open (FilesNames.dotc_filename, "r")
    ADTFile = open (FilesNames.adt_filename, "w")  

    writeHeader(FilesNames, ADTFile)
    writeContents(DotcFile, ADTFile, comment_off, dict_functions_comments, typedef_list)
    writeFooter(ADTFile)

    DotcFile.close()
    ADTFile.close()

    return

""" Writes ADT file from existent file """ 
def ADTFromExistentFile(FilesNames, ADTFile, comment_off):

    """ First, the existent .h file is read and the functions' comments are stored in a dictionary """
    adt_contents = ADTFile.readlines()
    dict_functions_comments = {}
    typedef_list = []

    comment = ""
    comment_scope = False 
    for line in adt_contents:
        
        if "/*" in line and "*/" not in line:
            comment_scope = True
            comment += line

        elif "*/" in line or ("//" in line and comment_scope == False):
            comment += line
            comment_scope = False

        elif comment_scope == True:
            comment += line

        elif comment_scope == False and "typedef" in line and "struct" not in line:
            dict_functions_comments[line] = comment
            typedef_list.append(line)
            comment = ""

        else:
            dict_functions_comments[line] = comment
            comment = ""

    """ Then, the previous file is overwritten by the new version, keeping the original comments """
    writeNewADT(FilesNames, comment_off, dict_functions_comments, typedef_list)

    return


FilesNames = ClassFileNames()
comment_off = False

""" Checks input from sys.argv """
for i in range(1, len(sys.argv)):

    if sys.argv[i] == "comment-off":
        comment_off = True

    elif FilesNames.dotc_filename == "": 
        FilesNames.dotc_filename = sys.argv[i]

    else:
        raise Exception(sys.argv[i] + " is not a valid command. Given filename: " + FilesNames.dotc_filename)

""" If dotc_filename is not given via sys.argv, asks for input from stdin """
if FilesNames.dotc_filename == "":
    FilesNames.dotc_filename = str(input())

FilesNames = getFilesNames(FilesNames)

""" If the file adt_filename already exists, the new one is created based on it """
try:
    with open(FilesNames.adt_filename, "r") as ADTFile:
        ADTFromExistentFile(FilesNames, ADTFile, comment_off)
except:
    writeNewADT(FilesNames, comment_off)
