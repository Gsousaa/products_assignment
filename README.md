# Products Assignment

![image](https://github.com/user-attachments/assets/c84a0f65-7a93-43ac-900c-1a3b92084b7b)


## Project Idea

The project's goal is to scrape and process information from the Market Watch portal to capture data related to the performance and competitors of a specific stock. Additionally, it will communicate with the Polygon API to find information such as the stock's status and open/close prices. The code is developed in Python using the FastAPI framework to build an API with two available endpoints. The first is a GET endpoint that returns general information about a stock. The second endpoint is for registering purchased stocks and the acquired quantity. For example, when checking the details of a stock purchase via the GET endpoint, it will show that a purchase was made and the quantity of shares acquired.

## Crawler Structure
For the web scraping component, the code uses the requests and BeautifulSoup libraries to interact with and make available the information by directly requesting the HTML code of the page, simulating the behavior of a human agent. The header below is an example:

```
{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com.br/"
}
```

In the code above, several important fields can be noted, such as "Referer," which indicates the point of origin or the site from which access to the application was initiated. This helps avoid blocks that the bot might face. The "Accept" line defines the type of response that is accepted/expected when making a request. Without these details, the bot's communication might be blocked by a Captcha or by the site's robots.txt, which allows access to only some endpoints.

## Alternative Sources
As an alternative for scenarios where blocking occurs, I created another path where information is fetched from two portals: MarketBeat, which follows a similar process as MarketWatch, downloading the HTML to return information about competitors and the market cap of each, and the Yahoo Finance API to retrieve performance data as expected.

## Data Unification
Finally, the scraped information is unified to ensure that the data returned does not break and is as accurate as possible.

## Tech

- Python - Utilized as the primary programming language for development, offering versatility and extensive library support.
- FastAPI - Implemented as the web framework for building a high-performance API, leveraging asynchronous features for better handling of concurrent requests.
- PostgreSQL - Employed as the relational database management system (RDBMS) for storing and managing structured data efficiently, offering powerful querying capabilities.
- BeautifulSoup - Used to parse and extract data from HTML content, in conjunction with the requests library, to simulate browser-like requests for web scraping tasks.
- Docker - Utilized for containerization, enabling consistent and isolated environments for deployment and execution, ensuring easy scalability and management across different platforms.

# Installation

### Prerequisites
To run this application using Docker, make sure you have the following installed:

- Docker: Verify that Docker is installed by running:
```
docker --version
```
If Docker is not installed, download and install it from the official Docker website.
- Docker Compose (Optional but recommended if using docker-compose.yml). Check if Docker Compose is installed:
```
docker-compose --version
```
If not installed, follow the instructions on the Docker Compose website.
### Steps to Run the Project
- Clone the Repository:

Open a terminal and clone the repository
```
git clone https://github.com/your-username/your-repository.git
```

 - Build the Docker Image:
```
docker build -t fastapi_app .
```
- Run the Docker Compose. This command will set up the database and application, making sure all services are running.:
```
docker-compose up -d
```
- Access the FastAPI Application:
```
The FastAPI endpoint will be available at http://localhost:8000.
You can access the interactive API documentation at http://localhost:8000/docs.
```
- Verify Database Connection. The PostgreSQL database is set to use port 5432. Ensure this port is available on your host machine.
