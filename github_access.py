import json
import requests
from github import Github
from flask import Flask, request, render_template, redirect, url_for, jsonify, flash
import time
from datetime import datetime, date, time, timedelta



app = Flask(__name__)

user = None
user_dict = None

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=['POST'])
def my_form_post():
    user_or_token = request.form['b1']
    error = None

    try:
        g = Github(login_or_token=user_or_token)
        user = g.get_user()
        login = user.login

        return redirect(url_for('index',inputvalue=user_or_token))

    except:
        error = "Invalid Token"

    return render_template('index.html', error=error)



@app.route('/<inputvalue>')
def index(inputvalue):
    user_dict = searchForAccount(inputvalue)
    return render_template("dashboard.html", content=user_dict)



def getCommits(repos, user_dict):
    try:
        # Make sure the user actually has repositories
        if repos != None:
            hours_and_commits = repos[0].get_stats_punch_card().raw_data


            # Now convert this into the desired format [hour, num_commits]
            form = []
            for index in range(0,len(hours_and_commits)):
                form.append([index % 24, hours_and_commits[index][2]])


            # Make sure they have more than one repository
            if (repos.totalCount > 1):

                # For each repository in this users account
                for repo in repos[1:]:

                    # Make sure the repo isnt private
                    if (not repo.private):
                        if repo.owner.login == user_dict['login']:
                            try:
                                data = repo.get_stats_punch_card().raw_data

                                # For every index in the array
                                for index in range(0,len(form)):
                                    form[index][1] = form[index][1] + data[index][2]
                            except Exception as e:
                                pass



            # Now store these separetely based on day
            user_dict['commit'][0] = form[0:24]         # Commit by hour on Sunday
            user_dict['commit'][1] = form[24:48]        # Commit by hour on Monday
            user_dict['commit'][2] = form[48:72]        # Commit by hour on Tuesday
            user_dict['commit'][3] = form[72:96]        # Commit by hour on Wednesday
            user_dict['commit'][4] = form[96:120]       # Commit by hour on Thursday
            user_dict['commit'][5] = form[120:144]      # Commit by hour on Friday
            user_dict['commit'][6] = form[144:]         # Commit by hour on Saturday

        else:
            template = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], [11, 0],
                       [12, 0], [13, 0], [14, 0], [15, 0], [16, 0], [17, 0], [18, 0], [19, 0], [20, 0], [21, 0], [22, 0], [23, 0]]

            user_dict['commit'][0] = template
            user_dict['commit'][1] = template
            user_dict['commit'][2] = template
            user_dict['commit'][3] = template
            user_dict['commit'][4] = template
            user_dict['commit'][5] = template
            user_dict['commit'][6] = template

    except Exception as e:
        print("Could not read commits: ",e)


def getLanguages(repositories, user_dict):
    try:
        temp_dict = {}

        # Make sure the user has repositories
        if (repositories != None):

            # For each repository they have
            for repo in repositories:

                # Make sure the repo isnt private and this user owns it
                if (not repo.private):
                    if repo.owner.login == user_dict['login']:

                        # Check if this repo has 1 or more programming languages used in it
                        languages = repo.get_languages()
                        if (languages != {} or languages != None):

                            # For all the languages add on the score for this repo
                            for lang,score in languages.items():
                                if (lang in temp_dict):
                                    temp_dict[lang] = temp_dict[lang] + score
                                else:
                                    temp_dict[lang] = score

            # Take the temp dict and convert it to the desired format [['lang', score], ...]
            for lang, score in temp_dict.items():
                user_dict['languages'].append([str(lang),score])

    except Exception as e:
        print("\n\nCould not get languages: ",e)


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
    user_dict['languages'] = []
    user_dict['commit'] = {0:[], 1:[], 2:[],3:[],4:[],5:[],6:[]}


    repos = user.get_repos()

    getLanguages(repos, user_dict)
    getCommits(repos, user_dict)

    # print(user_dict['commit'])
    # print(user_dict['languages'])
    return user_dict

    # except Exception as e:
    #     print(e)
    #     return user_dict



if __name__ == "__main__":
    app.run()
