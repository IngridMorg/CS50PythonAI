import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    print(corpus)

    #TESTING



    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #declare dictionary
    model = {}
    #if page has no putgoing links then the probability distrubution we should return will choose randomly among all
    #pages with equal probability
    pages = len(corpus[page])
    if(corpus[page] == None):
        #then we just choose randomly from all
        prob = 1 / pages
        print(prob)
        #ensure that the parameter page is also in the dictionary
        model[page] = prob
        #add all they keys in the corpus to the new dictionary
        #and assign them their probability
        for key in corpus[page]:
            model[key] = prob
        return model
    else:
        #we dont have a page that doesnt link to anything
        #so we need to do some more fun maths
        #dampinging on its own probability:
        prob1 = damping_factor / pages
        #1- dampening factor probability:
        prob2 = (1-damping_factor) / (pages +1)

        #add the parameter page to the dictionar
        model[page] = prob2
        #iterate over the linked pages to add their proability
        for key in corpus[page]:
            model[key] = prob1 + prob2
        return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #in random surfer we keep track of how many times a page will appear in our sample
    #so initially our dictionary will consist of every page with an integer value representing the amount of times the page has been visitied
    #then once all sample are complete we divide each of the integers by n to find the probability

    #we are going to loop n-1 times as the first time we are going to choose a page at random
    pages = len(corpus)
    firstPage = random.choice(list(corpus.keys()))
    #initialise the dictionary this function will return
    model = {}
    for key in corpus:
        model[key] = 0
    model[firstPage] = 1
    #use transition model to generate the first probability distrubution
    probModel = transition_model(corpus,firstPage, damping_factor)
    for i in range(0,n-1):
        #using probModel we need to determine what page to visit next
        pages = []
        probs = []
        for key,val in probModel.items():
            pages.append(key)
            probs.append(val)

        sample = random.choices(pages, weights=probs)[0]
        model[sample] +=1
        probModel = transition_model(corpus,sample, damping_factor)
    for i in model:
        model[i] = model[i] / n

    print(model)
    return model


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
