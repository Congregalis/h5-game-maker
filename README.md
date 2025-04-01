
# Simple Game Generator 🎮

A HTML5 game generator built with [Agno](https://github.com/agno-agi/agno) framework and Google Gemini model that creates playable games from text descriptions.

## Features

- 🎯 Generate complete HTML5 games from text prompts
- 🎨 Games include fullscreen mode and instructions
- 🔄 Built-in game restart and exit functionality
- ✨ Multiple game examples included
- 💾 Download game source code

## Quick Start

### 1. Create a virtual environment

```shell
uv venv
source .venv\Scripts\activate
```

### 2. Install requirements

```shell
uv install -r ./requirements.txt
```

### 3. Configure Google API Key

Two options:
1. Set environmne variable:
```shell
export GOOGLE_API_KEY=your-api-key
```
2. Or enter directly in the app interface


### 4. Run Application

```shell
streamlit run app.py
```

## Example Games
- 🐍 Snake: Grows longer as it eats food
- 🧱 Breakout: Colorful blocks with power-ups
- 👾 Space Invaders: Multiple enemy types
- 🦘 Platformer: Basic jumping mechanics

## Requirements
- Python3.8+
- Google API KEY(from Google AI Studio)
- A network environment where Gemini can be used