from WebsiteAPIInterface import WebsiteAPIInterface
from EntryState import EntryState

class Entry :

    def __init__(self) :
        self.title = None
        self.link = None
        self.source = None
        self.seasons = None
        self.selected_season = None
        self.episodes = None
        self.selected_episode = None
        self.m3u8_link = None

        self.curr_link = self.link
        self.entry_state = EntryState.ASK_FOR_QUERY

    
    def get_m3u8_link(self) :
        self.m3u8_link = self.source.get_m3u8_link(self.curr_link)
        return self.m3u8_link

    def get_seasons(self) :
        self.seasons = self.source.get_seasons(self.curr_link)
        return self.seasons

    def get_episodes(self) :
        self.episodes = self.source.get_episodes(self.curr_link)
        return self.episodes


    def set_query_selected(self, title: str, link: str, source: WebsiteAPIInterface) :
        self.title = title
        self.link = link
        self.source = source
        self.is_movie = self.source.is_movie(link)
        self.contains_seasons = self.source.contains_seasons(link)
        self.curr_link = link
        self.entry_state = EntryState.QUERY_SELECTED

    def set_season_selected(self, selected_season: dict) :
        self.selected_season = selected_season
        self.curr_link = selected_season["link"]
        self.entry_state = EntryState.SEASON_SELECTED
    
    def set_episode_selected(self, selected_episode: dict) :
        self.selected_episode = selected_episode
        self.curr_link = selected_episode["link"]
        self.entry_state = EntryState.EPISODE_SELECTD
    
    def set_playing(self) :
        self.entry_state = EntryState.PLAYING
    
    def is_movie(self) :
        return self.source.is_movie(self.curr_link)

    def contains_seasons(self) :
        return self.source.contains_seasons(self.curr_link)

    def revers_state(self) :
        if self.entry_state == EntryState.EPISODE_SELECTD :
            self.selected_episode = None
            self.curr_link = self.selected_season["link"]
            self.entry_state = EntryState.SEASON_SELECTED
        elif self.entry_state == EntryState.SEASON_SELECTED :
            self.selected_season = None
            self.curr_link = self.link
            self.entry_state = EntryState.RESULT_SELECTED
        elif self.entry_state == EntryState.PLAYING :
            self.m3u8_link = None
            self.curr_link = self.selected_season["link"] if self.selected_season else self.link
            self.entry_state = EntryState.SEASON_SELECTED if self.selected_season else EntryState.RESULT_SELECTED
    
    def get_state(self) :
        return self.entry_state
    
    def __str__(self) :
        return f"Title: {self.title}\nLink: {self.link}\nSource: {self.source}\nIs Movie: {self.is_movie}\nContains Seasons: {self.contains_seasons}\nSeasons: {self.seasons}\nSelected Season: {self.selected_season}\nEpisodes: {self.episodes}\nSelected Episode: {self.selected_episode}\nM3U8 Link: {self.m3u8_link}\nEntry State: {self.entry_state}"