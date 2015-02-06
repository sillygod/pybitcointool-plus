[![Build Status](https://api.travis-ci.org/leereilly/swot.png)](https://travis-ci.org/leereilly/swot)

# Pybitcointool-plus

Pybitciontool-plus is an enhanced version of [pybitcointool](https://github.com/vbuterin/pybitcointools). Pybitcointools is an excellent library which is lightweight and easy to use, although it has not mentioned about bitcoin principle. My project is based on pybitcointool a lot and I try to implemnt some function which it doesn't provide.

### Requirements

python 2.x
pyqrcode


### Installation

python setup install


### Document

here is the [document](https://sillygod.github.io/pybitcointool-plus)


### How to use RPC server

start a rpc server

```sh
python rpcServer.py
```

then use post method anyway you like to get return value

for example, you can see my test case for rpc `tests/test_rpc.py`

the data format is

```
{'method': 'the method you want to call',
 'id': 'null',  # or num you want :)
 'param': ''}

```



