# import
import pandas as pd
import json


# Load the datasets into a pandas dataframe
def load_dataset(path):
    with open(path, encoding="utf-8") as file:
        for count, line in enumerate(file):
            data = json.loads(line.strip())
            if count == 0:
                dataset = {}
                keys = data.keys()
                for k in keys:
                    dataset[k] = []
            for k in keys:
                dataset[k].append(data[k])
    new_df = pd.DataFrame(dataset)
    return new_df


# Refine the business dataframe by city and category
def refine_business(category, city):
    rdf = dfBusiness[dfBusiness["categories"].str.contains(category)]
    rdf = rdf[rdf["city"].str.contains(city)]
    rdf.set_index("business_id")
    return rdf


# Refine the reviews dataframe by timeframe and if they are relevant to the refined businesses
def refine_review(timeframe):
    tempdf = dfReview[dfReview['date'].str.contains(timeframe)]
    rdf = tempdf[tempdf["business_id"].isin(newDFBusiness2["business_id"])]
    return rdf


# Refine the businesses by the provided COVID data
def refine_covid():
    rdf = dfCovid[dfCovid["business_id"].isin(newDFBusiness["business_id"])]

    # Use line below if you wish to restrict the COVID data further, changed since reading an FAQ post
    # rdf = rdf[rdf['delivery or takeout'].str.contains("TRUE")]
    return rdf


# Refine the businesses dataframe by the refined COVID dataframe
def refine_by_covid():
    # After reading the FAQ, it is requested that the COVID data provides additional information but does not reduce
    #   the main data, if it were to be reduced, then the line below should be used instead

    # rdf = newDFBusiness[newDFBusiness["business_id"].isin(newDFCovid["business_id"])]

    rdf = newDFBusiness
    return rdf


# Refine the users dataframe
def refine_users():
    rdf = dfUsers[dfUsers["user_id"].isin(newDFReview["user_id"])]

    # Add a column for preferred number of recommendations to display (default 8)
    rdf = rdf.assign(display_num=8)

    # Add a column for blacklisted businesses
    rdf["blacklist"] = ""

    # Add a column for minimum number of stars
    rdf["min_stars"] = 1

    # Add a column for preference of recommending already reviewed businesses (Default No (do not recommend seen items))
    rdf["recommend_seen"] = "N"

    # Add a column, later to contain a string-dictionary, where further preferences are contained such as requiring
    #   wheelchair access
    rdf["advanced_preferences"] = ""

    # Add a column for if the user wishes only for businesses which are not "Temporarily closed until" (Default: No)
    rdf["covid_temp_closed"] = "N"

    # Add a column for user requiring businesses during COVID to offer either delivery or takeout (Default: No)
    rdf["covid_d_t"] = "N"

    return rdf


# Load the datasets and remove nan valued rows
dfBusiness = load_dataset("Datasets/full/yelp_academic_dataset_business.json")
dfReview = load_dataset("Datasets/full/yelp_academic_dataset_review.json")
dfCovid = load_dataset("Datasets/covid/yelp_academic_dataset_covid_features.json")
dfUsers = load_dataset("Datasets/full/yelp_academic_dataset_user.json")
dfBusiness.dropna(subset=["categories"], inplace=True)

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

# Refine the original datasets to my chosen domains
newDFBusiness = refine_business(domain, location)
newDFCovid = refine_covid()
newDFBusiness2 = refine_by_covid()
print("refined businesses (+ by covid)")
newDFReview = refine_review(startDate)
print("refined reviews")
newDFUser = refine_users()
print("refined users")

# Save the new datasets to new files which can then be accessed by the recommender system
newDFBusiness2.to_csv("newDFBusiness.csv", index=0)
newDFCovid.to_csv("newDFCovid.csv", index=0)
newDFReview.to_csv("newDFReview.csv", index=0)
newDFUser.to_csv("newDFUser.csv", index=0)
