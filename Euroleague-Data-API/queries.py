import strawberry
from typing import Optional, List
from resolvers import get_clubs, get_club_by_code, get_club_info, get_game_report, get_player_traditional
from structures import Club, GameReport, PlayerTraditionalResponse
from enum_code import ClubCode, CompetitionCode, CompetitionCode, SeasonMode, PhaseTypeCode, StatsMode, StatsSortMode, Stats, SortDirection

@strawberry.type
class Query:

    @strawberry.field
    def clubs(self, limit: Optional[int] = 10, offset: Optional[int] = 0) -> List[Club]:
        """
        Fetches a list of clubs with optional limit and offset.
        
        Args:
            limit (Optional[int]): The maximum number of clubs to return.
            offset (Optional[int]): The offset for pagination.
        
        Returns:
            List[Club]: A list of Club objects.
        """
        return get_clubs(limit=limit, offset=offset)

    @strawberry.field
    def club_by_code(self, club_code: ClubCode) -> Optional[Club]:
        """
        Fetch a specific club by its code from the Euroleague API.
        
        Args:
            club_code (ClubCode): The enum value representing the club code.
        
        Returns:
            Optional[Club]: The Club object corresponding to the club code, or None if not found.
        """
        return get_club_by_code(club_code)


    @strawberry.field
    def club_info(self, club_code: ClubCode) -> Optional[str]:
        """
        Fetch additional info for a specific club by its code.
        
        Args:
            club_code (ClubCode): The enum value representing the club code.
        
        Returns:
            Optional[str]: The info string returned by the API, or None if not found.
        """
        return get_club_info(club_code.name)
    
    @strawberry.field
    def game_report(self, competition_code: CompetitionCode = CompetitionCode.E.value, year: int = 2024, game_code: int = 1) -> Optional[GameReport]:
        """
        Fetches the game report for a specific game based on competitionCode, season year, and gameCode.
        
        Args:
            competition_code (CompetitionCode): The enum value representing the competition.
            year (int): The year of the season (YYYY format).
            game_code (int): The game code.
        
        Returns:
            Optional[GameReport]: The game report or None if not found.
        """
        return get_game_report(competition_code, year, game_code)
    
    @strawberry.field
    def player_traditional(
        self,
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
        return get_player_traditional(
            competition_code=competition_code,
            season_mode=season_mode,
            season_code=season_code,
            from_season_code=from_season_code,
            to_season_code=to_season_code,
            phase_type_code=phase_type_code,
            statistic_mode=statistic_mode,
            statistic_sort_mode=statistic_sort_mode,
            statistic=statistic,
            sort_direction=sort_direction,
            offset=offset,
            limit=limit
        )