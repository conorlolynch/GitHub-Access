import json
import requests
from github import Github
from flask import Flask, request, render_template, redirect, url_for,jsonify
import time
from datetime import datetime, date, time, timedelta


# So potential things that can be built:

# 2) Show all the langauges this user has used
# 3) Show the times the user commits at




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

    return render_template("dashboard.html", content=user_dict)


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
    user_dict['commit'] = {0:[], 1:[], 2:[],3:[],4:[],5:[],6:[]}

    # https://api.github.com/repos/conorlolynch/A-Star-Pathfinding/stats/punch_card

    repos = user.get_repos()
    hours_and_commits = repos[0].get_stats_punch_card().raw_data


    # Now convert this into the desired format [hour, num_commits]
    form = []
    for index in range(0,len(hours_and_commits)):
        form.append([index % 24, hours_and_commits[index][2]])


    # For each repository in this users account
    for repo in repos[1:]:
        if repo.owner.login == user_dict['login']:
            data = repo.get_stats_punch_card().raw_data

            # For every index in the array
            for index in range(0,len(form)):
                form[index][1] = form[index][1] + data[index][2]


    # Now store these separetely based on day
    user_dict['commit'][0] = form[0:24]         # Commit by hour on Sunday
    user_dict['commit'][1] = form[24:48]        # Commit by hour on Monday
    user_dict['commit'][2] = form[48:72]        # Commit by hour on Tuesday
    user_dict['commit'][3] = form[72:96]        # Commit by hour on Wednesday
    user_dict['commit'][4] = form[96:120]       # Commit by hour on Thursday
    user_dict['commit'][5] = form[120:144]      # Commit by hour on Friday
    user_dict['commit'][6] = form[144:]         # Commit by hour on Saturday


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
