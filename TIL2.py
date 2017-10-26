import praw, random


# a function that takes the Reddit post title and returns a presentable string
def clean_title(str):
    arr = str.split(' ')
    if arr[0].upper() in ['TIL', 'TIL:', 'TIL,', 'TIL;', 'TIL-', 'TIL--']:
        arr.pop(0)
    if arr[0].lower() == 'i' and arr[1].lower() == 'learned':
        arr = arr[2:]
    if arr[0] in ['-', ':']:
        arr.pop(0)
    if arr[0].lower() in ['that', 'that,']:
        arr.pop(0)
    arr[0] = arr[0].capitalize()
    if arr[0][0] in ['"', "'"]:
        arr[0] = arr[0][0] + arr[0][1:].capitalize();
    if arr[-1][-1] == '.':
        arr[-1] = arr[-1][:-1]
    return ' '.join(arr)


# a function that returns a list of the the first posts in the TIL subreddit
def list_posts(num_posts=1000):

    reddit = praw.Reddit(client_id='enter_client_id',
                     client_secret='enter_client_secret',
                     user_agent='enter_user_agent')

    return list(reddit.subreddit('todayilearned').hot(limit=num_posts))


# create the list of posts
ls_posts = list_posts()


# a function that checks whether a post is 'good': has a number of
# comments above a certain threshhold and satisfies
# rule VI of the TIL subreddit. Titles which begin with
# 'TIL of...' are usually not very comprehensible when removing the 'TIL'
# part
def isGood(post, min_comments=10):

    if clean_title(post.title).split(' ')[0].lower() in ['of', 'about']:
        return False

    if len(post.comments.list()) < min_comments:
        return False

    return True


# a function that chooses a random post which is 'good'
def find_post(list_posts=ls_posts, min_comments=10):

    lenlis = len(list_posts)

    i = random.randint(0,lenlis-1)
    post = list_posts[i]

    while not isGood(post):

        i = random.randint(0,lenlis-1)
        post = list_posts[i]

    return post

print(clean_title(find_post().title))
