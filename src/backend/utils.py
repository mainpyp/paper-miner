import re


def parse_sss(keywords:str = None) -> list:
    """
    This method parses semicolon separated strings.
    It returns a list of strings.
    """
    if not keywords:
        return []

    keywords = keywords.split(";")
    for index, word in enumerate(keywords):
        keywords[index] = word.strip()
    return list(filter(None, keywords))


def parse_papers(papers: list = None, scraped: str = "scholarly"):
    parsed_papers = {}
    if not papers:
        return []
    if scraped == "scholarly":
        for keyword in papers:
            keyword_papers = []
            for paper in papers[keyword]:
                authors = list(filter(None, paper.bib['author']))
                parsed_paper = {}
                if len(authors) == 0:
                    parsed_paper['author'] = "not available"
                else:
                    parsed_paper['author'] = authors[0]
                parsed_paper['title'] = paper.bib['title']
                try:
                    parsed_paper['abstract'] = paper.bib['abstract']
                except KeyError:
                    pass
                parsed_paper['citations'] = paper.bib['cites']
                parsed_paper['published'] = paper.bib['year']
                try:
                    parsed_paper['paper_url'] = paper.bib['url']
                    x = re.search('www.(\D*)\.', paper.bib['url'])
                    if x:
                        match = x.group(1)
                        parsed_paper['website'] = match
                    if parsed_paper['paper_url'].endswith(".pdf"):
                        parsed_paper["is_pdf"] = True

                except KeyError:
                    parsed_paper['paper_url'] = "No URL was found"
                parsed_paper['co_authors'] = ";".join(authors[1:])
                parsed_paper['author_ids'] = paper.bib['author_id']
                keyword_papers.append(parsed_paper)
            parsed_papers[keyword] = keyword_papers
    return parsed_papers


def sort_list_of_papers_by(found_papers: list, evaluation_measure: str):
    """
    PARAMETERS:
        List of papers (dicts)
    SORT BY:
        Kotsis score (K-score)
        Citations of each paper
    """
    if evaluation_measure == "K-Score":
        for keyword in found_papers:
            keyword_papers = found_papers[keyword]
            found_papers[keyword] = sorted(keyword_papers, key=lambda i: int(i['score']), reverse=True)
    elif evaluation_measure == "Citations":
        for keyword in found_papers:
            keyword_papers = found_papers[keyword]
            found_papers[keyword] =  sorted(keyword_papers, key=lambda i: int(i['citations']), reverse=True)
    elif evaluation_measure == "Year":
        for keyword in found_papers:
            keyword_papers = found_papers[keyword]
            print(keyword_papers)
            for paper in keyword_papers:
                try:
                    int(paper["published"])
                except ValueError:
                    paper["published"] = 1930
            found_papers[keyword] = sorted(keyword_papers, key=lambda i: int(i['published']), reverse=True)


def get_h_indexes(authors:list=None):
    """
    i10-Index = the number of publications with at least 10 citations.
    the H index is a general researcher rating index that takes into account
    a lot of parameters like average citations,
    holding important positions in universities as well as awards.
    takes author id list returns the max h index of the authors.
    """
    author_h_indexes=[]
    for author in authors:
        author.fill(sections=["indices"])
        author_h_indexes.add(author.hindex)
    return(max(author_h_indexes))


def get_i10(authors:list=None):
    author_i_indexes = []
    for author in authors:
        author.fill(sections=["indices"])
        author_i_indexes.add(author.i10index)
    return (max(author_i_indexes))


def get_abstract(paper_url: str):
    from urllib.request import urlopen
    import re
    html_content = urlopen('https://www.google.de').read()
    matches = re.findall('(\<).{100,10000}', html_content)

    if len(matches) == 0:
        print('I did not find anything')
    else:
        print(matches)
