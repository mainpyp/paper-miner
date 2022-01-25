from flask import Flask, render_template, redirect, url_for
import sys
sys.path.insert(0, "../..")
import os
from python_code.frontend.forms import EnterSettingsForm
from python_code.backend.utils import parse_sss, parse_papers, sort_list_of_papers_by
from python_code.backend.scholar_scraper import search_for_papers
from python_code.backend.pubmed_scraper import crawl_pubmed
from python_code.backend.rate_paper import rate_all_papers

IMAGE_FOLDER = os.path.join('static', 'images')

#  Tells that this file is the APP
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER


app.config['SECRET_KEY'] = '544276676f53b5ecb8dbcd6d69b10241'

papers = {}


@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def home():
    """
    / is the root page of our website and the function returns the html code to
    the website.
    Both routes cover the same page. The function renders the home.html file.
    """
    form = EnterSettingsForm()
    if form.validate_on_submit():  # checks if any keyword is given
        papers.clear()
        #  Google Scholar
        keywords = parse_sss(form.keywords.data)
        website = form.website.data
        evaluation_general = form.rating.data
        evaluation_measure_k_score = form.preferences.data
        print(f"Searching for {keywords}")
        if website == "Google Scholar":
            found_papers = parse_papers(search_for_papers(keywords=keywords, amount=int(form.output_amount.data)))
            if evaluation_general == "K-Score":
                from datetime import datetime
                time = len(keywords) * int(form.output_amount.data)
                if time <= 60:
                    time = f"{time} seconds"
                else:
                    time = f"{(time / 60):.2f} minutes"
                start = datetime.now().replace(microsecond=0)
                rate_all_papers(parsed_papers=found_papers, keywords=keywords, preferences=evaluation_measure_k_score)
                sort_list_of_papers_by(found_papers, evaluation_measure="K-Score")
                end = datetime.now().replace(microsecond=0)
                print(f"Rate all papers: {end - start}")
                papers.update(found_papers)
            elif evaluation_general == "Citations":
                sort_list_of_papers_by(found_papers, evaluation_measure="Citations")
                papers.update(found_papers)
            elif evaluation_general == "Year":
                sort_list_of_papers_by(found_papers, evaluation_measure="Year")
                papers.update(found_papers)
            else:
                papers.update(found_papers)
        elif website == "PubMed":
            found_papers = crawl_pubmed(keywords=keywords, amount=int(form.output_amount.data))
            papers.update(found_papers)
        return redirect(url_for('results'))
    return render_template('home.html', form=form)

@app.route('/results')
def results():
    sorted_paper = None
    return render_template('results.html', papers=papers, title="Results")

@app.route("/manual")
def manual():
    """
    /manual is the manual of the keyword paper miner
    """
    return render_template('manual.html', title="Manual")

@app.route("/k_score")
def k_score():
    """
    /k_score is the page where the k Score is explained
    """
    return render_template('k_score.html', title="Explanation of the K-Score")

@app.route("/about")
def about():
    """
    /manual is the manual of the keyword paper miner
    """
    kostis = os.path.join(app.config['UPLOAD_FOLDER'], 'kostis.jpeg')
    yazgi = os.path.join(app.config['UPLOAD_FOLDER'], 'yazgi.jpeg')
    adrian = os.path.join(app.config['UPLOAD_FOLDER'], 'adrian.jpeg')
    return render_template('about.html', title="About us", kostis=kostis, yazgi=yazgi, adrian=adrian)

if __name__ == '__main__':
    print("The app is running on 127.0.0.1:5000")
    app.run(debug=True)
