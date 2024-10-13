import strawberry
from typing import Optional, Dict, Any, List

@strawberry.type
class Images:
    crest: Optional[str]



@strawberry.type
class Venue:
    name: Optional[str]
    code: Optional[str]
    capacity: Optional[int]
    address: Optional[str]
    images: Optional[Images]
    active: Optional[bool]
    notes: Optional[str]

@strawberry.type
class Country:
    code: Optional[str]
    name: Optional[str]

@strawberry.type
class Club:
    code: Optional[str]
    name: Optional[str]
    alias: Optional[str]
    
    # Use python_name to map the API's 'isVirtual' to the internal 'is_virtual'
    isVirtual: Optional[bool] = strawberry.field(name="is_virtual")
    
    country: Optional[Country]
    address: Optional[str]
    website: Optional[str]
    ticketsUrl: Optional[str]
    twitterAccount: Optional[str] = strawberry.field(name="twitter_account")
    instagramAccount: Optional[str] = strawberry.field(name="instagram_account")
    facebookAccount: Optional[str] = strawberry.field(name="facebook_account")
    venue: Optional[Venue]
    venueBackup: Optional[Venue]
    nationalCompetitionCode: Optional[str] = strawberry.field(name="national_competition_code")
    city: Optional[str]
    president: Optional[str]
    phone: Optional[str]
    fax: Optional[str]
    images: Optional[Images]


@strawberry.type
class Season:
    name: Optional[str]
    code: Optional[str]
    alias: Optional[str]
    competitionCode: Optional[str]
    year: Optional[int]
    startDate: Optional[str]

@strawberry.type
class GameClub:
    code: Optional[str]
    name: Optional[str]
    abbreviatedName: Optional[str]
    editorialName: Optional[str]
    tvCode: Optional[str]
    isVirtual: Optional[bool]
    images: Optional[Images]

@strawberry.type
class GameTeam:
    club: Optional[GameClub]
    score: Optional[int]
    standingsScore: Optional[int]

@strawberry.type
class PhaseType:
    code: Optional[str]
    alias: Optional[str]
    name: Optional[str]
    isGroupPhase: Optional[bool]

@strawberry.type
class Group:
    id: Optional[str]
    order: Optional[int]
    name: Optional[str]
    rawName: Optional[str]

@strawberry.type
class GameReport:
    gameCode: Optional[int]
    season: Optional[Season]
    group: Optional[Group]
    phaseType: Optional[PhaseType]
    round: Optional[int]
    roundAlias: Optional[str]
    roundName: Optional[str]
    played: Optional[bool]
    date: Optional[str]
    confirmedDate: Optional[bool]
    confirmedHour: Optional[bool]
    localTimeZone: Optional[int]
    localDate: Optional[str]
    utcDate: Optional[str]
    local: Optional[GameTeam]
    road: Optional[GameTeam]
    localLast5Form: Optional[List[str]]
    roadLast5Form: Optional[List[str]]

@strawberry.type
class PlayerTeam:
    code: Optional[str]
    tvCodes: Optional[str]
    name: Optional[str]
    imageUrl: Optional[str]

@strawberry.type
class Player:
    code: Optional[str]
    name: Optional[str]
    age: Optional[int]
    imageUrl: Optional[str]
    team: Optional[PlayerTeam]

@strawberry.type
class PlayerTraditionalStatistics:
    playerRanking: Optional[int]
    player: Optional[Player]
    gamesPlayed: Optional[float]
    gamesStarted: Optional[float]
    minutesPlayed: Optional[float]
    pointsScored: Optional[float]
    twoPointersMade: Optional[float]
    twoPointersAttempted: Optional[float]
    twoPointersPercentage: Optional[str]
    threePointersMade: Optional[float]
    threePointersAttempted: Optional[float]
    threePointersPercentage: Optional[str]
    freeThrowsMade: Optional[float]
    freeThrowsAttempted: Optional[float]
    freeThrowsPercentage: Optional[str]
    offensiveRebounds: Optional[float]
    defensiveRebounds: Optional[float]
    totalRebounds: Optional[float]
    assists: Optional[float]
    steals: Optional[float]
    turnovers: Optional[float]
    blocks: Optional[float]
    blocksAgainst: Optional[float]
    foulsCommited: Optional[float]
    foulsDrawn: Optional[float]
    pir: Optional[float]

@strawberry.type
class PlayerTraditionalResponse:
    total: Optional[int]
    players: Optional[List[PlayerTraditionalStatistics]]
