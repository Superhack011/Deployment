from flask import Flask , Blueprint, request, json, flash, jsonify
from app import db
from .models import User,Report

views = Blueprint('views',__name__)

from urllib.parse import urlparse
def is_valid_url(url):
    parsed = urlparse(url)
    return all([parsed.scheme,parsed.netloc])

import requests
def is_Ok(url):
    response = requests.get(url, timeout=5)

    if (response.status_code == 200):
        return True
    else: return False;

import socket
def dns_validation(url):
    return socket.gethostbyname(urlparse(url).netloc)

import whois
def Whois_Check(url):
    url = urlparse(url).netloc
    wrepo = whois.whois(url)

    return wrepo.domain_name

@views.route('/check_url',methods=['POST'])
def urlReport():
    data = request.get_json()
    url = data.get('url','')

    try:
        new_user = User(name = url)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e :
        db.session.rollback()
        flash(f'An error occured {str(e)}',category='error')

    result = {
        "Valid" : False,
        "Formation" : "",
        "Reachability" : "",
        "DNS validity" : "",
        "SSL Certificate" : False,
        "Whois LookUp" : "",
        "Score" : 0
    }

    if is_valid_url(url) :
        result["Formation"] = "Valid Formation."
        result["Score"] += 10
    else : result["Formation"] = "Non Valid Formation."

    if is_Ok(url):
        result["Reachability"] = "A Responsive Url."
        result["Score"] += 20
    else : result["Reachability"] = "Non Responsive Url."
    
    if dns_validation(url):
        result["DNS validity"] = "Valid DNS."
        result["Score"] += 20
    else: result["DNS validity"] = "Not a Valid DNS."

    result["Whois LookUp"] = Whois_Check(url)
    if result["Whois LookUp"] != "":
        result["Score"] += 10;

    if result["Score"] > 50:
        result["Valid"] = True

    try:
        new_report = Report(validity=result["Valid"],formation=result["Formation"],
                            reachability=result["Reachability"],dns=result["DNS validity"],
                            ssl=result["SSL Certificate"],whois=result["Whois LookUp"],score=result["Score"],
                            user_id=new_user.id)

        db.session.add(new_report)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"The error occured is {str(e)}.!")

    return jsonify(result)


@views.route('/user',methods=['GET','POST'])
def user_list():
    users = User.query.all()

    userList = []
    for user in users:
        userList.append({
            "User Id " : user.id,
            "User Name ": user.name,
            "DateTime" : user.timestamp
        })

    return jsonify(userList)

@views.route('/all_report',methods=['GET','POST'])
def report_list():
    reports = Report.query.all()
    reportList = []

    for report in reports :
        reportList.append({
            "Valid" : report.validity,
            "Formation" : report.formation,
            "Reachability" : report.reachability,
            "DNS validity" : report.dns,
            "SSL Certificate" : report.ssl,
            "Whois LookUp" : report.whois,
            "Score" : report.score,
            "TimeStamp" : report.user.timestamp
        })

    return jsonify(reportList)
