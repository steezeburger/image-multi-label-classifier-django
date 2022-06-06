# Image Labeler

This repo contains two main packages, `django_app`, and `label_learner`.

### Django web app

The Django web application includes management commands for indexing a directory of images with Postgres, as well as generating a CSV to be used for the training data. It also includes a front end for more easily labeling hundreds of images for training data.

![image-labeler](https://raw.githubusercontent.com/steezeburger/image-multi-label-classifier-django/main/image-labeler.png)

### Label Learner

The `label_learner` application is really just a script + Conda environment for running tensorflow on a Mac M1 (Apple Silicon)
