# compare files in two directories recursively
import os

dir1 = r"f:\downloads\samples"
dir2 = r"H:\SanDiskSecureAccess\samples"

def remove_duplicate_files(dir1):
    recursive_list1 = os.walk(dir1)
    for (dirpath, dirnames, filenames) in recursive_list1:
        for filename in filenames:
            file1 = os.path.join(dirpath, filename)
            # remove duplicate files
            # if os.path.exists(file1):
            #     os.remove(file1)
            #     print(f"{file1} removed")


def compare_files(dir1, dir2):
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
    compare_files(dir1, dir2)

    #print("Done")

