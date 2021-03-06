'''
Represents an ambiguous surface form detected by wikiminer in a short text on the site
'''
from CONSTANT_VARIABLES import BASELINE_DbpediaSpotlight
from dataset_generation import nltk_extraction_dataset_mgr
from wikipedia import wikipedia_api_util
import text_util

class NamedEntity:
    ''' Represents a named entity detected in a short text.
    We use the entity's surface form as its unique identifier. That means that
    for short texts containing multiple entities with the same surface form, 
    we'll treat all occurrences as a single entity. '''
    
    def __init__(self, surface_form,
                 shorttext_id, shorttext_str,
                 username, site):
        '''
        @param surface_form: the surface form of the named entity this object represents
        @param shorttext_id: the ID of the short text that contains this entity
        @param shorttext_str: the string of the short text that contains this entity
        @param username: the username who authored the short text containing this entity
        @param site: the site on which the short text containing this entity was posted
        '''
        self.surface_form = surface_form
        self.shorttext_id = shorttext_id
        self.shorttext_str = shorttext_str
        self.username = username
        self.site = site
        
        # initialize the baseline candidate rankings, which each be a mapping 
        # from a candidate resource's title to its CandidateResource object
        self.wikipedia_miner_ranking = {}
        self.dbpedia_spotlight_ranking = {}
    
    def set_wikipedia_miner_ranking(self, wikipedia_miner_ranking):
        ''' @param wikipedia_miner_ranking: a ranking of CandidateResources according to Wikipedia Miner, 
        which should be a dict of candidate resource title to CandidateResource object ''' 
        self.wikipedia_miner_ranking = wikipedia_miner_ranking
        
    def set_dbpedia_spotlight_ranking(self, dbpedia_spotlight_ranking):
        ''' @param dbpedia_spotlight_ranking: a ranking of CandidateResources according to DBPedia Spotlight,
        which should be a dict of candidate resource title to CandidateResource object  '''  
        self.dbpedia_spotlight_ranking = dbpedia_spotlight_ranking
        
    def get_entity_id(self):
        ''' Using the containing short text's ID concatenated 
        with this entity's surface form as the entity's ID '''
        return str(self.shorttext_id)+"_"+str(self.surface_form)
    
    def get_surface_form(self):
        return self.surface_form.decode('latin-1')
        
    def get_short_text(self):
        return self.shorttext_str.decode('latin-1')
        
    def is_valid_entity(self, en_lang_users, valid_entity_cache):
        ''' @return: True if this is a valid named entity, otherwise returns False. 
        Currently the requirements are that this entity is at least two characters, 
        has at least 2 candidate resources (ie is ambiguous), is a noun, and is not
        an automated message through another service.'''
        
        # bypass users whose short text are not in English
        username = self.username
        if (not username in en_lang_users 
            or username=='rogermx' # this user tweets in Spanish..
            or username=='mentoz86' # this user has multiple non-English tweets..
            or username=='michitaro' # this user tweets in Japanese..
            or username=='tiyoringo'
            or username=='fabregas0414'
            or username=='jonkerz'
            or username=='mentoz86'
            or username=='kermanshahi'
            or username=='1veertje'
            ):
            return False
        
        if len(self.surface_form)<=1:
            return False # ignore single characters, which are probably resulting from buggy apostrophe stuff..
        
        if len(self.get_candidate_titles())<=1:
            return False # have to have at least 2 candidates to be ambiguous
        
        if text_util.is_unwanted_automated_msg(self.surface_form, self.shorttext_str):
            return False
        
        if not nltk_extraction_dataset_mgr.detectable_by_nltk(self.get_surface_form(), 
                                                              self.shorttext_id, 
                                                              valid_entity_cache):
            return False

        return True
    
    def get_candidate_titles(self):
        ''' Returns the titles of all the candidate resources 
        detected by wikipedia miner and/or dbpedia spotlight '''
        wikiminer_cand_objs = self.wikipedia_miner_ranking
        dbpedia_cand_objs = self.dbpedia_spotlight_ranking
        
        wikiminer_cand_titles = set([candidate_obj.title for candidate_obj in wikiminer_cand_objs.values()])
        dbpedia_cand_titles = set([candidate_obj.title for candidate_obj in dbpedia_cand_objs.values()])
        candidate_titles = list(wikiminer_cand_titles.union(dbpedia_cand_titles))
        return candidate_titles   
    
    def get_candidate_wikiURLs(self):
        ''' Returns the wikipedia page URLs of all the candidate resources 
        detected by wikipedia miner and/or dbpedia spotlight '''
        candidate_titles = self.get_candidate_titles()
        candidate_URLs = [wikipedia_api_util.get_wikipedia_page_url(candidate_title) 
                          for candidate_title in candidate_titles]
        return candidate_URLs
    
    
class CandidateResource:
    ''' Represents a candidate resource that an ambiguous named entity may refer to. ''' 
        
    def __init__(self, title, dbpedia_URI, score):
        '''
        @param title: The title of this candidate's wikipedia/dbpedia page (same thing) 
        @param dbpedia_URI: The URI of this candidate's dbpedia resource page
        @param score: A tuple of (algorithm_id, float_score) where algorithm is the id of
        the service or RESLVE ranking function that calculated and returned the float score.
        Note that float score is the score output by the service or algorithm ie it doesn't 
        have to be normalized to be between 0-1 because that will be done elsewhere
        '''
        self.title = title
        self.dbpedia_URI = dbpedia_URI
        self.score = score
        
    def get_score(self):
        ''' Providing a function for this because the DBPedia Spotlight 
        scores will be in unicode, which we want to decode '''    
        (algorithm_id, float_score) = self.score
        if algorithm_id==BASELINE_DbpediaSpotlight:
            return float(float_score.decode('utf-8'))
        return float_score
  
#    def is_valid_type(self, valid_candidate_cache):
#        if self.get_wikipedia_page() in valid_candidate_cache:
#            return True
#        
#        response = urllib2.urlopen("http://dbpedia.org/data/"+self.title+".json").read()
#        response = simplejson.loads(response.decode('utf-8'))
#        resource_data = response[self.dbpedia_URI]
#        
#        rdftype_key = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
#        if rdftype_key in resource_data: 
#            rdf_types = resource_data[rdftype_key]
#            for type_tuple in rdf_types:
#                if type_tuple['value'] in VALID_RDF_TYPES:
#                    return True
#                
#        # has no rdf type but can also test type using wikipedia category
#        # (ie has a high level category like people, place, etc within some number of direct parents 
#        # TODO
#        
#        # none of its associated types are what we consider valid
#        return False
