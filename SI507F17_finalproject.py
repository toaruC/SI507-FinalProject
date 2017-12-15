# Main Execution GOES HERE
from SI507F17_finalproject_oauth import *
from SI507F17_finalproject_database import *

from flask import Flask, request, render_template

DEBUG = True
app = Flask(__name__)

### CLASS DEFINITION
class InsPost:
    def __init__(self, post):
        self.id = post['id']
        self.owner = post['user']['id']
        self.img_url = post['images']['low_resolution']['url']
        self.num_of_likes = post['likes']['count']
        self.post_url = post['link']
        if post['tags']:
            self.num_of_tags = len(post['tags'])
            self.tags = post['tags']
        else:
            self.num_of_tags = 0
            self.tags = []

    def __repr__(self):
        return "post_url:{0}, owner:{1}, likes:{2}".format(self.post_url, self.owner, str(self.num_of_likes))

    def __contains__(self, tag):
        if tag in self.tags:
            return True


class InsUser:
    def __init__(self, user):
        self.name = user['username']
        self.id = user['id']
        self.profile_url = user['profile_picture']

    def __repr__(self):
        return "name: {0}, uid: {1}, profile: {2}".format(self.name, self.id, self.profile_url)


### Additional Func
def get_posts(data):
    post_list = []
    for i in data:
        post_list.append(InsPost(i))
    return post_list


### Flask
@app.route('/')
def show_user_photos():
    query_result_like = execute_and_print("SELECT name, img_url, num_of_likes from Posts INNER JOIN Users ON Posts.owner = Users.id WHERE num_of_likes>15", 10)
    like_list = []
    for i in query_result_like:
        like_list.append({"username":i[0], "img_url":i[1], "num_of_likes":i[2]})

    query_result_tag = execute_and_print("SELECT name, img_url,tags from Posts INNER JOIN Users ON Posts.owner = Users.id WHERE num_of_tags>1", 5)
    tag_list = []
    for i in query_result_tag:
        tag_list.append({"username":i[0], "img_url":i[1], "tags":i[2]})

    return render_template('index.html', like_list = like_list, tag_list = tag_list)


if __name__ == "__main__":

    ### GET DATA from Instagram API
    # to get 20 pieces of recent media data from 5 users who are in my sandbox list
    # and then save in 5 dict variables for database use
    if DEBUG:
        print("Get Data...")
    ins_media_url = 'https://api.instagram.com/v1/users/self/media/recent/'
    params = {'count':'20'}
    data_toaruc = get_data_from_api("toaruc", ins_media_url, params)['data']
    # print(data_toaruc)
    # print(type(data_toaruc))
    data_ctloku = get_data_from_api("ctloku", ins_media_url, params)['data']
    data_xly =  get_data_from_api("x.linying", ins_media_url, params)['data']
    data_alejwang = get_data_from_api("alejwang", ins_media_url, params)['data']
    data_hytest = get_data_from_api("hy501test", ins_media_url, params)['data']


    ###Convert cached data into class instances
    ## Create a list of Class InsUser instances
    if DEBUG:
        print("Start converting Class InsUser instances...")
    ins_user_list = []
    ins_user_list.append(InsUser(data_toaruc[0]['user']))
    ins_user_list.append(InsUser(data_ctloku[0]['user']))
    ins_user_list.append(InsUser(data_xly[0]['user']))
    ins_user_list.append(InsUser(data_alejwang[0]['user']))
    ins_user_list.append(InsUser(data_hytest[0]['user']))
    # print(ins_user_list)

    ## Create a list of Class InsPost instances
    if DEBUG:
        print("Start converting Class InsPost instances...")
    toaruc_posts = get_posts(data_toaruc)
    ctloku_posts = get_posts(data_ctloku)
    xly_posts = get_posts(data_xly)
    alejwang_posts = get_posts(data_alejwang)
    hytest_posts = get_posts(data_hytest)


    ### Insert data to Database
    ## Create tables
    if DEBUG:
        print("Start creating database tables...")
    create_tables()
    ## Insert lists into tables
    if DEBUG:
        print("Start inserting InsUser instances into database table: Users...")
    insert_users(ins_user_list)
    if DEBUG:
        print("Start inserting InsPost instances into database table: Posts...")
    insert_posts(toaruc_posts)
    insert_posts(ctloku_posts)
    insert_posts(xly_posts)
    insert_posts(alejwang_posts)
    insert_posts(hytest_posts)

    ### Test database query
    # select posts with more than 10 likes and its owner's username
    # result = execute_and_print("SELECT name, post_url from Posts INNER JOIN Users ON Posts.owner = Users.id WHERE num_of_likes>10", 25)
    # print(result[0][0], "and", result[0][1])

    ### Run Flask App on local server
    # auto reloads (mostly) new code and shows exception traceback in the browser
    app.run(use_reloader = False, debug = False)
