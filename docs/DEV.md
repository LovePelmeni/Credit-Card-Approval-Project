# Local Development


## Developing

1. Create directory with your functionality inside `src`

```
$ cd src

$ mkdir new_module 

$ cd new_module && touch new_functionality.py
```

2. Depending on what you want to develop you can add 
rest_endpoint to the `rest_settings.py` file 
to make your feature publicly available.

## Testing

1. Create directory inside `tests` for your tests 

```
$ cd tests 

$ mkdir my_tests 

$ cd my_tests && touch some_test.py

```

## Autoformatting Code Style 

1. Make sure that code style using AutoPEP8 autoformatter

```
# Entering Root Directory 

$ cd credit_card_approval

$ autopep8 --recursive .

```

3. Deploy Application using instructions from `README.md` file 
