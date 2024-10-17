# Euroleague-Data-API

**Euroleague-Data-API** is a Python-based GraphQL API client that interacts with the Euroleague’s official API to retrieve data about clubs, games, players, and statistics. It provides users with an easy-to-use interface to work with Euroleague data, making it simple to integrate basketball data into your projects.

## Features

- Fetch comprehensive data about Euroleague clubs, including venue details, social media accounts, and addresses.
- Retrieve game reports, player statistics, and competition details.
- Support for various filters and parameters, including competition codes, season codes, and more.
- Built-in mapping for Euroleague competition codes, phase types, and statistical modes.
- Flexible API requests with optional parameters and pagination support.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Methods](#api-methods)
  - [Clubs](#clubs)
  - [Competitions](#competitions)
  - [Game Reports](#game-reports)
  - [Player Statistics](#player-statistics)
- [Enums](#enums)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install **Euroleague-Data-API**, clone the repository and install the dependencies:

```
git clone https://github.com/Eidantz/Euroleague-Data-API.git
cd Euroleague-Data-API
pip install -r requirements.txt
```

## Usage

The API is structured around GraphQL queries powered by **Strawberry GraphQL**. You can run the API server locally using **uvicorn**.

### Running the API
Run:
```
main.py
```

After starting the server, you can query the GraphQL API on `http://0.0.0.0:8000/graphql`.

### Example Query: Retrieve Clubs Information

You can fetch data about Euroleague clubs using this GraphQL query:

```
query {
  clubs(limit: 10) {
    code
    name
    country {
      name
    }
    venue {
      name
      capacity
    }
  }
}
```

## API Methods

### Clubs

Retrieve information about Euroleague clubs, including venue details and social media accounts.

- **Endpoint**: `/v3/clubs`
- **Parameters**:
  - `limit` (optional, int): The number of results to return.
  - `offset` (optional, int): Offset for pagination.
  - `has_parent_club` (optional, bool): Filter clubs by parent clubs.
  - `search` (optional, str): Search term for club names.

### Competitions

Retrieve data for a specific competition.

- **Endpoint**: `/v3/competitions/{competitionCode}`
- **Parameters**:
  - `competitionCode` (required): The code for the competition.

### Game Reports

Retrieve detailed reports for specific games within a competition and season.

- **Endpoint**: `/v3/competitions/{competitionCode}/seasons/{seasonCode}/games/{gameCode}/report`
- **Parameters**:
  - `competitionCode` (required, from enum).
  - `seasonCode` (required, formatted as `{competitionCodeYYYY}`).
  - `gameCode` (required, int).

### Player Statistics

Retrieve traditional player statistics, such as points scored, assists, and rebounds.

- **Endpoint**: `/v3/competitions/{competitionCode}/statistics/players/traditional`
- **Parameters**:
  - `competitionCode` (required, from enum).
  - `seasonCode` (optional, formatted as `{competitionCodeYYYY}`).
  - `limit`, `offset` (optional, int): Pagination parameters.

## Enums

The project includes several enums for structured data:

- **CompetitionCode**: Enum of competition codes such as `E` for Euroleague, `U` for Eurocup, and more.
- **PhaseTypeCode**: Enum for phase types in the competition.
- **StatsMode**: Enum for statistical modes like traditional, advanced, etc.
- **StatsSortMode**: Enum for sorting statistics.
- **SortDirection**: Enum for ascending or descending sorting.

## Contributing

We welcome contributions! Please submit pull requests and issues through the GitHub repository.

## License

This project is licensed under the **MIT License** - see the `LICENSE` file for details.

