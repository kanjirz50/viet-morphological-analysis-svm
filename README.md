# Vietnamese morphological analyzer with using SVMs.

This morphological analyzer use SVMs for wordsegmentation and part-of-speech tagging.


## Requirements

- Python 2
- [YamCha](http://chasen.org/~taku/software/yamcha/)
- [model file](https://drive.google.com/file/d/0BxSyNdemluFBZ3A5X2ZOTEJKb1k/view?usp=sharing), download to `./models/vnPOS.model`

## Usage

```sh
% git clone https://github.com/kanjirz50/viet-morphological-analysis-svm.git
```

Please download model file from [here](https://drive.google.com/file/d/0BxSyNdemluFBZ3A5X2ZOTEJKb1k/view?usp=sharing) to ./models/vnPOS.model

```sh
# running analyzer
% python viet_morph_analyze.py < cat input_text.txt
```

## How to make model file

### Get tagged Corpus
* [vnPOS](http://vnlp.net/2009/06/25/corpus-vnpos/)

### Convert format from vnPOS to IOB2 tag format

Corpus is given below format.

```
Tấp_nập//JJ sắm//VB đtdđ//NN đầu//NN năm//NC
...
```

Change format to IOB2 tag format.(Use only I tag and B tag.)

```sh
% cat vnPOS.txt | python ./utils/vnPOS_to_iob2.py > vnPOS.iob2
# Output likes below one.
Tấp		B-JJ
nập		I_JJ
sắm		B-VB
đtdđ	B-NN
đầu		B-NN
năm		B-NC

...
```

Training with YamCha

```sh
# Show YamCha libexec directory
% yamcha-config --libexecdir
/usr/local/Cellar/yamcha/0.33/libexec/yamcha

# Copy Makefile
% cp /usr/local/Cellar/yamcha/0.33/libexec/yamcha/Makefile .

# Training
% make CORPUS=vnPOS.txt.rnd.train.iob2 MODEL=./model/vnPOS FEATURE="F:-2..2:0..0 T:-2..-1" train
```

## License
MIT
