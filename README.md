# 📘 RoboDodge

A simple block dodging game written in Python. Gets fast and out of control very quickly!

## ✨ Features

-   🚀 Original artwork
-   ⏱️ Quick time wasting exercise
-   📈 Procrastination aid
-   📦 Easy to run and play
-   ✅ Utterly pointless

## 🚀 Demo

Want a taste of what's in store?

Check out the [Live Demo](https://github.com/sedexdev/robo-dodge/tree/master/assets/video/sample.webm)!

## 📦 Installation

### Prerequisites

```bash
Python >= 3.12
```

### Local Setup

```bash
# Clone the repository
git clone https://github.com/sedexdev/robo-dodge.git
```

## ⚙️ Configuration

> Use a soundtrack of your choice for the game audio

Create a directory called `audio` under the `assets` directory:

```bash
mkdir assets/audio
```

Copy a `.mp3` file of your favourite song into this folder and rename it `theme.mp3`:

```bash
cp /path/to/your/song.mp3 assets/audio
mv assets/audio/song.mp3 assets/audio/theme.mp3
```

> Install pygame in a virtual environment

```bash
virtualenv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

## 🛠️ Usage

### 🎮 Running the game

```bash
cd robo-dodge
python3 main.py
```

### 🕹️ Controls

-   `Right arrow` - move right
-   `Left arrow` - move left

## 📂 Project Structure

```
robo-dodge/
│
├── assets/                 # Images and audio
├── src/                    # Source files
├── .gitignore              # Git ignore file
├── main.py                 # GitHub workflows and issue templates
├── README.md               # This README.md file
└── requirements.txt        # Dependencies
```

## 🐛 Reporting Issues

Found a bug or need a feature? Open an issue [here](https://github.com/sedexdev/robo-dodge/issues).

## 🧑‍💻 Authors

-   **Andrew Macmillan** – [@sedexdev](https://github.com/sedexdev)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
