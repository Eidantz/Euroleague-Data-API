# resolvers.py
from typing import List, Optional
from structures import (Club, Venue, Images, Country, GameReport, Group, PhaseType, Season, 
                        GameTeam, GameClub,PlayerTraditionalResponse, PlayerTraditionalStatistics, Player, PlayerTeam)
from utilities import make_euroleague_request_v3
from enum_code import ClubCode, CompetitionCode, CompetitionCode, SeasonMode, PhaseTypeCode, StatsMode, StatsSortMode, Stats, SortDirection


def get_clubs(limit: Optional[int] = 10, 
              offset: Optional[int] = 0, 
              has_parent_club: Optional[bool] = None, 
              search: Optional[str] = None) -> List[Club]:
    
    params = {
        "Limit": limit,
        "Offset": offset,
        "hasParentClub": has_parent_club,
        "search": search
    }

    # Use the utility function to make the API request
    data = make_euroleague_request_v3("clubs", params)

    clubs_data = []
    for club in data.get('data', []):
        
        # Convert country dict to Country object
        if 'country' in club and club['country']:
            club['country'] = Country(**club['country']) 
        if club['images'].get('crest', False):
            club['images'] = Images(**club['images']) 
        else:
            club['images'] = Images(crest="")
        
        # Convert venue and handle images
        if 'venue' in club and club['venue']:
            venue_data = club['venue']
            
            # Check if 'images' exists and is a dictionary
            if 'images' in venue_data and isinstance(venue_data['images'], dict):
                images_data = venue_data['images']
                
                # Use empty string if 'crest' is missing
                crest_value = images_data.get('crest', "")
                
                # Assign to the Images class
                venue_data['images'] = Images(crest=crest_value)
            else:
                venue_data['images'] = Images(crest="")  # Set empty string if no images exist
            
            # Convert venue dict to Venue object
            club['venue'] = Venue(**venue_data)  
        
        # Convert venueBackup and handle images similarly
        if 'venueBackup' in club and club['venueBackup']:
            venue_backup_data = club['venueBackup']
            
            # Handle images in venueBackup the same way
            if 'images' in venue_backup_data and isinstance(venue_backup_data['images'], dict):
                images_data = venue_backup_data['images']
                crest_value = images_data.get('crest', "")
                venue_backup_data['images'] = Images(crest=crest_value)
            else:
                venue_backup_data['images'] = Images(crest="")  # Set empty string if no images exist
            
            club['venueBackup'] = Venue(**venue_backup_data)  # Convert venueBackup dict to Venue object
        
        # Convert club dict to Club object
        clubs_data.append(Club(**club))  

    return clubs_data


def get_club_by_code(club_code: ClubCode) -> Club:
    """
    Fetches a club by its code from the Euroleague API using ClubCode enum.
    
    Args:
        club_code (ClubCode): The enum value representing the club's code.
    
    Returns:
        Club: The Club object corresponding to the clubCode.
    """
    # Get the club code string from the enum
    endpoint = f"clubs/{club_code.name}"
    
    data = make_euroleague_request_v3(endpoint)
    
    # Convert to Club object
    if 'country' in data and data['country']:
        data['country'] = Country(**data['country'])
    
    if data['images'].get('crest', False):
        data['images'] = Images(**data['images'])
    else:
        data['images'] = Images(crest="")

    if 'venue' in data and data['venue']:
        venue_data = data['venue']
        if 'images' in venue_data and isinstance(venue_data['images'], dict):
            images_data = venue_data['images']
            crest_value = images_data.get('crest', "")
            venue_data['images'] = Images(crest=crest_value)
        else:
            venue_data['images'] = Images(crest="")
        data['venue'] = Venue(**venue_data)
    
    if 'venueBackup' in data and data['venueBackup']:
        venue_backup_data = data['venueBackup']
        if 'images' in venue_backup_data and isinstance(venue_backup_data['images'], dict):
            crest_value = venue_backup_data['images'].get('crest', "")
            venue_backup_data['images'] = Images(crest=crest_value)
        else:
            venue_backup_data['images'] = Images(crest="")
        data['venueBackup'] = Venue(**venue_backup_data)

    return Club(**data)


def get_club_info(club_code: ClubCode) -> str:
    """
    Fetches additional info for a club by its code from the Euroleague API.
    
    Args:
        club_code (str): The code of the club to fetch info for.
    
    Returns:
        str: The 'info' field returned from the API.
    """
    endpoint = f"clubs/{club_code}/info"
    data = make_euroleague_request_v3(endpoint)
    
    # Return the 'info' field from the response
    return data.get('info', '')

