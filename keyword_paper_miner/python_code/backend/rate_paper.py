from scholarly import scholarly
import datetime
import requests
import re
now = datetime.datetime.now()


"""
these functios calculate the score for each of the 4 rating ways.
Each function returns one score which will be added up to form the end score of the paper,
The funtions will get for parameters the dictionary of each paper(see Utils wrote by Adrian),
as well as the rating weight preference from the website.
returns the score for each author in regards of their h index and i10 index.
i10-Index = the number of publications with at least 10 citations.
the H index is a general researcher rating index that takes into account
a lot of parameters like average citations,
holding important positions in universities as well as awards."""
def get_indexes_scores(author,preferences:str=None):

    sum_indexes_old = 0
    sum_indexes_new = 0
    author.fill(sections=["indices"])
    sum_indexes_old += author.hindex + author.i10index
    sum_indexes_new += author.hindex5y + author.i10index5y
    if preferences == "year":
        sum_indexes_new * 3
    else:
        sum_indexes_new * 2
    return (sum_indexes_old + sum_indexes_new)



def get_indexes_scores_with_id(author_ids:list=None,preferences:str=None):
    """new is newer than five years, old is from begining till current.
    """
    sum_indexes_old = 0
    sum_indexes_new = 0
    for author_id in author_ids:
        url = f'https://scholar.google.com/citations?user={author_id}&hl=en'
        request = requests.get(url)

        if request.status_code != 200:
            """
            Status code is not 200, error while downloading html page.
            """
            print(f'Error: Status Code {request.status_code} for {author_id}')
        else:
            """
            Use regular expression to get h-index, i10-index
            """
            h_index = re.findall(r'h-index</a></td><td class="gsc_rsb_std">[0-9]+</td><td class="gsc_rsb_std">[0-9]+</',
                                 request.text)
            i10_index = re.findall(
                r'i10-index</a></td><td class="gsc_rsb_std">[0-9]+</td><td class="gsc_rsb_std">[0-9]+</', request.text)

            h_index = re.findall(r'[0-9]+', str(h_index))
            i10_index = i10_index[0][3:]
            i10_index = re.findall(r'[0-9]+', str(i10_index)[3:])
            if h_index is not None:
                sum_indexes_old +=int(h_index[0])
                sum_indexes_new +=int(h_index[1])

            if i10_index is not None:
                sum_indexes_old += int(i10_index[0])
                sum_indexes_new += int(i10_index[1])

    """
    if the preference is year then we give the new h and i index an extra boost.
    """
    if preferences == "year":
        sum_indexes_new * 5
    else:
        sum_indexes_new * 2

    return (sum_indexes_old + sum_indexes_new)



def authenticate_authors(author_ids: list = None, author_names: list = None):
    authors = []
    authenticated_authors = []
    for author in author_names:

        search_query = list(scholarly.search_author(author))
        if search_query != []:
            authors.append((search_query))

    """ authenticate authors, we get a list of scholarly author objects.
    in case of 2 authors with the same name we decide by the auther id
    (if author id in our author id list the append to authenticated authors
    the 2 for lops may look computationally questionable however our lists are small
    and most often will have a length of 1 for possible_authors
    and <10 for authors 
    """
    for posible_author in authors:
        for author in posible_author:
            if ((author.id) in author_ids):
                authenticated_authors.append(author)
            else:
                continue
    return authenticated_authors



def rate_authors(parsed_papers: dict = None,preferences:str=None):
    score_authors = 0
    author_ids = (parsed_papers["author_id"])
    all_authors = []
    all_authors.append(parsed_papers["author"])
    all_authors.append(parsed_papers["co_authors"])
    auth_authors = authenticate_authors(author_ids, all_authors)
    for author in auth_authors:
        score_authors += get_indexes_scores(author,preferences)
    if (preferences == "author"):
        score_authors = score_authors * 10
    return (score_authors)


def rate_authors_by_id(parsed_papers: dict = None,preferences:str=None):
    score_authors = 0
    author_ids = (parsed_papers["author_ids"])
    authenticate_authors_ids=[]
    for author_id in author_ids:
        if(author_id!=None):
            authenticate_authors_ids.append(author_id)
    if(len(authenticate_authors_ids)>0):
        score_authors += get_indexes_scores_with_id(authenticate_authors_ids,preferences)
    else:
        score_authors=50
    if (preferences == "author"):
        score_authors = score_authors * 10
    return (score_authors)




# calculating score based on number of citations
def rate_citations(parsed_papers: dict = None,preferences:str=None):
    num_of_citations = int(parsed_papers["citations"])
    if (preferences == "citations"):
        score_citations = num_of_citations * 3
    else:
        score_citations = num_of_citations

    return score_citations


# calculating score based on year of publishment
def rate_year(parsed_papers: dict = None,preferences:str=None):
    # year paper was published
    try:
        year = int(parsed_papers["published"])
    except ValueError:
        print(parsed_papers)
        year = 1930
        parsed_papers["published"] = 1930

    # current year
    this_year = now.year
    # maximum score paper can get if priority is year
    max_prior = 2400
    # maximum score paper can get if priority is NOT year
    max_non_prior = 480
    # if the main priority is year
    if (preferences == "year"):
        score_year = max_prior - (this_year - year) * 10
    else:
        score_year = max_non_prior - (this_year - year) * 10
    if(score_year<0):
        score_year=0
    return score_year


def rate_paper(paper: dict = None, preferences:str=None):
    score = 0
    score += rate_authors_by_id(paper,preferences)
    score += rate_year(paper,preferences) + rate_citations(paper,preferences)
    return score


def rate_all_papers(parsed_papers: list, keywords: list, preferences: str):
    if not preferences:
        preferences = "citations"
    if len(parsed_papers) == 0:
        return
    for keyword in keywords:
        for paper in parsed_papers[keyword]:
            start = datetime.datetime.now().replace(microsecond=0)
            paper['score'] = rate_paper(paper=paper, preferences=preferences)
            end = datetime.datetime.now().replace(microsecond=0)
            print(f"Rate one paper: {end - start}")





if __name__ == '__main__':
    print(list(scholarly.search_author("S Jones")))
