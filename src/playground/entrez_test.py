from Bio import Entrez

def search_entrez(keywords: list, amount: int):
    Entrez.email = "henkeladrian@icloud.com"
    for keyword in keywords:
        handle = Entrez.esearch(db='pubmed',
                                sort='relevance',
                                retmax='100',
                                retmode='xml',
                                term=f"{keyword}[TW]")

        record = Entrez.read(handle)
        handle.close()
        print(record)
        print(record['Count'], record['IdList'])
        paper_handle = Entrez.efetch(db='pubmed',
                                     retmode='xml',
                                     id=record['IdList'])
        paper_record = paper_handle.read()
        paper_handle.close()
        paper_list = list(paper_record['PubmedArticle'])
        print(type(paper_list))



if __name__ == '__main__':
    keywords = ["Python", "Federated Learning"]
    search_entrez(keywords=keywords, amount=10)