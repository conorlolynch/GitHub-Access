import json
import requests
from github import Github
from flask import Flask, request, render_template, redirect, url_for,jsonify
import time
from datetime import datetime, date, time, timedelta


# So potential things that can be built:

# 1) Display the users profile pic as well as some basic background information (followers and following)
# 2) Show all the langauges this user has used
# 3) Show the times the user commits at



# Look into creating a random account with to get a token to surpass the rate limit





app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods=['POST'])
def my_form_post():
    user_or_token = request.form['b1']
    print(user_or_token)
    return redirect(url_for('index', inputvalue=user_or_token)) # then you can pass email or pass


@app.route('/<inputvalue>')
def index(inputvalue):
    user_dict = searchForAccount(inputvalue)
    temp_arr = [[],[],[],[],[],[],[]]

    # Quickly zoom through the list and change certain indexes
    for i in range(0,7):
        for key, value in sorted(user_dict['commit'][i].items()):
            print("Key: ",key," Value: ",value)
            temp_arr[i].append([key, value])


        # Sort the list before
        print("\n",temp_arr[i],"\n")

    return render_template("dashboard.html", content=user_dict, vals=temp_arr)


def searchForAccount(token):
    # Take input from the user
    user_dict = dict()

    #try:
    g = Github(login_or_token=token)
    user = g.get_user()
    login = user.login
    #print(user)

    # User information
    user_dict['login'] = user.login
    user_dict['id'] = user.id
    user_dict['location'] = user.location
    user_dict['atr'] = user.avatar_url
    user_dict['profile_url'] = user.html_url
    user_dict['followers'] = user.followers
    user_dict['following'] = user.following
    user_dict['public_repos'] = user.public_repos
    user_dict['name'] = user.name
    user_dict['bio'] = user.bio
    user_dict['email'] = user.email
    user_dict['repos'] = dict()     # The same thing as repo
    user_dict['commit'] = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}}    # 6 days of the week

    # User repository information
    for repo in user.get_repos():
        #user_dict['repos'][repo.name] = dict()
        repo_total = 0

        # For each commit made
        for com in repo.get_commits():
            if (user_dict['id'] == com.author.id):
                date_time = com.commit.author.date

                hour = date_time.hour
                day = date_time.weekday()

                # If its in then increment it
                if (hour in user_dict['commit'][day]):
                    user_dict['commit'][day][hour] = user_dict['commit'][day][hour] + 1
                else:
                    user_dict['commit'][day][hour] = 1


    return user_dict

    # except Exception as e:
    #     print(e)
    #     return user_dict


# def searchForAccount(user_or_token):
#     try:
#         # Creating GitHub client
#         g = Github(user_or_token)
#         for repo in g.get_user().get_repos():
#             print("Name: ",repo.name)
#             print("Description: ",repo.description)
#
#             # Print all repository content
#             print("Contents:")
#             for content in repo.get_contents(""):
#                 print(content)
#
#     except Exception as e:
#         # Token didnt work so check to see if its a username instead
#         print("Attempting Username")
#         base_url = r"https://api.github.com/users"
#
#         api_url = F"{base_url}/{user_or_token}"
#         res = requests.get(api_url)
#         info = json.loads(res.content.decode('utf-8'))
#         print(info)


if __name__ == "__main__":
    app.run()
