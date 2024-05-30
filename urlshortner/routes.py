from flask import Blueprint, render_template, request, redirect
from .extensions import db
from .models import URL
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Load the dataset
data = pd.read_csv('urlshortner/dummydata.csv')

# Map 'Yes' and 'No' to 1 and 0
data['Presence of Keywords'] = data['Presence of Keywords'].map({'Yes': 1, 'No': 0})
data['Special Characters'] = data['Special Characters'].map({'Yes': 1, 'No': 0})

# Define features and target
features = ['URL Length','Presence of Keywords','Special Characters'] 
y = data['Clicks']
X = data[features]

# Train a logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

def get_features_for_url(original_url):
    url_length = len(original_url)
    presence_of_keywords = 1 if any(keyword in original_url for keyword in ['website', 'long', 'breaking news', 'cookies', 'chocolate', 'cute', 'animals', 'python', 'question']) else 0
    special_characters = 1 if any(char in original_url for char in ['-', '_']) else 0

    feature_dict = {
        'URL Length': [url_length],
        'Presence of Keywords': [presence_of_keywords],
        'Special Characters': [special_characters]
    }
    return pd.DataFrame(feature_dict)

short=Blueprint('short', __name__)

@short.route('/<short_url>')
def redirect_to_url(short_url):
    link=URL.query.filter_by(short_url=short_url).first_or_404()
    link.clicks+=1
    db.session.commit()
    return redirect(link.orignal_url)

@short.route('/')
def index():
    return render_template('index.html')

@short.route('/shorten',methods=['POST'])
def shorten():
    orignal_url=request.form['orignal_url']
    best_short_url = None
    best_click_likelihood = -1

    for _ in range(10):  # Generate and evaluate 10 short URLs and pick the one with the highest click likelihood
        link=URL(orignal_url=orignal_url)
        short_url=link.short_url
        features = get_features_for_url(orignal_url)
        click_likelihood = model.predict(features)[0]

        if click_likelihood > best_click_likelihood:
            best_click_likelihood = click_likelihood
            best_short_url = short_url

    
    new_url=URL(orignal_url=orignal_url)
    new_url.short_url=best_short_url
    db.session.add(new_url)
    db.session.commit() 
    return render_template('url.html',short_url=best_short_url) 

@short.errorhandler(404)
def page_not_found(e):
    return "not found",404