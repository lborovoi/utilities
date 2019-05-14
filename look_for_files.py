import os
import time
import sys

#extensions = ['sav', 'xls', 'csv']
extensions = ['py']

def to_date(t):
    return time.strftime('%d/%m/%Y', time.localtime(t))

def search_files(root, outfile_dict, catch_up = None):
    queue = [root]
    count = 0
    while queue:
        dir = queue.pop()

        if catch_up == dir:
            catch_up = None

        count +=1
        if not catch_up:
            # print(dir)
            if count%10 == 0:
                print ("already done", count)
        else:
            if count%1000 == 0:
                print ("already done", count)

        try:
            listing = os.listdir(dir)

            for file in listing:
                if file.startswith('$'):  # recycle bin
                    continue

                full_name = os.path.join(dir, file)
                if os.path.isdir(full_name):
                    queue.append(full_name)
                elif not catch_up:
                    extension = os.path.splitext(full_name)[1]
                    if extension in outfile_dict:
                        outfile = outfile_dict[extension]
                        created = os.path.getctime(full_name)
                        modified = os.path.getmtime(full_name)
                        outfile.write('\t'.join([full_name, to_date(created), to_date(modified)]))
                        outfile.write('\n')

        except Exception as ex:
            print(ex)
            continue


dir = r'C:\Users\Leah\Documents\search'
outfile_dict = {}
for ext in extensions:
    filename = os.path.join(dir, '{}_files.tsv'.format(ext))
    outfile_dict['.' + ext] = open(filename, 'wt')

search_files(r'e:\\', outfile_dict) # , catch_up=r'e:\\3D')

for f in outfile_dict.values():
    f.close()