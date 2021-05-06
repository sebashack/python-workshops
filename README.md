## Operating System

This code has only been run in Ubuntu 20.04.


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

## Run code

First, make sure venv is active.

The application's command line has the following structure:

```
usage: src [-h] -i DIR -o DIR -j FILE -wt INT -ht INT
args: the following arguments are required: -i/--input-dir, -o/--out-dir, -j/--out-json, -wt/--width, -ht/--height

```

where

- `--input-dir`: Input directory with raw images which haven't been preprocessed.
- `--out-dir`: Output directory where processed images are located for subsequent display in ImageViewer. Image
               is transformed to gray-scale, and resolution is adjusted by `width x height` pixels.
- `--out-json`: Output json file where images are stored after user has labeled them via ImageViewer. Images are
                stored in base64.

Here is an example. Run command line like this:

```
python src -i ./face-examples -o ./unlabeled-images -j ./sample.json -wt 300 -ht 300
```

This command will read images from dir `./face-examples` and write rois with `300 x 300` resolution into `./unlabeled-images`.
Subsequently, ImageViewer will pop up and user will proceed to label each example. When labeling is finished, the dictionary of
images is properly encoded and written into `./sample.json` file.
