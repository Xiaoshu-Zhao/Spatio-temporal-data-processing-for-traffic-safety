from utils.Crawler import search_by_tweet_id
import itertools
import pandas as pd

class Tweets_location:
    userid = ['CROSSMARKJobs','JeffreyHines80','511NY','511NYMidHudson',
 'Manhattanpeachy','robbwil1','CTDOT_District1','CTDOT_Statewide',
 'shellfaber6','XclusiveArrival','HalterTop34','kyny889','iamnatemyles',
 'rocdabroski', 'josephmariko','chrisiestyles', 'RockStarr65',
 'coachmlewis33', 'TotalTrafficPHL', 'BlazeMusicNet', 'LsarowarRBLX2nd',
 'BGWritesStuff', 'BKSoulStew', 'j_rakowski', 'WWFarmersMarket',
 'DeWittGodfrey', 'rchiarellajewel', 'NWS_MountHolly', 'NWSSevereTstorm',
 'Devilsfan79', 'algattullo', 'iembot_phi', 'yankee32879', 'adampicz',
 'KennethFerrone', 'dhsbaseballnj', 'AnthonyPPinto', '5feetoffashion', 'Grafh',
 'DJBEEBLACK', 'hrhwe1032','RaquelCion', 'BrewPubExplorer', 'lincolnwrites',
 'giordanobc', 'NomInNY', 'TAsterisk', 'RobHBedford', 'imdjencore',
 'everytract', 'stevelauro', 'M97Cos', 'choppy2984', 'Majikonline',
 'JohnnyBarfly', 'RoyRuger', 'RRWhiskySpirits', 'harisamin', 'lentaminen',
 'Katluck125', 'TotalTrafficNYC', 'SsmBoutique40', 'billfelty', 'BienRealty',
 'Dr_Fiorillo', 'huntingforjoy', 'Home_Zuh', 'Mirjana13nyc', 'PaneraCareers',
 'JoeFleeNY', 'OWWRNY', 'drrichardreish', 'ctbeertours', 'citygrl33',
 'sonic13oom', 'parkslope5thave', 'GAGA_glitz', 'CTDOT_District3',
 'pop_amargaritav']
    
    def get_tweets_id(self, username = "RobHBedford", limit = 20):
        import nest_asyncio
        nest_asyncio.apply()
        import twint
        c = twint.Config()

        c.Username = username
        c.Since = '2020-1-1'
        c.until= '2021-6-1'
        #c.Location = True
        #c.Custom["tweet"] = ["id"]
        #c.Custom["user"] = ["bio"]
        c.Limit = limit
        #c.Store_csv = True
        c.Hide_output = True
        c.Output = "none"
        c.Pandas = True

        twint.run.Search(c)

        Tweets_df = twint.storage.panda.Tweets_df
        return Tweets_df
    
    def get_tweets_location(self,username = 'RobHBedford', limit = 20):
        
        tweets_ids = self.get_tweets_id(username, limit).id
        tweets_ids = pd.to_numeric(tweets_ids)
        tweets_ids = tweets_ids[:limit]
        
        df = search_by_tweet_id(tweets_ids[0] - 1, tweets_ids[0])

        for i in range(1, len(tweets_ids)):
            
            since_id = tweets_ids[i] - 1
            max_id = tweets_ids[i]
            temp = search_by_tweet_id(since_id, max_id)
            df = pd.concat([df, temp])
            
        return df.loc[df.coordinates.notnull(), ['date','content','coordinates','place']]
    