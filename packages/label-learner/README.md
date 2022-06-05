# Label Learner

This is the part of the project that actually trains a model for labeling images.

## Setup

The following script handles installing the necessary packages required to use tensorflow metal on a Mac M1.

* downloads miniforge3 install script
* runs miniforge3 install script
* initializes a conda virtual environment
* installs Tensorflow and other Python dependencies for data science

NOTE: The setup script will provide the directory path you should use for the miniforge3 installer. Be sure to follow
along and enter it when asked!

```shell
$ ./setup-mac-local.sh
```

## Training the model

After running the setup script, you can now call `train_model.py` with Python from the venv

```shell
$ ./miniforge3/envs/leabel_learner_venv/bin/python train_model.py
```

## Workflows

### Activating the Conda venv

Activating the `label_learner_venv` is a 2-step process, unfortunately.

You must first activate the `base` Conda venv, and then activate the `label_learner_venv`

```shell
$ source ./miniforge3/bin/activate
# now in  "base" conda venv
(base) $ conda activate label_learner_venv
# now in label_learner_env
(label_learner_env) $ which python
```

### Deactivating the Conda venv

To deactivate a conda venv, you must use `conda deactivate`

```shell
(label_learner_venv) $ conda deactivate
# now in "base" conda env
(base) $ conda deactivate
# now in your regular shell
$ which python
```