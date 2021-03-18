import atexit
import json
import logging
import os
import psycopg2
import time
from typing import List

import lib.duolingo as duolingo


env_json_file: str = os.path.abspath('./env.json')
sess_file: str = os.path.abspath('./duo.sess')
env = {}
lingo = None
conn = None


def init_sql() -> None:
    db: str = env['PG_DB']
    usr: str = env['PG_USER']
    host: str = env['PG_HOST']
    port: str = env['PG_PORT']
    pss: str = env['PG_PASS']

    global conn
    conn = psycopg2.connect(database=db,
                            user=usr,
                            password=pss,
                            host=host,
                            port=port)

    logging.info('Successfully connected to db')


def init_env() -> None:
    global env

    for e in env['env']:
        if e in env:
            msg: str = 'Found env var "%s" in file with default value "%s"'
            logging.info(msg, e, env[e])
        else:
            env[e] = os.environ[e]
            logging.info('Found env var "%s" with value "%s"', e, env[e])


def init_atexit() -> None:
    def end():
        conn.close()
        logging.info('bye')

    atexit.register(end)


def init_duo_log() -> None:
    usr: str = env['DUO_USER']
    pss: str = env['DUO_PASS']

    global lingo
    lingo = duolingo.Duolingo(username=usr,
                              password=pss,
                              session_file=sess_file)
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
    init_sql()


def sleep() -> None:
    logging.info('Sleeping for %d', env['sleep'])
    time.sleep(env['sleep'])


def get_random_user() -> str:
    cur = conn.cursor()
    sql = 'SELECT username FROM duolingo.data.users ORDER BY RANDOM() LIMIT 1'
    cur.execute(sql)

    rows = cur.fetchall()
    user = rows[0][0]
    logging.info('Got random user %s', user)

    return user


def get_friends(name: str) -> List[str]:
    logging.info('Querying friends for %s', name)

    lingo.set_username(name)
    friends_resp = lingo.get_friends()
    friends: List[str] = []

    for fob in friends_resp:
        fob: str = fob['username']
        friends.append(fob)

    logging.info('Found friends:')
    logging.info(friends)
    return friends


def main() -> None:
    init()

    while True:
        user: str = get_random_user()
        get_friends(user)

        sleep()


if __name__ == '__main__':
    main()
