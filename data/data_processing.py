import os
import glob

# authors = ["haruki_murakami", "kurt_vonnegut", "oscar_wilde"]

authors = ["oscar_wilde"]

def file_to_lines(file_path, save_path):
    with open(file_path, "r+") as f:
        lines = f.readlines()
        text_chunk = " ".join(lines)
        for i in range(10):
            print(text_chunk[:1000])
        f.write(text_chunk)


        with open(save_path, "w") as save_f:
            save_f.write(text_chunk)


def read_files():
    for a in authors:
        files = glob.glob(a + "/*.txt")
        for f in files:
            file_to_lines(f, a+"_lines.txt")

if __name__ == '__main__':
    read_files()