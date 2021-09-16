from flask import Flask, request, session, flash, jsonify
from flask.helpers import url_for
from werkzeug.utils import redirect
from .forms import NewsletterForm
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from app import app
import os
import json


#News
@app.route("/newsletter/signup", methods=[ 'POST'])
def newsletter():
    form = NewsletterForm(request.form)        
    if request.method == 'POST' and form.validate():
        try:
            client = MailchimpMarketing.Client()
            client.set_config({
            "api_key": os.environ.get("MAILCHIMP_API_KEY"),
            "server": os.environ.get("MAILCHIMP_SERVER")
        })

            client.lists.add_list_member(os.environ.get("MAILCHIMP_LIST_ID"), {"email_address": form.email.data, "status": "subscribed", "tags":["lead"]})
            flash("Thank you for subscribing", "bg-green-400")
            return redirect(url_for('index'))
        except ApiClientError as error:
            print(error.text)
            res = json.loads(error.text)
            if res['title'] == "Member Exists":
                flash("You are already subscribed!", "bg-yellow-400")
                return redirect(url_for('index'))
            flash("An error occured", "bg-red-400")  
            return redirect(url_for('index'))
    flash("That didn't work", "bg-red-400")
    return redirect(url_for('index'))

