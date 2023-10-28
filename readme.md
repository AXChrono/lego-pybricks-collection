# LEGO® Pybricks Collection

A collection of Pybricks scripts I made, mainly for vehicles.

My first introduction to Pybricks was by an article on [RacingBrick](https://racingbrick.com/2021/08/remote-control-for-control-sets-without-an-app-or-smartphone-pybricks/). Most, if not all, of my vehicle related scripts find its roots from the scripts over there.

## Create Python virtual environment in VSCode

This is mainly needed to get no code errors and make use of IntelliSense.

[Based on the information on this support topic on GitHub.](https://github.com/pybricks/support/issues/10)

* Click the right mouse button under the last file in the explorer pane.
* click **Open in integrated Terminal**
* Execute the following in the Terminal:

  ```sh
  python3 -m venv .venv
  ```

* Open the Command Pallette (Ctrl + Shift + P) and search for **Python: Create Terminal**.
* Execute the following in the Terminal:

  ```sh
  python -m pip install --upgrade pip
  pip install git+https://github.com/pybricks/pybricks-api@master
  ```

## Disclaimer

LEGO® is a trademark of the LEGO Group of companies which does not sponsor, authorize or endorse this project.
