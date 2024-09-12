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
    frontier    = [seed_url]
    uniqueSet   = {seed_url}
    depth       = 0
    maxDepth    = 500

    while frontier:
        nextFrontier = []
        for node in range(len(frontier)):
            currentState = frontier.pop()
            links = visit_url(currentState)
            depth += 1
            if depth >= maxDepth:
                return

            for link in links:
                if link not in uniqueSet:
                    uniqueSet.add(link)
                    nextFrontier.append(link)
                         
        frontier = nextFrontier
        if depth >= maxDepth:
            return


def crawler_dfs(seed_url: str):
    frontier    = [seed_url]
    uniqueSet   = {seed_url}
    depth       = 0
    maxDepth    = 500

    while frontier:
        currentState = frontier.pop()
        if depth >= maxDepth:
            return
        
        links = visit_url(currentState)
        depth += 1
        for link in links:
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
    #creating word dictionary
    totalWords = set()
    with open(dict_file_path, 'r') as file:
        for word in file:
            word = word.strip().lower()
            totalWords.add(word)

    #frontier
    frontier = [start_word]
    goal_state = [target_word]
    used_words = set()
    path = []

    while frontier:
        current_word = frontier.pop()
        path.append(current_word)

        for letter in current_word:
            index = current_word.index(letter)
            for char in 'abcdefghijklmnopqrstuvwxyz':
                current_word[index] = str(char)

                if current_word == target_word:
                    print(path)
                    return path
                
                if current_word in totalWords and current_word not in path:
                    path.append(current_word)
                    frontier.append(current_word)

    # No path found
    return []


    
    
    