import string
import random
import datetime
import pandas as pd
import numpy as np


def edit_reviews(user_id, businesses, reviews, users):
    # Display current reviews
    reviews = pd.read_csv("newDFReview.csv")

    # Give the option to Add, Amend, Delete
    print("[N] - Add a new review")
    print("[V] - View and Rate Reviews")
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
            amend_reviews(user_id, reviews)
            anything_else(user_id, businesses, reviews, users)

        elif choice.upper() == "D":
            valid_choice = True
            delete_review(user_id, reviews, businesses, users)
            anything_else(user_id, businesses, reviews, users)

        elif choice.upper() == "V":
            valid_choice = True
            display_reviews(user_id)

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
        review_business_input = input("Please enter the id or name of the business (or [C] to cancel): ")
        if review_business_input.upper() != "C":
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
        else:
            valid_input = True
    print()

    if review_business_input.upper() != "C":

        # Detect if the user has already reviewed the chosen business and if so, give them the option to
        #   edit their review instead
        # review_business_id
        user_reviews = reviews[reviews["user_id"] == user_id]
        prev_reviewed_business = False
        for index, row in user_reviews.iterrows():
            if review_business_id == row["business_id"]:
                prev_reviewed_business = True
                break
        if prev_reviewed_business:
            print("You have already reviewed this business, if you wish, you may instead edit this review in the edit "
                  "section")
            print()
        else:

            # Take the text of the review
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
        choice = input("Please select from the options above (or [C] to cancel): ")
        if choice.upper() != "C":
            if choice.upper() == "S":
                valid_choice = True
                display_reviews(user_id)
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
        else:
            valid_choice = True
    reviews.to_csv("newDFReview.csv", index=0)
    print()


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


def amend_reviews(user_id, reviews):
    print("--- Your existing reviews ---")
    user_reviews = reviews[reviews["user_id"] == user_id]
    if len(user_reviews) != 0:
        print(user_reviews)
    else:
        print("...You do not currently have any existing reviews")
    print()
    valid_review = False
    while not valid_review:
        choice = input("Enter the ID of the review you wish to edit (or [C] to cancel): ")
        if choice.upper() != "C":
            review_search = reviews[reviews["review_id"] == choice]
            if len(review_search) != 0:
                valid_review = True
            else:
                print("INVALID INPUT")
        else:
            valid_review = True

    if choice.upper() != "C":
        review_id = choice

        # Editable:
        #   Stars
        #   Text
        print("[S] - Stars given")
        print("[T] - Review's text")
        valid_choice = False
        while not valid_choice:
            choice = input("Please select from the options above: ")
            if choice.upper() == "S":
                valid_choice = True
                valid_input = False
                while not valid_input:
                    print("Please enter the number of stars you wish to rate this business [1-5]: ")
                    review_stars = input()
                    try:
                        if int(review_stars) in range(1, 6):
                            valid_input = True
                            review_stars = str(int(review_stars)) + ".0"
                    except ValueError as e:
                        print(e)
                        valid_input = False
                reviews.loc[reviews["review_id"] == review_id, "stars"] = str(review_stars)
                print("Number of stars given has been changed to: ", review_stars)
                reviews.to_csv("newDFReview.csv", index=0)

            elif choice.upper() == "T":
                valid_choice = True
                print("Enter your new review text below:")
                review_text = input()
                reviews.loc[reviews["review_id"] == review_id, "text"] = review_text
                reviews.to_csv("newDFReview.csv", index=0)
                print("Review text has ben changed")
            else:
                print("INVALID INPUT")

            print()
            print("--- Your existing reviews ---")
            user_reviews = reviews[reviews["user_id"] == user_id]
            print(user_reviews)


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


