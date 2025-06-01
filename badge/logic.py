
def assign_badge(user):
    count = len(user.recipes)
    if count >= 25:
        user.badge = "Master Chef"
    elif count >= 10:
        user.badge = "Home Cook"
    elif count >= 5:
        user.badge = "Novice Chef"
    else:
        user.badge = "Newbie"
