# Tello approaches human and lands on palm
## Setup
### [Edge TPU dependencies installation](https://github.com/jsk-ros-pkg/coral_usb_ros)
#### [Installing the EdgeTPU runtime](https://coral.withgoogle.com/docs/accelerator/get-started/#1-install-the-edge-tpu-runtime)

```bash
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
# If you do not have USB3, install libedgetpu1-legacy-std
sudo apt-get install libedgetpu1-legacy-max # Choose <YES> when asked
sudo apt-get install python3-edgetpu
```
### [Install just the TensorFlow Lite interpreter (Noetic)](https://www.tensorflow.org/lite/guide/python)

```bash
sudo apt-get install python3-tflite-runtime
```

### Install vcstool (noetic)
```bash
sudo apt install python3-vcstool
```

### Workspace build (noetic)
```bash
source /opt/ros/noetic/setup.bash 
mkdir -p ~/tello_ws/src
cd ~/tello_ws/src
sudo rosdep init
rosdep update
git clone https://github.com/heissereal/tello_approaching_human.git
vcs import < tello_approaching_human/tello_approaching_human.rosinstall --recursive
rosdep install --from-paths . --ignore-src -y -r
cd ~/tello_ws
catkin init
catkin build
```
### Model download for coral

```bash
source ~/tello_ws/devel/setup.bash
roscd coral_usb/scripts
rosrun coral_usb download_models.py
```


## Demo
### Start communication with tello
```bash
source ~/tello_ws/devel/setup.bash
roslaunch tello_driver tello_node.launch 
```

### Run `tello_recognition.launch`
```bash
source ~/tello_ws/devel/setup.bash
roslaunch tello_demos tello_recognition.launch
```

### Start hovering
```bash
source ~/tello_ws/devel/setup.bash
rosrun tello_demos tello_keyboard.py
```
- Press 't' -> takeoff
- Press 'l' -> land


