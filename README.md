# Real-time Cryptocurrency Trading Strategy Checker

This is a project that allows users to obtain real-time price data from various cryptocurrency brokers, saves it to a database, triggers checks for trading strategies, and generates a link to a chart if the strategy is working on the data. It uses Python, Django, Redis, WebSocket, and JavaScript.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Architecture Overview](#architecture-overview)
- [Contributing](#contributing)
- [License](#license)

## Installation

To get started with this project, follow the instructions below.

1. Clone the repository

$ git clone https://github.com/your_username/realtime-crypto-strategy-checker.git
$ cd realtime-crypto-strategy-checker

2. Install dependencies

$ pip install -r requirements.txt


3. Configure environment variables

$ cp .env.example .env

Edit the `.env` file to include your API keys and other necessary configuration details.

4. Start the server

$ python manage.py runserver


## Usage

Once the server is up and running, you can visit the web interface to view real-time data, configure your trading strategies, and generate charts.

## Architecture Overview

This project is built using the following technologies:

- Python - for the backend and trading strategies
- Django - for the web framework
- Redis - for real-time data storage and processing
- WebSocket - for real-time communication between the client and server
- JavaScript - for the client-side web interface

The project is divided into several components:

- **Data Acquisition:** Real-time price data is obtained from various cryptocurrency brokers using their respective APIs. The data is then stored in Redis for processing.
- **Strategy Processing:** Trading strategies are implemented in Python and run on the real-time data in Redis. When a strategy is triggered, a message is sent to the client via WebSocket.
- **Web Interface:** The web interface allows users to view real-time data, configure trading strategies, and generate charts.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.