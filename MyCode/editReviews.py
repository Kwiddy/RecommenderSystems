import string
import random
import datetime


def edit_reviews(user_id, businesses, reviews, users):
    # Display current reviews
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
            add_new_review(user_id, reviews, businesses)
            anything_else(user_id, businesses, reviews, users)

        elif choice.upper() == "A":
            valid_choice = True
            print("Amend")
            # function to amend existing review
            anything_else(user_id, businesses, reviews, users)

        elif choice.upper() == "D":
            valid_choice = True
            print("delete")
            # function to delete existing review
            anything_else(user_id, businesses, reviews, users)

        elif choice.upper() == "B":
            valid_choice = True
            print()

        elif choice.upper() == "X":
            valid_choice = True
            exit()

        else:
            print("INVALID INPUT")


def add_new_review(user_id, reviews, businesses):
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
            valid_input = True
        elif len(name_search) != 0:
            review_business_id = name_search['business_id'].iloc[0]
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


    # Update newDFReview.csv: take user,bus,rev id, take stars, text, and date, add (set other vals to initially zero?)
    print(reviews.tail(3))

    # Update newDFBusiness.csv: update review count, do I need to update stars?
    print("hi")

    # Update newDFUser.csv: update review count, update average stars,
    print("hi")

    # Update newDFCheckin.csv update checkin
    print("hi")

    print("Review created with id: ", review_id)
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