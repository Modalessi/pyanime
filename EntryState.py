from enum import Enum


class EntryState(Enum) :
    ASK_FOR_QUERY = 0
    QUERY_SELECTED = 1
    RESULT_SELECTED = 2
    SEASON_SELECTED = 3
    EPISODE_SELECTD = 4
    PLAYING = 5
