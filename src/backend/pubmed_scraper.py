from pymed import PubMed
from pubmed_lookup import PubMedLookup, Publication
from json import loads

def crawl_pubmed(keywords: list, amount: int):
    """
    This function creates a pymed query and sends it to pymed.
    The result is a dictionary following this structure:
    keyword -> list of papers
    paper -> dictionary
    """
    pubmed = PubMed(tool="MyTool", email="my@email.address")
    results = {}
    for keyword in keywords:
        our_query = f"{keyword}[Keywords]"
        keyword_results = pubmed.query(query=our_query, max_results=amount)
        results[keyword] = [loads(queried_paper.toJSON()) for queried_paper in keyword_results]
    parsed_results = {}
    for keyword in results:
        list_of_papers = results[keyword]
        parsed_results[keyword] = []
        for each_paper in list_of_papers:
            parsed_paper = {}
            id = each_paper['pubmed_id']
            lookup = PubMedLookup(id, "henkeladrian@icloud.com")
            publication = Publication(lookup)
            authors = each_paper['authors']
            co_authors = (';').join(
                [f"{authors[i]['firstname']} {authors[i]['lastname']}" for i in range(1, len(authors))])
            parsed_paper['author'] = f"{authors[0]['firstname']} {authors[0]['lastname']}"
            parsed_paper['title'] = each_paper['title']
            parsed_paper['abstract'] = publication.abstract
            parsed_paper['citations'] = 0
            parsed_paper['published'] = publication.year
            parsed_paper['paper_url'] = publication.url
            parsed_paper['co_authors'] = co_authors
            parsed_results[keyword].append(parsed_paper)
    return parsed_results

if __name__ == '__main__':
    #  Here I run our method that returns the result
    scraped_papers = crawl_pubmed(["Proteins"], amount=5)
    #  This is for you to figure out what will be printed out!
    for keyword in scraped_papers:
        for paper in scraped_papers[keyword]:
            print(paper['author'] + "\n",
            paper['title'] + "\n",
            paper['published'] + "\n",
            paper['paper_url'] + "\n",
            paper['co-authors'] + "\n")
