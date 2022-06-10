function getFilesName(filename)

    new_name = filename
    if (not filename:find(".c")) then
       new_name = filename .. ".c" 
    end
    return new_name

end

function change_name(filename)
    return filename:gsub(".c", ".h")
end

list_of_filenames_c = {}
list_of_filenames_h = {}

dotc_filename = ""

comment_off = false

for i=1, #arg, 1 do

    if (arg[i] == "comment-off") then
        comment_off = true
    else
        table.insert(list_of_filenames_c, arg[i])
    end

end

print(table.concat(list_of_filenames_c, ", "))

i = 1
for k, v in pairs(list_of_filenames_c) do
    v = getFilesName(v)
    list_of_filenames_h[i] = change_name(v)
    i = i+1
    print(v)
end

print(table.concat(list_of_filenames_h, ", "))
