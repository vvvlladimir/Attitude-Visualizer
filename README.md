# Attitude-Visualizer

Visualize user reactions to Telegram channel posts through emoji analysis.
![Alt text](https://i.imgur.com/1cP0FBF.png)

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Telegram API Setup](#telegram-api-setup)
- [Emoji Analysis](#emoji-analysis)
- [Usage](#usage)
- [Example of Use](#example-of-use)
- [License](#license)

## Introduction
The Attitude-Visualizer project is designed to evaluate and visualize user reactions to specific posts in a Telegram channel. By fetching posts and analyzing the emojis used in reactions, it provides a standardized score for each post, which is then plotted on a graph for comparison.

## Prerequisites
1. Python installed on your machine.
2. A registered Telegram account with developer API credentials for the Telethon library.

## Installation
1. **Clone the Repository**
    ```bash
    git clone https://github.com/vvvlladimir/Attitude-Visualizer.git
    ```

2. **Navigate to the Project Directory**
    ```bash
    cd Attitude-Visualizer
    ```

3. **Install Required Packages**
    ```bash
    pip install -r requirements.txt
    ```

## Telegram API Setup
To interact with Telegram's API, you'll need to set up your own API ID and hash:

1. **Login to Telegram**: Use the phone number linked to the developer account you wish to use.
2. **Access API Development Tools**: Visit [API Development tools](https://my.telegram.org/auth?to=apps).
3. **Create a New Application**: Fill in the application details. Note: Only the first two fields (App title and Short name) can be modified later. No need to provide a URL.
4. **Generate Credentials**: Click on "Create application". **Keep your API hash confidential. Telegram won’t allow you to revoke it. Avoid sharing it publicly!**

For more details on Telethon sign-in, check the [official documentation](https://docs.telethon.dev/en/stable/basic/signing-in.html).

## Emoji Analysis
The project uses the `emoji_scores.json` file for emoji analysis. Each emoji has a score between -1 and 1, representing its emotional tone. These scores are based on a neural network analysis.

When the program fetches emojis from Telegram post reactions, it matches them with the scores in `emoji_scores.json`. The cumulative score of all emojis for a post gives the overall reaction score.

## Usage
Once everything is set up:

1. Run the application.
```bash
uvicorn main:app --reload   
```
2. Input your Telegram API ID and Hash on the main page.
3. Select the number of posts (Post Limit) to be processed and the offset from the last post (Post Offset).
4. Specify the channel tag with or without `@`
5. Push "start" button.


## Example of Use
1. **Launch the Application**: Start the Attitude-Visualizer application.
2. **Enter API Credentials**: On the main page, input all settings.
3. **Fetch Posts**: Click on the "start" button. The application will retrieve the latest posts from the specified Telegram channel.
4. **View Analysis**: After fetching, the application will analyze the emojis in the reactions and provide a score for each post.
5. **Visualize Data**: Each post will be displayed on the chart, you can hover over it, view its data and click on it, thereby opening a link to this post.
6. **JSON Files**: If desired, you can download the generated json files by simply clicking on the name or delete the file by clicking "Delete".



## License
[MIT](https://choosealicense.com/licenses/mit/)
