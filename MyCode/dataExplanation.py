# Function to output an explanation of how the user's data is used to generate the recommendations
#   This function has been moved to a separate file for the sake of cleanliness and readability
def show_data_explanation():
    print("HOW THE SYSTEM USES YOUR DATA")
    print("This system uses a combination of recommender systems (Collaborative and Content-based) with a cascade "
          "scheme to generate your recommendations. In order to find the suitability of each Sports Bar for you "
          "your pass reviews and ratings are taken into account, along with any preferences which you may have "
          "expressed. The majority of the data is editable to you and so you can edit and improve the data used "
          "to recommend businesses as you please. More details on this can be found below.")
    print()

    print("YOUR REVIEWS")
    print("The suitability of businesses are measured by similarities and comparisons to businesses which you have "
          "already reviewed. As such, your reviews are essential to the effectiveness of the recommender system. "
          "By navigating through the menu, you have the option to view your current reviews, add new reviews, edit "
          "reviews, and also delete reviews. As a result, if you wish for your reviews to no longer be considered "
          "when generating recommendations, you may delete your existing reviews so that they will not be used")
    print()

    print("YOUR PREFERENCES")
    print("The system provides numerous additional preferences to further refine the recommendations given. Firstly, "
          "whilst there is a default number of recommendations to be displayed on output, you may change this to a "
          "more comfortable/useful value. Additionally, you may choose a minimum number of stars required for any "
          "business to be recommended. If you wish you not have certain businesses recommended, you may add them to "
          "an editable blacklist which will then be removed from the list of generated recommendations. Finally, "
          "before advanced recommendations are considered, you may choose whether you wish for previously reviewed "
          "businesses to be recommender. All of these preferences are editable at any point and the generated "
          "recommendations will update accordingly.")
    print()

    print("ADVANCED PREFERENCES")
    print("In addition to the more general preferences above, there are numerous changeable advanced preferences for "
          "specific requirements. You may choose to add, edit, and delete requirements regarding around the following "
          "business attributes: the presence of outdoor seating, delivery and takeout options, good businesses for "
          "kids, wheelchair accessibility, smoking rules, noise level, and alcohol availability.")
    print()

    print()