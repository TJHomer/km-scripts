import click
import requests
import json


host = "http://localhost:8080"
key = "my-api-key"
url = "{}/v1/PEOPLE/list?api_key={}".format(host, key)

r = requests.get(url)
data = r.json()


def number_of_members():
    # displays how many members and trial members there are
    count=0
    people=data['data']
    for person in people:
        if person['PEOPLE_MEMBERSHIPS_ID'] == 8 or person['PEOPLE_MEMBERSHIPS_ID'] == 10:
            count = count + 1
    return count


def membership_id_key(id):
    # changes the member id key from numbers to actual status
    id_list = {5: 'ABANDONDED', 6: 'ALUMNI', 7: 'INTENT', 8: 'MEMBER', 9: 'REJECTED', 10: 'TRIAL'}
    for k,v in id_list.items():
        if k == id:
            return v
        

def is_trial(i, term):
    # searches only trial members
    people=data['data']
    for person in people:
        if person['PEOPLE_MEMBERSHIPS_ID'] == 10:
            if term == 'ALL':
                display_info('trial', person)
                click.echo(person['PEOPLE_UDF5']) #intent info
            else:
                if term in person['PEOPLE_NAME_FIRST'] or term in person['PEOPLE_NAME_LAST']:
                    display_info('trial', person)


            
def display_info(info, person):
    # displays requested information about person.
    # if nothing is specifically requested, it displays member status, name, and email
    person_key = {'basic_info': (person['PEOPLE_NAME_FIRST'] + ' ' + person['PEOPLE_NAME_LAST']),
                  'email':      (person['PEOPLE_EMAIL']),
                  'id':         (str(person['PEOPLE_ID'])),
                  'phone':      (person['PEOPLE_UDF3']),
                  'status':     (membership_id_key(person['PEOPLE_MEMBERSHIPS_ID'])),
                  'intent':     (person['PEOPLE_UDF5']),
                  'pic':        ('Coming soon to a terminal near you!'),
                  'trial':      ("Trial date up: " + str(person['PEOPLE_UDF4']))
                  }
    click.secho(person_key['status'] + ": " + person_key['basic_info'], fg='magenta', bold=True)
    click.echo(person_key['email'])
    for k,v in person_key.items():
        if info == k:
            click.echo(v)


def search_term_digit(info, term):
    # if searching by person's id number
    people = data['data']
    term = str(term)
    for person in people:
        if term == str(person['PEOPLE_ID']):
            display_info(info, person)

    



@click.command()
@click.option('--i', type=click.Choice(['trial', 'phone', 'status', 'intent', 'pic', 'id']),
                                       help='Display specific field information.')
@click.argument('term')
def search(i, term):
    """ This script searches haxdb for people information.\n
        Search 'count' for total number of members.
        Search '-i trial all' for trial member info.
        Or search by name or ID number."""
    term = term.upper()
    if term == 'COUNT':
        click.echo(number_of_members()) 
    elif i == 'trial':
        is_trial(i, term)
    elif term.isdigit():
        search_term_digit(i, term)
    else:
        people = data['data']
        for person in people:
            if term in person['PEOPLE_NAME_FIRST'] or term in person['PEOPLE_NAME_LAST']:
                display_info(i, person)
            



search()



