import re
import os
from tqdm.auto import tqdm
from frog import Frog, FrogOptions

frog = Frog(FrogOptions(morph=False, mwu=False, chunking=False, ner=False))

corpus_dir = "Corpus/Normalized/"

def parse(filename):
    filename_corpus = f"{corpus_dir}{filename}"

    with open(filename_corpus, "r", encoding="utf-8") as f:
        x = []
        lines = f.readlines()
        for line in lines:
            tag = re.match(r'<[^\\][^<>]*>', line)  # store sentence tag
            line = re.sub(r'<[^<>]*>', "", line)  # remove sentence tags
            normalized_words = re.findall(r'(\w+)\[(\w+)\]', line)  # store both normalized and normalized forms in list
            clean_line = re.sub(r'\w+\[(\w+)\]', r'\1', line)  # keep only normalized word forms
            output = frog.process(clean_line)   # make predictions based on cleaned_line
            new_line = ""
            for item in output:
                # words with FL tag
                if "__FL__" in item['text']:
                    new_line = new_line + item["text"] + " "
                # other words
                else:
                    new_line = new_line + item["text"] + "[" + item['lemma'] + ", " + item['pos'] + ", " + str(item['posprob']) + "] "
            for pair in normalized_words:
                new_line = re.sub(pair[1] + r'(?=\[)', pair[0], new_line, 1)
            x.append(tag.group(0) + new_line.rstrip() + "<\sentence>")
    with open(f"Corpus/FrogTagged/{filename}", "w", encoding="utf8") as f1:
        f1.write('\n'.join(x))


if __name__ == '__main__':
    directory = os.fsencode(corpus_dir)

    files = list(os.listdir(directory))
    num_files = len(files)

    # loop through directory (corpus)
    for index, file in enumerate(files):
        filename = os.fsdecode(file)
        #print(f"{index + 1}/{num_files} - {filename}")
        try:
            if filename.startswith("SPI")
            #if filename.endswith(".txt"):
                # process the files here:
                parse(filename)
        except:
            print(f"ERROR: {filename}")