def display_reviews(user):
    reviews = pd.read_csv("newDFReview.csv")
    businesses = pd.read_csv("newDFBusiness.csv")
    print()
    print("[M] - Display all of my reviews")
    print("[U] - Search for reviews by user")
    print("[B] - Search for reviews by business")
    print("[X] - Return")
    valid_choice = False
    while not valid_choice:
        choice = input("Please choose from the selection above: ")

        if choice.upper() == "M":
            valid_choice = True
            user_reviews = reviews[reviews["user_id"] == user]
            user_reviews["business name"] = user_reviews.apply\
                (lambda row: businesses[businesses["business_id"] == row.business_id]["name"].iloc[0], axis=1)
            print(user_reviews[["review_id", "user_id", "business name", "stars", "useful",
                                "funny", "cool", "text", "date"]])
            print()
            display_reviews(user)

        elif choice.upper() == "U":
            valid_choice = True
            valid_user = False
            while not valid_user:
                print()
                chosen_user = input("Please enter a user ID (or [X] to exit): ")
                if chosen_user.upper() != "X":
                    user_reviews = reviews[reviews["user_id"] == chosen_user]
                    if len(user_reviews) == 0:
                        print("Invalid User ID / This user has left no valid reviews (valid reviews must be in valid "
                              "timeframe)")
                    else:
                        valid_user = True
                        # user_reviews = user_reviews.set_index("review_id")
                        user_reviews["business name"] = user_reviews.apply(
                            lambda row: businesses[businesses["business_id"] == row.business_id]["name"].iloc[0],
                            axis=1)
                        print(user_reviews[["review_id", "user_id", "business name", "stars", "useful",
                                            "funny", "cool", "text", "date"]])
                        temp = []
                        for index, row in user_reviews.iterrows():
                            temp.append(row["review_id"])
                        rate_review(temp)
                else:
                    valid_user = True
            display_reviews(user)

        elif choice.upper() == "B":
            valid_choice = True
            valid_business = False
            while not valid_business:
                print()
                chosen_business = input("Please enter a business ID / name (or [X] to exit): ")
                if chosen_business.upper() != "X":
                    # Try business_id first
                    business_reviews = reviews[reviews["business_id"] == chosen_business]
                    if len(business_reviews) != 0:
                        valid_business = True
                        # business_reviews = business_reviews.set_index("review_id")
                        business_reviews["business name"] = business_reviews.apply(
                            lambda row: businesses[businesses["business_id"] == row.business_id]["name"].iloc[0],
                            axis=1)
                        print(business_reviews[["review_id", "user_id", "business name", "stars", "useful",
                                            "funny", "cool", "text", "date"]])
                        temp = []
                        for index, row in business_reviews.iterrows():
                            temp.append(row["review_id"])
                        rate_review(temp)
                    else:
                        # Try searching by business name second
                        possible_businesses = businesses[businesses["name"] == chosen_business]
                        if len(possible_businesses) != 0:

                            valid = False
                            while not valid:
                                print()
                                print(possible_businesses)
                                chosen_business = input("Please enter one of the Business IDs above (or [X] to exit): ")
                                if chosen_business.upper() != "X":
                                    business_reviews = reviews[reviews["business_id"] == chosen_business]
                                    if len(business_reviews) == 0:
                                        print(
                                            "Invalid Business ID / This user has left no valid reviews (valid "
                                            "reviews must be in valid timeframe)")
                                    else:
                                        valid = True
                                        # user_reviews = user_reviews.set_index("review_id")
                                        business_reviews["business name"] = business_reviews.apply(
                                            lambda row:
                                            businesses[businesses["business_id"] == row.business_id]["name"].iloc[0],
                                            axis=1)
                                        print(business_reviews[
                                                  ["review_id", "user_id", "business name", "stars",
                                                   "useful",
                                                   "funny", "cool", "text", "date"]])
                                        temp = []
                                        for index, row in business_reviews.iterrows():
                                            temp.append(row["review_id"])
                                        rate_review(temp)
                                else:
                                    valid = True

                        else:
                            print("Invalid business ID / This business has no valid reviews (must be in valid timeframe)")
                else:
                    valid_business = True
            display_reviews(user)

        elif choice.upper() != "X":
            print("INVALID INPUT")

        else:
            valid_choice = True
            print()


# Give the user the option to rate a particular review
def rate_review(reviews):
    reviews_df = pd.read_csv("newDFReview.csv")
    users_df = pd.read_csv("newDFUser.csv")
    print()
    valid_choice = False
    giving_rating = False
    while not valid_choice:
        yn = input("Would you like to rate any reviews? [Y/N]: ")
        if yn.upper() == "Y":
            valid_choice = True
            giving_rating = True
        elif yn.upper() != "N":
            print("INVALID INPUT")
        else:
            valid_choice = True

    # Give a menu of rating choices to choose from and update review's and user's dataframes accordingly
    if giving_rating:
        valid_review = False
        while not valid_review:
            print()
            chosen_review = input("Please enter a review_id ID (or [X] to exit): ")
            if chosen_review.upper() != "X":
                if chosen_review not in reviews:
                    print("INVALID ID")
                else:
                    valid_review = True
                    print()
                    print("[U] - Useful")
                    print("[F] - Funny")
                    print("[C] - Cool")
                    print("[B] - Return")
                    print("[X] - Exit")
                    valid_choice = False
                    returning = False
                    while not valid_choice:
                        choice = input("Please enter from the selection above: ")

                        if choice.upper() == "U":
                            valid_choice = True
                            chosen_stat = "useful"

                        elif choice.upper() == "F":
                            valid_choice = True
                            chosen_stat = "funny"

                        elif choice.upper() == "C":
                            valid_choice = True
                            chosen_stat = "cool"

                        elif choice.upper() == "B":
                            valid_choice = True
                            returning = True
                            print()

                        elif choice.upper() == "X":
                            valid_choice = True
                            exit()

                        else:
                            print("INVALID INPUT")

                    if not returning:
                        # Update the review
                        reviews_df.loc[reviews_df["review_id"] == chosen_review, chosen_stat] += 1
                        reviews_df.to_csv("newDFReview.csv", index=0)

                        # Update the relevant user
                        id_search = reviews_df.loc[reviews_df["review_id"] == chosen_review]
                        complimented_user = id_search['user_id'].iloc[0]
                        users_df.loc[users_df["user_id"] == complimented_user, chosen_stat] += 1
                        users_df.to_csv("newDFUser.csv", index=0)

                        print("The review has been rated...")

            else:
                valid_review = True
