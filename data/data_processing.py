import re
import os
import glob

def file_to_sentences(file_path, save_path):
    # using 'utf-8-sig' encoding to exclude the byte order mark(BOM) U+FEFF
    with open(file_path, "r+", encoding='utf-8-sig') as f:
        # read in raw text
        raw_text = f.readlines()
        text = " ".join(raw_text)

        # split text by lines
        lines = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

        # remove blank lines and whitespaces
        lines = [l.strip().replace("\n", "") for l in lines]

        # save in a single file for each author, one sentence per line
        with open(save_path, "a+") as sf:
            sf.write("\n".join(lines))

def read_files(authors):
    for a in authors:
        # get all files under a same author
        file_paths = glob.glob(a + "/*.txt")

        # save processed text to a single file
        save_file_path = a + "_lines.txt"
        if os.path.exists(save_file_path):
            os.remove(save_file_path)

        for f in file_paths:
            file_to_sentences(f, save_file_path)

if __name__ == '__main__':
    # authors = ["haruki_murakami", "kurt_vonnegut", "oscar_wilde"]
    authors = ["oscar_wilde"]

    read_files(authors)