<p id="top"></p>

# Attitude-Visualizer: Emoji-Based Telegram Post Analytics

![Project Logo](https://i.imgur.com/1cP0FBF.png)

## Table of Contents

- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Getting Started](#getting-started)
    - [Installation Steps](#installation-steps)
    - [Configuring Telegram API](#configuring-telegram-api)
- [Emoji Sentiment Analysis](#emoji-sentiment-analysis)
- [How to Use](#how-to-use)
- [Web UI Features](#web-ui-features)
- [Contribution Guidelines](#contribution-guidelines)
- [License Information](#license-information)

---

## Overview

The Attitude-Visualizer project offers an intuitive way to gauge user reactions to posts on a Telegram channel. It
fetches messages using the Telegram API, analyzes emojis in reactions, and visualizes the sentiment and popularity of
each post. This project is built on FastAPI and uses the Telethon library for Telegram API interactions.

---

## System Requirements

- Python version 3.8 or above
- FastAPI library

---

## Getting Started

### Installation Steps

1. **Clone the Project Repository**
    ```bash
    git clone https://github.com/vvvlladimir/Attitude-Visualizer.git
    ```
2. **Enter the Project Folder**
    ```bash
    cd Attitude-Visualizer
    ```
3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

### Configuring Telegram API

1. **Sign In to Telegram**: Log in using a phone number associated with the developer account.
2. **Navigate to API Development Tools**: Go to [API Development tools](https://my.telegram.org/auth?to=apps).
3. **Create a New App**: Fill in the necessary details. Only the first two fields (App title and Short
   name) can be modified later. No need to provide a URL
4. **Obtain API Credentials**: Take note of your API ID and Hash.

⚠️ **Caution**: Keep your API & Hash private; Telegram does not allow you to revoke it.

For more on using Telethon for sign-in, visit
the [Telethon documentation](https://docs.telethon.dev/en/stable/basic/signing-in.html).

---

## Emoji Sentiment Analysis

The project uses a neural network to assign sentiment scores to emojis, which are stored in `emoji_scores.json`. These
scores range from -1 to 1, representing the emotional tone of each emoji. The program matches fetched emojis with these
scores to derive an overall sentiment score for each post.

---

## How to Use

1. **Launch FastAPI Server**
    ```bash
    uvicorn main:app --reload
    ```
2. **Access Web Interface**: Open the local web UI in your preferred browser.

---

## Web UI Features

1. **API Credentials**: Input your Telegram API ID and Hash.
2. **Post Settings**: Select the range and number of posts to analyze.
3. **Channel Identifier**: Enter the Telegram channel's tag.
4. **Start Analysis**: Click "start" to begin fetching and analyzing posts.
5. **Manage Data**: Download or delete generated JSON files.
6. **Visualization**: View the sentiment and popularity of posts through a graphical representation.

### Enhanced UI (Optional)

For those who wish to enhance the UI with custom overflow colors, you can optionally use
the [Overflow Color script](https://github.com/dimitrinicolas/overflow-color.git).

To install the script, run:

```bash
npm i overflow-color
```

### Video

---

## Contribution Guidelines

Please refer to the [Contributing](CONTRIBUTING.md) section for more details.

---

## License Information

This project is licensed under the [MIT license](LICENSE).

---

<p align="right">
  <a href="#top"><b>Return</b></a>
</p>
