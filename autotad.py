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

""" Adapt line to be written in the ADT file """
def adaptLine(line):

    #Structs are defined by typedef and named by their original name capitalized
    if "struct" in line:
        line = line.replace("{", " ").split(" ")
        struct_name = line[line.index("struct") + 1]

        line = "typedef " + struct_name + " " + struct_name.capitalize() + ";\n"
    else:
        line = line.replace('{',';')

    return line

""" Writes header in file """ 
def writeHeader(FilesNames, ADTFile):

    #prepares ADTFile name for writing
    header_filename = FilesNames.adt_filename.upper().replace('.','_')

    str_header = "#ifndef " + header_filename + "\n#define " + header_filename + "\n"

    ADTFile.write(str_header)

    return

def writeContents(DotcFile, ADTFile, dict_functions_comments = {}):

    #curly_braces_control makes the scope control to identify functions
    curly_braces_control = 0

    dotc_contents = DotcFile.readlines()
    for line in dotc_contents:

        #If "//AUTOTAD_PRIVATE" is in line, curly_braces_control is changed so the next function will be ignored by the script 
        if "//AUTOTAD_PRIVATE" in line and curly_braces_control == 0:
            curly_braces_control = -1 

        elif '{' in line:

            if curly_braces_control == 0:

                line = adaptLine(line)

                #If line already existed in a previous file, it's original comment is kept in the new one
                if line in dict_functions_comments:
                    str_comment_section = "\n" + dict_functions_comments[line]
                else:
                    str_comment_section = "\n/*\n * Comment section\n*/\n"

                ADTFile.write(str_comment_section)
                ADTFile.write(line)

            curly_braces_control += 1

        if '}' in line:
            curly_braces_control -= 1 if curly_braces_control > 0 else 0

    return

""" Writes footer in file """ 
def writeFooter(ADTFile):

    ADTFile.write("\n#endif")

    return

""" Writes new ADT file from scratch """ 
def writeNewADT(FilesNames, dict_functions_comments = {}):

    """ Opening files """
    DotcFile = open (FilesNames.dotc_filename, "r")
    ADTFile = open (FilesNames.adt_filename, "w")  

    writeHeader(FilesNames, ADTFile)
    writeContents(DotcFile, ADTFile, dict_functions_comments)
    writeFooter(ADTFile)

    DotcFile.close()
    ADTFile.close()

    return

""" Writes ADT file from existent file """ 
def ADTFromExistentFile(FilesNames, ADTFile):

    """ First, the existent .h file is read and the functions' comments are stored in a dictionary """
    adt_contents = ADTFile.readlines()
    dict_functions_comments = {}

    comment = ""
    comment_scope = False 
    for line in adt_contents:
        
        if "/*" in line:
            comment_scope = True
            comment += line

        elif "*/" in line:
            comment += line
            comment_scope = False

        elif comment_scope == True:
            comment += line

        else:
            dict_functions_comments[line] = comment
            comment = ""

    """ Then, the previous file is overwritten by the new version, keeping the original comments """
    writeNewADT(FilesNames, dict_functions_comments)

    return

def main():

    FilesNames = ClassFileNames()

    """ Gets dotc_filename from argv if it exists; otherwise, asks for input from stdin """
    if (len(sys.argv) > 1):
        FilesNames.dotc_filename = sys.argv[1]
    else:
        FilesNames.dotc_filename = str(input())

    FilesNames = getFilesNames(FilesNames)

    """ If the file adt_filename already exists, the new one is created based on it """
    try:
        with open(FilesNames.adt_filename, "r") as ADTFile:
            ADTFromExistentFile(FilesNames, ADTFile)
    except:
        writeNewADT(FilesNames)

main()
