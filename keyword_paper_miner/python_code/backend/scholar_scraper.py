from scholarly import scholarly
from python_code.backend.utils import parse_papers

def search_for_papers(keywords: list, amount: int) -> dict:
    f""" This functions returns the first {amount} number of the most cited papers
    of each keyword in {keywords} in descending order. 

    :param keywords: List of keywords as string
    :param amount: amount of papers that are found
    :return: Dictionary of keywords with a list of papers as values
    """
    result = {}
    for keyword in keywords:
        search_query = scholarly.search_pubs(keyword)
        for i, paper in enumerate(search_query):
            if keyword not in result:
                result[keyword] = [paper]
            else:
                result[keyword].append(paper)
            if i == amount - 1:
                break
    return result




if __name__ == '__main__':
    keywords = ['Principles of protein-protein interactions']
    amount = 5
    papers = search_for_papers(keywords=keywords, amount=amount)
