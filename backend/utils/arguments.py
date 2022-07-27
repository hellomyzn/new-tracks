import argparse

parser = argparse.ArgumentParser()

def get_env():    
    parser.add_argument("--env", help='optional')
    args = parser.parse_args()
    env = args.env
    return env