def get_game_report(competition_code: CompetitionCode, year: int, game_code: int) -> GameReport:
    """
    Fetch the game report for a specific game using the competitionCode, seasonCode, and gameCode.
    
    Args:
        competition_code (CompetitionCode): The enum value representing the competition code.
        year (int): The year of the season (YYYY format).
        game_code (int): The game code.
    
    Returns:
        GameReport: The game report object containing detailed game information.
    """
    season_code = f"{competition_code.name}{year}"  # Construct seasonCode
    endpoint = f"competitions/{competition_code.name}/seasons/{season_code}/games/{game_code}/report"
    data = make_euroleague_request_v3(endpoint)
    
    # Map the API data to strawberry types manually
    season_data = data.get('season', {})
    season = Season(
        name=season_data.get('name'),
        code=season_data.get('code'),
        alias=season_data.get('alias'),
        competitionCode=season_data.get('competitionCode'),
        year=season_data.get('year'),
        startDate=season_data.get('startDate')
    )
    
    group_data = data.get('group', {})
    group = Group(
        id=group_data.get('id'),
        order=group_data.get('order'),
        name=group_data.get('name'),
        rawName=group_data.get('rawName')
    )
    
    # Handle GameClub mapping with crest handling for both local and road teams
    def map_game_club(club_data):
        if 'images' in club_data and isinstance(club_data['images'], dict):
            images_data = club_data['images']
            crest_value = images_data.get('crest', "")
            club_data['images'] = Images(crest=crest_value)
        else:
            club_data['images'] = Images(crest="")  # Set empty string if no images exist
        
        return GameClub(**club_data)
    
    local_team_data = data.get('local', {})
    local_team = GameTeam(
        club=map_game_club(local_team_data.get('club', {})),
        score=local_team_data.get('score'),
        standingsScore=local_team_data.get('standingsScore')
    )
    
    road_team_data = data.get('road', {})
    road_team = GameTeam(
        club=map_game_club(road_team_data.get('club', {})),
        score=road_team_data.get('score'),
        standingsScore=road_team_data.get('standingsScore')
    )
    
    # Map the rest of the fields
    return GameReport(
        gameCode=data.get('gameCode'),
        season=season,
        group=group,
        phaseType=PhaseType(**data.get('phaseType', {})),
        round=data.get('round'),
        roundAlias=data.get('roundAlias'),
        roundName=data.get('roundName'),
        played=data.get('played'),
        date=data.get('date'),
        confirmedDate=data.get('confirmedDate'),
        confirmedHour=data.get('confirmedHour'),
        localTimeZone=data.get('localTimeZone'),
        localDate=data.get('localDate'),
        utcDate=data.get('utcDate'),
        local=local_team,
        road=road_team,
        localLast5Form=data.get('localLast5Form', []),
        roadLast5Form=data.get('roadLast5Form', [])
    )


def get_player_traditional(
    competition_code: CompetitionCode,
    season_mode: Optional[SeasonMode] = None,
    season_code: Optional[int] = None,
    from_season_code: Optional[int] = None,
    to_season_code: Optional[int] = None,
    phase_type_code: Optional[PhaseTypeCode] = None,
    statistic_mode: Optional[StatsMode] = None,
    statistic_sort_mode: Optional[StatsSortMode] = None,
    statistic: Optional[Stats] = None,
    sort_direction: Optional[SortDirection] = None,
    offset: Optional[int] = 0,
    limit: Optional[int] = 10
) -> PlayerTraditionalResponse:
    
    endpoint = f"competitions/{competition_code.name}/statistics/players/traditional"
    
    # Prepare query parameters
    params = {
        "SeasonMode": season_mode.value if season_mode else None,
        "SeasonCode": f"{competition_code.name}{season_code}" if season_code else None,
        "FromSeasonCode": f"{competition_code.name}{from_season_code}" if from_season_code else None,
        "ToSeasonCode": f"{competition_code.name}{to_season_code}" if to_season_code else None,
        "phaseTypeCode": phase_type_code.value if phase_type_code else None,
        "statisticMode": statistic_mode.value if statistic_mode else None,
        "statisticSortMode": statistic_sort_mode.value if statistic_sort_mode else None,
        "statistic": statistic.value if statistic else None,
        "sortDirection": sort_direction.value if sort_direction else None,
        "Offset": offset,
        "Limit": limit
    }
    
    # Make the request
    data = make_euroleague_request_v3(endpoint, params=params)
    
    # Map the data to the structures
    players = [
        PlayerTraditionalStatistics(
            playerRanking=player_data.get('playerRanking'),
            player=Player(
                code=player_data['player'].get('code'),
                name=player_data['player'].get('name'),
                age=player_data['player'].get('age'),
                imageUrl=player_data['player'].get('imageUrl'),
                team=PlayerTeam(**player_data['player']['team'])
            ),
            gamesPlayed=player_data.get('gamesPlayed'),
            gamesStarted=player_data.get('gamesStarted'),
            minutesPlayed=player_data.get('minutesPlayed'),
            pointsScored=player_data.get('pointsScored'),
            twoPointersMade=player_data.get('twoPointersMade'),
            twoPointersAttempted=player_data.get('twoPointersAttempted'),
            twoPointersPercentage=player_data.get('twoPointersPercentage'),
            threePointersMade=player_data.get('threePointersMade'),
            threePointersAttempted=player_data.get('threePointersAttempted'),
            threePointersPercentage=player_data.get('threePointersPercentage'),
            freeThrowsMade=player_data.get('freeThrowsMade'),
            freeThrowsAttempted=player_data.get('freeThrowsAttempted'),
            freeThrowsPercentage=player_data.get('freeThrowsPercentage'),
            offensiveRebounds=player_data.get('offensiveRebounds'),
            defensiveRebounds=player_data.get('defensiveRebounds'),
            totalRebounds=player_data.get('totalRebounds'),
            assists=player_data.get('assists'),
            steals=player_data.get('steals'),
            turnovers=player_data.get('turnovers'),
            blocks=player_data.get('blocks'),
            blocksAgainst=player_data.get('blocksAgainst'),
            foulsCommited=player_data.get('foulsCommited'),
            foulsDrawn=player_data.get('foulsDrawn'),
            pir=player_data.get('pir')
        )
        for player_data in data.get('players', [])
    ]
    
    return PlayerTraditionalResponse(
        total=data.get('total'),
        players=players
    )