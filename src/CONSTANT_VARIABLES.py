####### GLOBAL CONSTANT VARIABLES #######
from ranking_algorithms.article_VSM import Article_ContentBOW_VSM, \
    Article_ID_VSM, Article_TitleBOW_VSM
from ranking_algorithms.article_WSD import Article_ContentBOW_WSD
from ranking_algorithms.direct_categories import DirectCategory_ID_VSM, \
    DirectCategory_TitleBOW_VSM
from ranking_algorithms.graph_categories import CategoryGraph_ID_VSM, \
    CategoryGraph_TitleBOW_VSM

DEBUG_ON = False

''' Spreadsheet column strings that will be used to 
identify the same information in multiple spreadsheets: '''

COLUMN_USERNAME = 'username'

COLUMN_SHORTTEXT_ID = "shorttextID"
COLUMN_SHORTTEXT_STRING =  "shorttextString"

COLUMN_ENTITY_ID = "entityID"


''' Requirements to be considered an "active" user, ie minimum 
number of contributions on wikipedia/twitter/flickr/etc: '''

# Hauff: "Placing Images on the World Map": 10 on Twitter, 5 on Flickr
ACTIVE_WIKIPEDIA_MIN = 100 

# maximum number of pages most recently edited by a user on 
# Wikipedia that we'll consider; any more will result in an
# interest model that is too diverse and noisy?
# ACTIVE_WIKIPEDIA_MAX = 100

# Zhang, "Community Discovery in Twitter Based on User Interests": 100=active
# Lu, Lam, Zhang: "Twitter User Modeling...": 100=active
# Naaman, "Is it really about me": 10=active
# Counts, Fisher: "Taking It All In?": 10=active
ACTIVE_TWITTER_MIN = 100 


''' The identifiers for the various strategies we use to disambiguate
an entity (Turker judgements, toolkit services, RESLVE ranking functions): '''

GOLD_MechanicalTurker = 'mechanical_turk_judgement'

BASELINE_WikipediaMiner = 'wikipedia_miner_algorithm'
BASELINE_DbpediaSpotlight = 'dbpedia_spotlight_algorithm'


def get_RESLVE_algorithm_constructors():
    ''' The constructors of the various RESLVE algorithms
    that can be used to create a reslve_algorithm object '''
    
    # RESLVE algorithms based on articles' page content
    article_contentBowVsm = Article_ContentBOW_VSM
    article_idVsm = Article_ID_VSM
    article_titleBowVsm = Article_TitleBOW_VSM
    
    # RESLVE algorithms based on articles' direct categories
    directCategory_idVsm = DirectCategory_ID_VSM
    directCategory_titleBowVsm = DirectCategory_TitleBOW_VSM
    
    # RESLVE algorithms based on articles' full category hierarchy
    graphCategory_idVsm = CategoryGraph_ID_VSM
    graphCategory_titleBowVsm = CategoryGraph_TitleBOW_VSM

    # RESLVE algorithm based on WSD lesk approach
    articleContent_bowWsd = Article_ContentBOW_WSD
    
    reslve_algorithms = [article_contentBowVsm, article_idVsm, article_titleBowVsm, 
                         directCategory_idVsm, directCategory_titleBowVsm, 
                         graphCategory_idVsm, graphCategory_titleBowVsm, 
                         articleContent_bowWsd]
    return reslve_algorithms


# Entity types we restrict our sample to. (See http://schema.org/Thing)
VALID_RDF_TYPES = ['http://schema.org/CreativeWork',
                   'http://schema.org/Event',
                   #'http://schema.org/Intangible',
                   'http://schema.org/MedicalEntity',
                   'http://schema.org/Organization',
                   'http://schema.org/Person',
                   'http://schema.org/Place',
                   'http://schema.org/Product']