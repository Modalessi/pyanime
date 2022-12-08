
class WebsiteAPIInterface() :
    # Interface for all WebsitesAPIs
    
    # every website api needs to have constant contains the website name
    WEBSITE_NAME = "WEBSITE_NAME"
    
    def search(query: str)-> list :
        '''
        search for a query in the website and return results in a list of dicts
        with the following format
        {
            "title of the result" : str
            "link" : str
        }
        '''
    
    
    def is_movie(link: str)-> bool :
        '''
        return wether the webpage link is a movie or not
        '''
    
    
    def contains_seasons(link: str)-> bool :
        '''
        return wether the webpage contains seasons or not
        '''
    
    
    
    def get_seasons(link: str)-> list :
        '''
        should return all seasons in a an array of dicts
        with the following format
        {
            "title of the season" : str
            "link" : str
            "index" : int
        }
        '''
        
        
        
        
    def get_episodes(result: dict)-> list :
        '''
        should return all episodes in a an array of dicts
        with the following format
        {
            "title of the episode" : str
            "link" : str
            "index" : int
        }
        '''
        
    
    
    def get_m3u8_link(result: dict)-> str :
        '''
        should return m3u8 link for an episode or a movie
        in order to pass to a media player
        '''