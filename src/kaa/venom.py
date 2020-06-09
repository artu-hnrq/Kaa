import re

def docfy(key, value, *filenames):
    key = f"<!-- {key} -->"

    for filename in filenames:
        with open(filename) as file:
            updated_text = re.sub(
                f"{key}(.*)$",
                f"{key} {value}",
                file.read(),
                flags = re.MULTILINE
            )

        with open(filename, 'w') as file:
            file.write(updated_text)


# Head
import configparser
from github import Github

github = Github("a59cad280b756743ad24ed9615b55797f3382175")


def summary():
    config = configparser.ConfigParser()
    config.read('setup.cfg')

    summary = config['metadata']['description']
    docfy('summary', summary, 'DESCRIPTION.md', 'README.md')
    github.get_user().get_repo('Kaa').edit(description = summary)
