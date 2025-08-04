<a id="objectmotionnotify"></a>
<br />
<div align="center">
  <a href="https://github.com/Haifisch92/ObjectMotionNotify/blob/main/images/MotionDetectionNotify.jpg">
    <img src="images/MotionDetectionNotify.jpg" alt="Logo" width="768" height="768">
  </a>
  <h3 align="center">Motion Detection Notify</h3>
  <p align="center">
    Motion Detection Software with OpenCV and Telegram Alerts
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
      	<li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Motion Detection Software with OpenCV and Telegram Alerts
This software is a lightweight and efficient motion detection system built with OpenCV, designed to monitor environments in real time and send instant alerts via Telegram. It is ideal for surveillance, security, or automation purposes.
🔧 Core Features:
Motion Detection Mode
Start or stop motion detection with a single command.
The system continuously analyzes video frames and detects movement using OpenCV's background subtraction and contour detection techniques.
Photo Capture
Take snapshots manually or automatically when motion is detected.
Captured images are saved locally and optionally sent to a configured Telegram chat.
Video Recording
Record video footage on demand or during motion events.
Videos are stored locally and can be forwarded to Telegram for remote viewing.
📲 Telegram Integration:
Receive real-time alerts with snapshots or video clips directly in your Telegram chat.
Control the system remotely via Telegram commands (e.g., /start, /stop, /photo, /record).
⚙️ Technology Stack:
Python
OpenCV for video processing and motion detection
Telegram Bot API for remote interaction and notifications

<p align="right">(<a href="#objectmotionnotify">back to top</a>)</p>

### Built With

* [![Python][Python.com]][Python-url]
* [![Telegram API][Telegram.com]][Telegram-url]
* [![OpenCV][OpenCV.com]][OpenCV-url]


<p align="right">(<a href="#objectmotionnotify">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This project use uv packets manager, install with curl
   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
or with wget
   ```sh
   wget -qO- https://astral.sh/uv/install.sh | sh
   ```

### Installation

_Once uv is installed on your computer, it will handle the dependencies and the virtual environment automatically._

1. Clone the repo
   ```sh
   git clone https://github.com/Haifisch92/ObjectMotionNotify.git
   ```
2. Edit configexample.toml file and rename config.toml required param : token, chat_id, stream 

3. Start project and create virtual environment
   ```sh
   uv run main.py
   ```

<p align="right">(<a href="#objectmotionnotify">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Object Motion python class
- [x] Allert Telegram
- [ ] Allert email

See the [open issues](https://github.com/Haifisch92/ObjectMotionNotify/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#objectmotionnotify">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Aiello Gabriel - [Twitter](https://twitter.com/haifisch_92) - devgabriel92@gmail.com

<p align="right">(<a href="#objectmotionnotify">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/screenshot.png


[Python.com]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/ 
[Telegram.com]: https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white
[Telegram-url]: https://core.telegram.org/  
[OpenCV.com]: https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white
[OpenCV-url]: https://opencv.org/

