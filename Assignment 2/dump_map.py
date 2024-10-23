#!/usr/bin/env python3

import argparse
from typing import TextIO

from city_map import CityMap


def dump_map(city_map: CityMap, file: TextIO) -> None:
    """Dump a dense overview of the provided map to a file,
    with tags for each location."""
    for label in city_map.geolocations:
        tags_str = " ".join(city_map.tags[label])
        print(f"{label} ({city_map.geolocations[label]}): {tags_str}",
              file=file)
        for label2, distance in city_map.distances[label].items():
            print(f"  -> {label2} [distance = {distance}]", file=file)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Dump a map file in a readable format to an output file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-m', '--map',
        type=str,
        default='data/rit-map.pbf',
        help="Map file (.pbf)",
    )
    parser.add_argument(
        '-l', '--landmarks',
        type=str,
        default='data/rit-landmarks.json',
        help="Landmark file (.json)",
    )
    parser.add_argument(
        '--output',
        type=str,
        default='readable-map.txt',
        help="Output file to write to",
    )
    args = parser.parse_args()

    # Do slow imports after argument parsing to speed up '--help',
    # invalid argument messages, etc.
    from map_utils import create_map_with_landmarks

    pbf_filename = args.map
    landmark_filename = args.landmarks
    output_filename = args.output
    with open(output_filename, 'w') as output_file:
        city_map = create_map_with_landmarks(pbf_filename, landmark_filename)
        dump_map(city_map, output_file)
        print(f"Dumped map {pbf_filename} "
              f"with landmarks in {landmark_filename} to:\n"
              f"\t{output_filename}")


if __name__ == "__main__":
    main()
