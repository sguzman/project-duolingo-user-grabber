import atexit
import duolingo
import json
import logging
import os
import typing
from typing import Dict
from typing import List
from typing import Optional


env_json_file: str = os.path.abspath('./env.json')
env = {}
sessfile: str = os.path.abspath('./.duo.sess')
lingo = None


def init_env() -> None:
    for e in env['env']:
        if e in env:
            logging.info('Found env var "%s" in file with default value "%s"', e, env[e])
        else:
            env[e] = os.environ[e]
            logging.info('Found env var "%s" with value "%s"', e, env[e])


def init_atexit() -> None:
    def end():
        logging.info('bye')

    atexit.register(end)


def init_duo_log() -> None:
    usr: str = env['DUO_USER']
    pss: str = env['DUO_PASS']

    lingo = duolingo.Duolingo(username=usr, password=pss)
    logging.info('Success logged in with user "%s" and pass "%s"', usr, pss)
    logging.info(lingo)


def init_logging() -> None:
    name: str = env['name']

    logging.basicConfig(
        format=f'{name} %(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info('hi')


def init_json() -> None:
    global env

    json_file = open(env_json_file, 'r')
    env = json.load(json_file)


def init() -> None:
    init_json()
    init_logging()
    init_env()
    init_atexit()
    init_duo_log()


def main() -> None:
    init()


if __name__ == '__main__':
    main()
