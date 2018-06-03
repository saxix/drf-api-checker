# -*- coding: utf-8 -*-
import os


def mktree(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired "
                      "dir, '%s', already exists." % newdir)
    else:
        os.makedirs(newdir)


def clean_url(url):
    return url[1:-1].replace('/', '_')


def get_filename(base, name):
    filename = os.path.join(base, name)
    if not os.path.exists(filename):
        mktree(os.path.dirname(filename))
    return filename

#
# def get_response_filename(base, url):
#     return get_filename(base, clean_url(url) + '.response.json')
#
#
# def get_fixtures_filename(base, basename='fixtures'):
#     return get_filename(base, f'{basename}.json')
