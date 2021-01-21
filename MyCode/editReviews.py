import string
import random
import datetime
import pandas as pd
import numpy as np


def edit_reviews(user_id, businesses, reviews, users):
    # Display current reviews
    reviews = pd.read_csv("newDFReview.csv")
    display_reviews(user_id, reviews)

    # Give the option to Add, Amend, Delete
    print("[N] - Add a new review")
    print("[A] - Amend an existing review")
    print("[D] - Delete an existing review")
    print("[B] - Back")
    print("[X] - Exit")
    valid_choice = False
    while not valid_choice:
        choice = input("Please enter from the selection above: ")

        if choice.upper() == "N":
            valid_choice = True
            add_new_review(user_id, reviews, businesses, users)
            anything_else(user_id, businesses, reviews, users)

        elif choice.upper() == "A":
            valid_choice = True
            print("Amend")
            # function to amend existing review
            anything_else(user_id, businesses, reviews, users)

        elif choice.upper() == "D":
            valid_choice = True
            delete_review(user_id, reviews, businesses, users)
            anything_else(user_id, businesses, reviews, users)

        elif choice.upper() == "B":
            valid_choice = True
            print()

        elif choice.upper() == "X":
            valid_choice = True
            exit()

        else:
            print("INVALID INPUT")


def add_new_review(user_id, reviews, businesses, users):
    # Dummy function to generate a new review_id
    # Due to only being able to submit a subset of the yelp data and this recommender only focusing on said subset
    #   I simply create a new random review ID that hasn't been seen before from the existing IDs in the subset
    review_id = gen_new_review_id(reviews)

    valid_input = False
    while not valid_input:
        print("Please enter the text of your review: ")
        review_text = input()
        if len(review_text) > 0:
            valid_input = True
            print()
        else:
            print("PLEASE ENTER SOME REVIEW TEXT")

    valid_input = False
    while not valid_input:
        print("Please enter the id or name of the business:")
        review_business_input = input()
        id_search = businesses[businesses["business_id"] == review_business_input]
        name_search = businesses[businesses["name"] == review_business_input]
        if len(id_search) != 0:
            review_business_id = id_search['business_id'].iloc[0]
            print("Chosen Business: ", str(id_search['name'].iloc[0]))
            valid_input = True
        elif len(name_search) != 0:
            review_business_id = name_search['business_id'].iloc[0]
            print("Chosen Business: ", str(name_search['name'].iloc[0]))
            valid_input = True
        else:
            print("INVALID NAME OR BUSINESS")
    print()

    valid_input = False
    while not valid_input:
        print("Please enter the number of stars you wish to rate this business [1-5]: ")
        review_stars = input()
        try:
            if int(review_stars) in range(1, 6):
                valid_input = True
                print()
                review_stars = str(int(review_stars)) + ".0"
        except ValueError as e:
            print(e)
            valid_input = False

    # Generate date
    review_time = str(datetime.datetime.now())[:-7]

    # update reviews dataframe
    new_review = {'review_id': review_id, 'user_id': user_id, 'business_id': review_business_id, 'stars': review_stars,
                  'useful': 0, 'funny': 0, 'cool': 0, 'text': review_text, 'date': review_time}
    reviews = reviews.append(new_review, ignore_index=True)
    reviews.to_csv("newDFReview.csv", index=0)

    # update review count, do I need to update stars?
    businesses.loc[businesses["business_id"] == review_business_input, "review_count"] += 1
    businesses.to_csv("newDFBusiness.csv", index=0)

    # Edit user's number of reviews and average stars
    users['average_stars'] = np.where(users['user_id'] == user_id, round(((users['average_stars']*users["review_count"])+int(review_stars[:-2]))/(users["review_count"]+1), 2), users['average_stars'])
    users.loc[users["user_id"] == user_id, "review_count"] += 1
    users.to_csv("newDFUser.csv", index=0)

    print("Review created with id: ", review_id)
    print()


def delete_review(user_id, reviews, businesses, users):
    print()
    print("[S] - Select one review to delete")
    print("[A] - Delete all of my reviews")
    valid_choice = False
    while not valid_choice:
        choice = input("Please select from the options above: ")
        if choice.upper() == "S":
            valid_choice = True
            display_reviews(user_id, reviews)
            valid_choice_2 = False
            while not valid_choice_2:
                chosen_id = input("Please enter ID of review to be deleted: ")
                id_search = reviews[reviews["review_id"] == chosen_id]
                business_id = id_search['business_id'].iloc[0]
                if len(id_search) == 0:
                    print("INVALID ID")
                else:
                    valid_choice_2 = True

                    temp = reviews[reviews.review_id == chosen_id]
                    users['average_stars'] = np.where(users['user_id'] == user_id, round(
                        ((users['average_stars'] * users["review_count"]) - int(temp["stars"])) / (
                                    users["review_count"] - 1), 2), users['average_stars'])
                    temp = []

                    reviews = reviews[reviews.review_id != chosen_id]
                    businesses.loc[businesses["business_id"] == business_id, "review_count"] -= 1
                    businesses.to_csv("newDFBusiness.csv", index=0)
                    users.loc[users["user_id"] == user_id, "review_count"] -= 1
                    users.to_csv("newDFUser.csv", index=0)
        elif choice.upper() == "A":
            sure_valid = False
            valid_choice = True
            while not sure_valid:
                yn = input("Are you sure? [Y/N]: ")
                if yn.upper() == "Y":
                    sure_valid = True
                    temp = reviews[reviews.user_id == user_id]
                    for index, row in temp.iterrows():

                        users['average_stars'] = np.where(users['user_id'] == user_id, round(
                            ((users['average_stars'] * users["review_count"]) - int(row["stars"])) / (
                                    users["review_count"] - 1), 2), users['average_stars'])

                        businesses.loc[businesses["business_id"] == row['business_id'], "review_count"] -= 1
                        businesses.to_csv("newDFBusiness.csv", index=0)
                        users.loc[users["user_id"] == user_id, "review_count"] -= 1
                        users.to_csv("newDFUser.csv", index=0)
                    reviews = reviews[reviews.user_id != user_id]
                    temp = []
                elif yn.upper() == "N":
                    sure_valid = True
                else:
                    print("INVALID INPUT")
        else:
            print("INVALID INPUT")
    reviews.to_csv("newDFReview.csv", index=0)
    print()

    ## To do: average stars

def gen_new_review_id(reviews):
    alphabet = list(string.ascii_letters) + ["_", "-"]
    for i in range(0,10):
        alphabet.append(str(i))

    # Generate a random 22 long id which is not already in the reviews
    valid_selection = False
    while not valid_selection:
        generated_id = ''.join(random.sample(alphabet, 22))
        id_search = reviews[reviews["review_id"] == generated_id]

        if len(id_search) == 0:
            valid_selection = True

    return generated_id


def anything_else(user_id, businesses, reviews, users):
    valid_choice = False
    while not valid_choice:
        yn = input("Continue editing your reviews? [Y/N]: ")
        if yn.upper() == "Y":
            valid_choice = True
            edit_reviews(user_id, businesses, reviews, users)
        elif yn.upper() != "N":
            print("INVALID INPUT")
        else:
            valid_choice = True


def display_reviews(user, reviews):
    user_reviews = reviews[reviews["user_id"] == user]
    print(user_reviews)
    print()