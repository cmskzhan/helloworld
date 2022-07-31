# compare files in two directories recursively
import os
import hashlib
import pandas as pd

# dir1 = r"f:\downloads\samples"
# dir2 = r"H:\SanDiskSecureAccess\samples"

def remove_duplicated_files(dir: str) -> set:
    filelist = []
    file_sizes = []
    for (dirpath, dirnames, filenames) in os.walk(dir):
        for filename in filenames:
            file1 = os.path.join(dirpath, filename)
            filelist.append(file1)
            file_sizes.append(os.path.getsize(file1))
    
    df = pd.DataFrame({"file": filelist, "size": file_sizes})
    
    # keep files that has the same size, 
    #   keep=False means unique value is marked as False, hence removed from df
    remove_unique_size_files = df[df.duplicated(subset="size", keep=False)]
    # calculate md5
    md5sum = []
    for i in remove_unique_size_files['file']:
        with open(i, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
            md5sum.append(md5)

    remove_unique_size_files['md5'] = md5sum
    duplicated_files = remove_unique_size_files[remove_unique_size_files.duplicated(subset="md5", keep=False)] # unique files are filtered out
    # sort files by full path
    duplicated_files.sort_values(by='file', ascending=True, inplace=True)
    merge_duplicates = duplicated_files.drop_duplicates(subset='md5', keep='last') # keep last duplicated files
    files_to_remove = set(duplicated_files['file']) - set(merge_duplicates['file'])

    print(duplicated_files)

    for i in files_to_remove:
        os.remove(i)
    
    return files_to_remove




            


def compare_files_sizes(dir1, dir2) -> None:
    recursive_list1 = os.walk(dir1)
    recursive_list2 = os.walk(dir2)
    for (dirpath, dirnames, filenames) in recursive_list1:
        for filename in filenames:
            file1 = os.path.join(dirpath, filename)
            
            # replace substring in filename
            file2 = file1.replace(dir1, dir2)
            # check if file2 exists
            if os.path.exists(file2):
                # compare files
                if os.path.getsize(file1) != os.path.getsize(file2):
                    print(f"{file1} and {file2} are different sizes")
            else:
                print(f"{file2} does not exist")

if __name__ == "__main__":
    #compare_files(dir1, dir2)
    print(remove_duplicated_files(r"F:\scritps"))

