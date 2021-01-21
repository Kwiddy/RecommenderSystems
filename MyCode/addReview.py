def add_new_review(user_id, businesses, reviews, users):
    # Display current reviews
    display_reviews(user_id, reviews)

    # Give the option to Add, Amend, Delete

    # Add a new review

    # Delete an existing review

    # Amend an existing review


def display_reviews(user, reviews):
    user_reviews = reviews[reviews["user_id"] == user]
    print(user_reviews)
    print()