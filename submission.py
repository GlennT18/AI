from typing import List
from utils import visit_url

# Please do not rename this variable!
TASK3_RESPONSE = """
TODO: Set your answer to task 3's question to this variable's value

Multi-line string is supported, in case you have a longer answer.
"""


def crawler_bfs(seed_url: str):
    frontier = [seed_url]
    uniqueSet = {seed_url}
    depth = 0
    maxDepth = 500

    while frontier:
        nextFrontier = []
        for node in range(len(frontier)):
            current_state = frontier.pop()
            links = visit_url(current_state)

            for link in links:
                if link not in uniqueSet:
                    uniqueSet.add(link)
                    nextFrontier.append(link)
        
        frontier = nextFrontier
        depth += 1
        if depth >= maxDepth:
            print("Max Depth Reached")
            return


def crawler_dfs(seed_url: str):
    #call visit_url
    raise NotImplementedError  # TODO: Replace this line with your code


def word_path(
        dict_file_path: str,
        start_word: str,
        target_word: str,
) -> List[str]:
    raise NotImplementedError  # TODO: Replace this line with your code