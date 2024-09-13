from typing import List
from utils import visit_url

"""
Sumbit:
submission.py
bfs.txt
dfs.txt
cold-warm.txt
small-short.txt
"""

# Please do not rename this variable!
TASK3_RESPONSE = """
I believe we should use breadth first search for the search enginge. This is becuase the use of BFS allows for more course details to be shown at once
If you search for courses, it will return all of the classes within that directory. But if you are using DFS, you will see a lot more information related
to the first class before you see any information related to the second class.
"""


def crawler_bfs(seed_url: str):
    #setting up frontier, unique set(unique urls), and depth
    frontier    = [seed_url]
    uniqueSet   = {seed_url}
    depth       = 0
    maxDepth    = 500

    #starting bfs
    while frontier:
        nextFrontier = []
        for url in range(len(frontier)):
            #for every url in frontier
            currentState = frontier.pop()
            links = visit_url(currentState)
            depth += 1
            if depth >= maxDepth:
                return
            
            #for each link gathered
            for link in links:
                #if its a new link add it to set and frontier
                if link not in uniqueSet:
                    uniqueSet.add(link)
                    nextFrontier.append(link)
                         
        frontier = nextFrontier
        if depth >= maxDepth:
            return


def crawler_dfs(seed_url: str):
    #set up frontier, uniqueset(unique urls), and depth
    frontier    = [seed_url]
    uniqueSet   = {seed_url}
    depth       = 0
    maxDepth    = 500

    #start dfs search
    while frontier:
        currentState = frontier.pop()
        if depth >= maxDepth:
            return
        
        #getting new links
        links = visit_url(currentState)
        depth += 1
        for link in links:
            #if link is new, add it to set and update frontier
            if link not in uniqueSet:
                uniqueSet.add(link)
                frontier.append(link)  

    if depth >= maxDepth:
        return

def word_path(
        dict_file_path: str,
        start_word: str,
        target_word: str,
) -> List[str]:
    #getting all the words
    totalWords = set()
    with open(dict_file_path, 'r') as file:
        for word in file:
            totalWords.add(word.strip().lower())

    #set up frontier and visited
    frontier = ([(start_word, [start_word])])
    visited = set()
    visited.add(start_word)
    
    #bfs search starts now
    wordLength = len(start_word)
    while frontier:
        currentWord, path = frontier.pop(0)

        #iterate over every character and change it
        for index in range(wordLength):
            for char in 'abcdefghijklmnopqrstuvwxyz':
                nextWord = currentWord[:index] + char + currentWord[index+1:]
                
                if nextWord in totalWords and nextWord not in visited:
                    if nextWord == target_word:
                        return path + [nextWord]
                    
                    visited.add(nextWord)
                    frontier.append((nextWord, path + [nextWord]))
    
    # No path found
    return []


    
    
    