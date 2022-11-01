# ZhihuRec Data-mining
A flask app for analyzing ZhihuRec dataset.

## Requirement

``` bash
 pip install requirements.txt
```

## Usage
- [Dataset] Put dataset ZhihuRec in the root directory.
- [Work Path] Set the work path in root directory.
- [Preprocess] Run the io.py, to convert answer_infos.txt into .csv files.

First, run this command to get answers' csv files:

``` bash
 python tools/io.py
```

or just download from here:

and put the folder `answer_csv` into `source/`

Then you can use this command to run the flask app:
``` bash
 python app.py
```

The flask app will run on the "127.0.0.1:5000"

## Files
- [model] The tf-idf model will be saved here.
- [source] Processed files 
  - [answer_csv] Answers' csv files. All files are sorted.
    - [xxxx.csv] The xxxx means the start(min) answer's index in this file. 
- [tools] Tools help you analyze the dataset.
  - [io.py] Used to read/write/convert dataset.
  - [tfidf.py] TF-IDF algorithm. its mainly functions are `train()`,`load_tfidf()`,`save_tfidf()`, `compare_similarity()`.
- [zhihuRec] The dataset. You should put txt files here.
- [app.py] The entry of the flask app.
- [preprocess.py] Use the code in `tools` to create tfidf matrix, and save the result into `model`.