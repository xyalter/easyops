# easyops

## Create Virtual Environments
```
python3 -m venv <DIR>
source <DIR>/bin/activate
pip3 install --upgrade pip
```

## Install dependencies
```
pip3 install -r requirements.txt
```

## Install develops dependencies
```
pip3 install -r dev-requirements.txt
```

python3 -m venv .venv
source .venv/bin/activate
bash launcher.sh -T debian -H "gz1.lesscode.dev"


# build

```
python -m build
```

```
twine upload dist/*
```
