## Operating System

This code has only been run in Ubuntu 20.04.

## Install system dependencies

```
./first-time-install.sh
```

## Set work environment

```
make set-py-venv-with-deps
```


## Activate virtual environment

```
source .env/bin/activate
```

## Deactivate virtual environment

```
deactivate
```

## Command line usage

```
usage: src [-h] -m MODE [-i FILE] [-l DIR] [-e INT] [-d FILE]
```

### Train a model from scratch

Invoke the main python script in `train` mode without a previously trained model:

```
python src -m train -d <path-to-data-file> -e=15
```

where

```
-d: Path to data-set file in json format.
-e: Number of epochs to train the model.
```

### Train a model from a previously trained model

Invoke the main python script in `train` mode with a previously trained model:

```
python src -m train -d <path-to-data-file> -l <path-to-trained-model-dir> -l -e=15
```

where

```
-l: Path to trained model directory.
```

### Evaluate efficacy of model

Invoke the main python script in `evaluate` mode:

```
python src -m evaluate -d <path-to-data-file> -l <path-to-trained-model-dir>
```

### Prediction

Invoke the main python script in `classify` mode:

```
python src -m classify -d <path-to-data-file> -l <path-to-trained-model-dir> -i <input-image-to-classify>

```

where

```
-i: Path to input image file to be classified.
```

## Notes on this repository


- The CNN model trained for this project used the data-set `sample.json` in the root of this repository.
- The set of labels used for this model is:

```
{
    0: "barack-obama",      # Barack Obama
    1: "rihanna",           # Rihanna
    2: "donald-trump",      # Donald Trump
    3: "emma-chamberlain",  # Emma Chamberlain
    4: "justin",            # Justin Bieber
    5: "jennifer",          # Jennifer Aniston
}

```

Thus these are the only celebreties which are possible to identify with this model.

- the directory `example-images` has some images that you can user to try out the command-line application
  in `classify` mode.

## Trained models

The trained model to try out the command line can be found downloaded from either of the following links:

- Google Drive: https://drive.google.com/file/d/1Hn9U_HNzZzO8FDXLZCaOjRtH2SfQT16f/view?usp=sharing
- One Drive: https://eafit-my.sharepoint.com/:u:/g/personal/spulido1_eafit_edu_co/ET5Q8i0iRPRAlP_-8HtqMb0BEscUcAB3ygcUs8BD7P8Tzg?e=4Jsw2t
