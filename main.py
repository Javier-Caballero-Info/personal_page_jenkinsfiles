import getpass
import jenkins
from jinja2 import FileSystemLoader, Environment, select_autoescape
import json
import requests
import sys
import time


jenkins_url = 'http://0.0.0.0:8080'
JENKINSFILE_PROJECT = 'git@github.com:Javier-Caballero-Info/personal_page_jenkinsfiles.git'


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def get_server_instance(username, password):
    return jenkins.Jenkins(jenkins_url, username=username, password=password)


def restart_server():
    url = jenkins_url + "/restart"

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Basic Y2FiYWxsZXJvamF2aWVyMTM6MzY0MTY5OTk=",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data='', headers=headers)

    print(response.text)


def create_folder(folder_name):
    print(" - Creating folder %s ..." % folder_name)
    with open('setup/folder_config.xml', 'r') as file:
        try:
            server.create_job(folder_name, file.read())
        except jenkins.JenkinsException:
            print("   Folder %s already exists" % folder_name)


def create_job(job_name, config):
    print(" - Creating job %s ..." % job_name)

    file_loader = FileSystemLoader('templates')
    template_env = Environment(loader=file_loader, autoescape=select_autoescape(['xml']))

    template = template_env.get_template('job_template.xml')

    job_config = template.render(
        project_url=config['project_url'],
        jenkinsfile_project=JENKINSFILE_PROJECT,
        jenkinsfile=config['jenkinsfile']
    )

    try:
        server.create_job(job_name, job_config)
    except jenkins.JenkinsException:
        try:
            server.reconfig_job(job_name, job_config)
            print("   Job %s updated" % job_name)
        except jenkins.JenkinsException:
            pass


install_plugins = query_yes_no('Do you want to install all the plugins?', "no")

jenkins_user = input("Please enter your username: ")

jenkins_password = getpass.getpass(prompt="Please enter please your password: ")

server = get_server_instance(jenkins_user, jenkins_password)

user = server.get_whoami()

version = server.get_version()

print('Hello %s from Jenkins %s' % (user['fullName'], version))

with open('configuration.json', 'r+') as f:
    data = json.load(f)

    if install_plugins:

        plugins = data['plugins']

        print('\nPreparing to install all the necessary plugins\n')

        for p in plugins:
            print(" - Installing plugin %s ..." % p)
            try:
                server.install_plugin(p, True)
            except IndexError:
                pass

        print('\nAll plugins were installed')

        print('\nRestarting server')

        restart_server()

        time.sleep(120)

        print('\nServer restarted')

    print('\nCreating folders\n')

    folders = data['folders']

    for folder in folders:
        create_folder(folder)

    print('\nAll folders were created')

    print('\nCreating jobs\n')

    jobs = data['jobs']

    for job in jobs:
        create_job(job['full_name'], job['setup'])

    print('\nAll jobs were created')

    env_vars = data['environment_vars']

    print('\nPlease, setup the following environment vars:')

    for e in env_vars:
        print('   - ' + e)

    print('\nConfiguration finished ...  enjoy your jenkins')
