"""main module"""
import sys
from datetime import datetime

from core.search import get_videos
from core.utils import write_json

def main():
    try:
        subject_to_search = sys.argv[1]
        print('Subject', subject_to_search)
    except (KeyError, IndexError) as error:
        print('Please provide a subject to search', error)
        sys.exit(1)

    trends = get_videos(subject_to_search)
    name_to_save = f'{subject_to_search}_{datetime.now().second}.json'
    write_json(trends, name_to_save)


if __name__ == '__main__':
    main()
