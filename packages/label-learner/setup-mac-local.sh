#! /bin/bash

##############################################################
# setup script for running this application locally on macOS #
##############################################################

function download_installer() {
  MINIFORGE_INSTALLER="Miniforge3-MacOSX-arm64.sh"
  echo "Checking if ${MINIFORGE_INSTALLER} exists..."
  if [[ ! -f $MINIFORGE_INSTALLER ]]; then
    echo "${MINIFORGE_INSTALLER} does not exist. Download now..."
    wget "https://github.com/conda-forge/miniforge/releases/latest/download/${MINIFORGE_INSTALLER}"
  else
    echo "${MINIFORGE_INSTALLER} exists. Installing now..."
  fi
}

function run_installer() {
  # installs miniforge if there is not already a miniforge3 directory
  echo "Checking if miniforge3 directory exists..."
  if [[ ! -d "miniforge3" ]]; then
    echo "miniforge3 does not exist. Running miniforge installer..."
    # echo the path to use when miniforge installer asks for install location
    LOCAL_MINIFORGE_INSTALL_PATH="$(pwd)/miniforge3"
    echo "#################################################################"
    echo "# Use the following path for your miniforge3 install location:  #"
    echo "# ${LOCAL_MINIFORGE_INSTALL_PATH}"
    echo "#################################################################"
    # run installer
    bash Miniforge3-MacOSX-arm64.sh
  else
    echo "miniforge3 already installed!"
  fi
}

function initialize_conda_venv() {
  # configure conda not to create "base" venv
  ./miniforge3/bin/conda config --set auto_activate_base false || exit
  # create and activate our own venv
  ./miniforge3/bin/conda create --name label_learner_venv python=3.9 || exit

  # activate the venv
  # NOTE - must use "base" venv so that `conda activate` works
  source miniforge3/bin/activate
  conda activate label_learner_venv || exit

  # install conda plugin for apple tensorflow
  # NOTE - now in label_learner_venv venv, can just call `conda`
  conda install -c apple tensorflow-deps
}

function install_tensorflow() {
  # install tensorflow and tensorflow metal
  pip install tensorflow-macos
  pip install tensorflow-metal
  pip install matplotlib numpy pandas scikit-learn tqdm
}

# ensure we are in the right dir
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "$SCRIPT_DIR"/ || exit

download_installer
run_installer
initialize_conda_venv
install_tensorflow
