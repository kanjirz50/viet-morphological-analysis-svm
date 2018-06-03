# Vietnamese morphological analyzer using SVMs.

![](https://travis-ci.org/kanjirz50/viet-morphological-analysis-svm.svg?branch=master)
![](https://img.shields.io/pypi/v/visvmtagger.svg)
![](https://img.shields.io/pypi/l/visvmtagger.svg)
![](https://img.shields.io/pypi/pyversions/visvmtagger.svg)

SVMs based morphological analyzer for word segmentation and part-of-speech tagging.

Old version(Python2 and YamCha) is [here](https://github.com/kanjirz50/viet-morphological-analysis-svm/tree/0.1).

## Usage

```sh
$ pip install visvmtagger
$ python
```

```python
>>> from visvmtagger import Tagger
>>> t = Tagger()
>>> t.tokenize("Tôi là sinh viên .")
[Tôi(B-PP), là(B-VB), sinh(B-NN), viên(I-NN), .(B-SB)]
>>> t.tokenize("Tôi là sinh viên .")[0].surface # pos is also available
'Tôi'
```

## How to make model file

Please see a `main()` in `visvmtagger/train.py` .

## License
MIT
