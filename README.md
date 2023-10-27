<p id="top"></p>

# Attitude-Visualizer: Emoji-Based Telegram Post Analytics

![Project Logo](https://github.com/vvvlladimir/Attitude-Visualizer/assets/57634619/8fad3d34-6da7-44f6-a89c-9e910733bc8c)

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Installation Steps](#installation-steps)
    - [Configuring Telegram API](#configuring-telegram-api)
- [Emoji Sentiment Analysis](#emoji-sentiment-analysis)
- [How to Use](#how-to-use)
- [Web UI Features](#web-ui-features)
    - [Enhanced UI (Optional)](#enhanced-ui-optional)
    - [Video](#video)
- [Contribution Guidelines](#contribution-guidelines)
- [License Information](#license-information)

---

## Overview

The Attitude-Visualizer project offers an intuitive way to gauge user reactions to posts on a Telegram channel. It
fetches messages using the Telegram API, analyzes emojis in reactions, and visualizes the sentiment and popularity of
each post. This project is built on FastAPI and uses the Telethon library for Telegram API interactions.

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
4. **You may have to install python-multipart**
    ```bash
    pip install python-multipart
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

The project used a neural network to assign sentiment scores to emoji, which are stored in the `emoji_scores.json` file.
These
scores range from -1 to 1, reflecting the emotional tone of each emoji relative to the others. The program matches the
selected emoji against these scores to get an overall sentiment score for each post. If you wish, you can
edit `emoji_scores.json` and add the emoji you want to use

---

## How to Use

1. Launch FastAPI Server
    ```bash
    python main.py
    ```
2. Open the local web UI in your preferred browser.
3. Specify all the necessary **data** and click the `start` button

4. At the **first launch**, the `client.session` file will be created in the main directory and you will need to enter
   your phone number and
   the code that will come to your telegram account in the terminal. _If you have two-factor authentication via
   password, you need to enter that as well._
5. On subsequent runs, you can omit the ID and HASH. If you want to change the account delete the `client.session` file
   and register with new data

⚠️ **Caution**: `client.session` and `config.json` contain **all access data** for your telegram account. **Never share
this file!**

---

## Web UI Features

1. **API Credentials**: Input your Telegram API ID and Hash.
2. **Post Settings**: Select the range and number of posts to analyze.
3. **Channel Identifier**: Enter the Telegram channel's tag.
4. **Start Analysis**: Click "start" to begin fetching and analyzing posts.
5. **Manage Data**: Download or delete generated JSON files.
6. **Visualization**: View the sentiment and popularity of posts through a graphical representation. The radius of each
   point shows the number of views of the post

### Enhanced UI (Optional)

For those who wish to enhance the UI with custom overflow colors, you can optionally use
the [Overflow Color script](https://github.com/dimitrinicolas/overflow-color.git).

To install the script, run:

```bash
npm i overflow-color
```

### Video



https://github.com/vvvlladimir/Attitude-Visualizer/assets/57634619/e290fba3-c79e-470f-a94d-1180d4561466



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
