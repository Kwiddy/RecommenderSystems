import pandas as pd
import json


def load_dataset(path):
    with open(path, encoding="utf-8") as f:
        for count, line in enumerate(f):
            data = json.loads(line.strip())
            if count == 0:
                dataset = {}
                keys = data.keys()
                for k in keys:
                    dataset[k] = []
            for k in keys:
                dataset[k].append(data[k])
    return pd.DataFrame(dataset)


def refine_business(category, city):
    # refine by category
    rdf = dfBusiness[dfBusiness["categories"].str.contains(category)]
    rdf = rdf[rdf["city"].str.contains(city)]
    rdf.set_index("business_id")
    return rdf


def refine_review(timeframe):
    tempdf = dfReview[dfReview['date'].str.contains(timeframe)]
    rdf = tempdf[tempdf["business_id"].isin(newDFBusiness["business_id"])]
    return rdf


# Load the datasets and remove nan valued rows
dfBusiness = load_dataset("Datasets/full/yelp_academic_dataset_business.json")
dfReview = load_dataset("Datasets/full/yelp_academic_dataset_review.json")
dfBusiness.dropna(subset=["categories"], inplace=True)
print(dfReview.columns)

# Create new dataset with specific category
# Number of items for several categories (all cities):
#       Restaurants 63944
#       Bars 16855
#       Pet Services 3084
#       Italian 5012
#       Sports Bar 2376
domain = "Sports Bar"
location = "Toronto"
startDate = "2019"
newDFBusiness = refine_business(domain, location)
newDFReview = refine_review(startDate)
print(newDFReview)

newDFBusiness.to_csv("newDFBusiness.csv")
newDFReview.to_csv("newDFReview.csv")
