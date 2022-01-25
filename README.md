Keyword Paper Miner (KPM)
======================

This is the text mining repository for the seminar "Problem Based Learning <br>
(PBL)" in the winter semester of 2020/21.
Contributors: <br>
* Adrian Henkel
* [Konstantinos Mitsakis](https://github.com/Kostismi)

### Hey thanks for checking out our repository. Down below you will find a small tutorial on how to run our script!
______

1. First of all you to need clone this repository. ☝️
2. After you have done this, either actviate the virtualenvironment in the keyword_paper_miner folder     like this:
    ```bash
    source venv/bin/activate
    ```
    or install all packages that are specified in the [requirements][req] file. <br> 
    A tutorial on how to use virtual environments can be found [here][venv].<br>
    When the virtual environment is active, you can simply run <br> 
    ```bash 
    pip install -r [path to requirements.txt]
    ```
    in order to run all needed packed in one go.
    >CAUTION: The requirement.txt file specifies versions of packages. These packages will be overwritten when being installed outside of the virtualenvironment!
    
3. Then you need to navigate with your terminal to *paper-miner/src/frontend* and run:
    ```bash
    export FLASK_APP=flask_file.py
    flask run
    ```
    You need this in order to tell FLASK which application you want to run.
4. After you have done this, somthing like this should appear:
    ```
    * Serving Flask app "flask_file.py"
    * Environment: production
     WARNING: This is a development server. Do not use it in a production deployment.
     Use a production WSGI server instead.
    * Debug mode: off
     ```
5. Congratulations! 🎉 <br>
Now the application should run on port 5000 on you localhost. Add one of the following URLs into your Browser!
    ```
    http://127.0.0.1:5000/
    or
    http://localhost:5000/
    ```
    From there on it should be self-explanatory. (Obvious hint: The Manual tab should be helpful 😉)
6. If something is not working properly, please feel free to ask us! We will be happy to help you. 💡
<br>
<br>
<img style="float='left';"src="https://media2.giphy.com/media/LmNwrBhejkK9EFP504/giphy.gif?cid=ecf05e47ac7b6060c2de1312e14d1335097ad1f4cb5db286&amp;rid=giphy.gif" alt="Coding GIF by memecandy" style="width: 480px; height: 480px; left: 0px; top: 0px; opacity: 0;">
<img src="https://github.com/mainpyp/paper-miner/blob/main/src/frontend/images/thumbnail_logo.png">


# Keyword Paper Miner Release Notes
## v1.0
06-12-2020

* Release of the fully functional application.
* TODO: Increase efficiency of the K-Score.
* TODO: Explain the K-Score in the manual section.

## v1.1
07-12-2020

* Fixed the runtime problem of the K-Score calculation. 
* TODO: write the K-Score explanation in HTML
* TODO: tune K-Score

## v1.2
07-01-2020

* Final beta application of the Keyword Paper Miner
* TODO: Fetch more papers in order to rank them

## v1.3
20-01-2020

* Makes the About page more interesting
* Adds font-awsome icons to navigation bar and paper (link)
* Adds the funcitonality of fetching more papers per keyword
* Adds the functionality of estimating runtime before running a query
* TODO: Provide the whole abstract when scraping Google Scholar

[req]: https://gitlab.lrz.de/000000000149C8EB/problem-based-learning/-/blob/master/requirements.txt
[venv]: https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/
[KPM]: "https://gitlab.lrz.de/000000000149C8EB/problem-based-learning/-/blob/master/keyword_paper_miner/python_code/frontend/images/thumbnail_logo.png"
