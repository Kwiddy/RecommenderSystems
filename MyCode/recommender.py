# 2 personalised recommender systems
# cli
# 1 must be collaborative: collaborative content-based, collaborative demographic, collaborative knowledge-based
# choose the hybrid scheme: weighted, mixed, switching, feature combination, feature augmentation, cascade
#
# collaborative should be item-item?
# look at paper in wk 4 movie recommender
#
# Measure the similarity between users to find neighbours. e.g. pearson correlation
# use regression / classification -- I would need to do regression? because ordering matters i.e. its a continuous scale

import pandas as pd
import numpy as np
import math

businesses = pd.read_csv("newDFBusiness.csv")
reviews = pd.read_csv("newDFReview.csv")
print(reviews)

def calc_pearson():
    # Calculate the pearson correlation, use pandas.DataFrame.corr or pandas.Series.corr (probably series > df)


# Eventually this should be changeable, this is just for testing purposes
i_user_id = "454575"


