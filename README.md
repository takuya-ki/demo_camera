# pan-tilt

[![support level: community](https://img.shields.io/badge/support%20level-community-lightgray.svg)](https://rosindustrial.org/news/2016/10/7/better-supporting-a-growing-ros-industrial-software-platform)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Pan-tilt camera controller.

## Dependency

### Python dependency
- Python 3.8.10
  - rtsp        1.1.12
  - PySimpleGUI 4.60.5
  - onvif-zeep  0.2.12
  - Pillow      10.0.0
  - utllib3     1.26.8

### Available cameras
- tp-link Tapo C200  

<img src=image/c200.jpg height=180> <img src=image/c200_gui.png height=180>  

- tp-link Tapo C225  

<img src=image/c225.jpg height=180> <img src=image/c225_gui.png height=180>  


## Installation

```bash
git clone git@github.com:takuya-ki/pan-tilt.git
cd pan-tilt
pip install -r requirements.txt
```

### Anaconda

```bash
git clone git@github.com:takuya-ki/pan-tilt.git
cd pan-tilt
conda create -n tapo python=3.8.10 -y
conda activate tapo
pip install -r requirements.txt
```

## Usage

```bash
python src/tapogui.py [camera_type]  # 'c200' or 'c225'
```

## Author / Contributor

[Takuya Kiyokawa](https://takuya-ki.github.io/)

## License

This software is released under the MIT License, see [LICENSE](./LICENSE).
