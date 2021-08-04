import sys
from os.path import exists

""" Class containing used files names """
class ClassFiles:
    dotc_filename = ""
    adt_filename = ""

""" Gets the ADT file name """
def getADTfilename(Files):

    if ".c" not in Files.dotc_filename:
        Files.dotc_filename += ".c"

    Files.adt_filename = Files.dotc_filename.replace(".c",".h")
    return Files

""" Writes header in file """ 
def writeHeader(Files, ADTFile):

    #prepares ADTFile name for writing
    header_filename = Files.adt_filename.upper().replace('.','_')

    str_header = "#ifndef " + header_filename + "\n#define " + header_filename + "\n"

    ADTFile.write(str_header)

    return

""" Writes footer in file """ 
def writeFooter(ADTFile):

    ADTFile.write("\n#endif")

    return

""" Writes ADT file from scratch """ 
def ADTFromScratch(Files, DotcFile, ADTFile):

    writeHeader(Files, ADTFile)

    contents = DotcFile.readlines()
    str_comment_section = "\n/*\n * Comment section\n*/\n"

    #Makes the scope control, therefore only functions names are written in ADTFile
    curly_braces_control = 0

    for line in contents:

        #If "//PRIVATE_AUTOTAD" is in line, curly_braces_control is changed
        #  so the next read function will be ignored by the script
        if "//PRIVATE_AUTOTAD" in line:
            curly_braces_control = -1

        if '{' in line:

            if curly_braces_control == 0:

                #TODO:
                #  clean the struct writer section
                if "struct" in line:
                    i = 0
                    line = line.replace("{", " ").split(" ")

                    for i in range(len(line)):
                        if line[i] == "struct":
                            aux_string = "typedef "+line[i+1]
                            line[i+1] = line[i+1].capitalize()
                            line = aux_string + " " + line[i+1] + ";\n"
                            break;
                else:
                    line = line.replace('{',';')

                ADTFile.write(str_comment_section)
                ADTFile.write(line)

            curly_braces_control += 1

        if '}' in line:
            curly_braces_control -= 1 if curly_braces_control > 0 else 0

    writeFooter(ADTFile)

    return
    
#TODO:
#  clean ADTFromExistentFile
#  modularize writing section
""" Writes ADT file from existent file """ 
def ADTFromExistentFile(Files, DotcFile, ADTFile):

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

        elif comment_scope:
            comment += line

        else:
            dict_functions_comments[line] = comment
            comment = ""

    ADTFile = open(Files.adt_filename, 'w')

    writeHeader(Files, ADTFile)

    curly_braces_control = 0
    dotc_contents = DotcFile.readlines()

    for line in dotc_contents:

        #If "//PRIVATE_AUTOTAD" is in line, curly_braces_control is changed
        #  so the next read function will be ignored by the script
        if "//PRIVATE_AUTOTAD" in line:
            curly_braces_control = -1

        if '{' in line:

            if curly_braces_control == 0:

                #TODO:
                #  clean the struct writer section
                if "struct" in line:
                    i = 0
                    line = line.replace("{", " ").split(" ")

                    for i in range(len(line)):
                        if line[i] == "struct":
                            aux_string = "typedef "+line[i+1]
                            line[i+1] = line[i+1].capitalize()
                            line = aux_string + " " + line[i+1] + ";\n"
                            break;
                else:
                    line = line.replace('{',';')

                if line in dict_functions_comments:
                    str_comment_section = "\n" + dict_functions_comments[line]
                else:
                    str_comment_section = "\n/*\n * Comment section\n*/\n"

                ADTFile.write(str_comment_section)
                ADTFile.write(line)

            curly_braces_control += 1

        if '}' in line:
            curly_braces_control -= 1 if curly_braces_control > 0 else 0

    writeFooter(ADTFile)

def main():

    Files = ClassFiles()

    """ Gets dotc_filename from argv if it exists; otherwise, asks for input from stdin """
    if (len(sys.argv) > 1):
        Files.dotc_filename = sys.argv[1]
    else:
        Files.dotc_filename = str(input())

    getADTfilename(Files)

    """ Opening files """
    DotcFile = open (Files.dotc_filename, "r")

    try:
        ADTFile = open (Files.adt_filename, "x")  
        ADTFile = open (Files.adt_filename, "w")  

        ADTFromScratch(Files, DotcFile, ADTFile)
    except:
        ADTFile = open (Files.adt_filename, "r")  

        ADTFromExistentFile(Files, DotcFile, ADTFile)



                
    DotcFile.close()
    ADTFile.close()

main()

"""
    Script for getting rid of all commentaries

    comment = ""
    comment_scope = False 
    for line in contents:
        
        if "/*" in line:
            comment_scope = True
            comment += line

        elif "*/" in line:
            comment += line
            comment_scope = False
            comment = ""

        elif comment_scope:
            comment += line

        else:
            ADTFile.write(comment)
            ADTFile.write(line)
"""
