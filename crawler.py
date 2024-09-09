#!/usr/bin/env python3

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Let the crawler perform the specified action.",
    )
    subparsers = parser.add_subparsers(
        required=True,
        dest='action',
        title="actions",
    )
    bfs_parser = subparsers.add_parser(
        'bfs',
        help="Run the crawler using breadth-first search",
        description="Run the crawler using breadth-first search, "
                    "starting from the SEED_URL.",
    )
    dfs_parser = subparsers.add_parser(
        'dfs',
        help="Run the crawler using depth-first search",
        description="Run the crawler using depth-first search, "
                    "starting from the SEED_URL.",
    )
    clean_cache_parser = subparsers.add_parser(
        'clean-cache',
        help="Clean the crawler's cache (does not run the crawler)",
        description="Clean the crawler's cache without running the crawler.",
    )

    bfs_parser.add_argument(
        'seed_url',
        metavar="SEED_URL",
        help="The seed URL",
    )
    dfs_parser.add_argument(
        'seed_url',
        metavar="SEED_URL",
        help="The seed URL",
    )

    args = parser.parse_args()

    import submission
    import utils

    if args.action == 'bfs':
        submission.crawler_bfs(args.seed_url)
    elif args.action == 'dfs':
        submission.crawler_dfs(args.seed_url)
    elif args.action == 'clean-cache':
        utils.clean_cache_dir()


if __name__ == '__main__':
    main()
