#!/usr/bin/python

from jira.client import JIRA
import sys
import logging

USER = 'nagios'
PASS = 'nagiospw'
API_URL = "http://localhost:8080"

logging.basicConfig(filename='/var/log/nagios3/jira-handler.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

    

def jconnect ():
    try:
        jira = JIRA({'server': API_URL}, basic_auth=(USER, PASS))
        return jira
    except Exception as err:
        err = "Couldn't create connection to jira: %s" % err
        sys.stderr.write(err)
        logging.error(err)

def search_similar_issues (jc, servicedesc, servicestate, hostname):

    query = "labels=%s and labels=%s and labels=%s" % (servicedesc, servicestate, hostname)
    similar_issues = jc.search_issues(query)
    keys = [ "%s" % (issue.key) for issue in similar_issues ]
    return keys

def create_issue (jc, summary, description, alert_id, servicedesc, servicestate, hostname):

    
    try:
        new_issue = jc.create_issue(project={'key': 'DEMO'},
                              summary=summary,
                              description=description,
                              labels=["alertid_"+alert_id, servicedesc, servicestate, hostname],
                              issuetype={'name': 'Bug'})
        logging.info("Created issue with alert_id %s" % alert_id)
        keys = search_similar_issues(jc, servicedesc, servicestate, hostname)
        if len(keys) != 0:
            for key in keys:
                if key != new_issue.key:
                    jc.create_issue_link(type="Relates",
                                        inwardIssue=key,
                                        outwardIssue=new_issue.key)

    except Exception as err:
        err = "Couldn't create issue: %s" % (err)
        sys.stderr.write(err)
        logging.error(err)
        return False

def close_issue (jc, alert_id):
    try:
        nag = jc.search_issues('labels=alertid_'+sys.argv[5])
        jc.transition_issue(nag[0].id, 5)
        logging.info("Closed issue with alert_id %s" % alert_id)
    except Exception as err:
        err = "Couldn't close issue: %s" % (err)
        sys.stderr.write(err)
        logging.error(err)
        return False

def print_usage():
    print "Usage: %s SOFT|HARD <SUMMARY> <DESCRIPTION> CRITICAL|OK ALERT_ID SERVICEDESC  SERVICESTATE" % sys.argv[0]

def main():
    try:    
        nag_state = sys.argv[1] # SOFT/HARD
        summary = sys.argv[2]
        description = sys.argv[3]
        nag_status = sys.argv[4] # CRITICAL/OK
        alert_id = sys.argv[5] # Nagios alert ID
        servicedesc = sys.argv[6]
        servicestate = sys.argv[7]
        hostname = sys.argv[8]
    except IndexError:
        print_usage()
        return False

    jc = jconnect()
    if jc:
        if nag_state == "HARD":
            if nag_status == "CRITICAL":
                create_issue(jc, summary, description, alert_id, servicedesc, servicestate, hostname)
            elif nag_status == "OK":
                close_issue(jc, alert_id)
        elif nag_stage == "SOFT" and nag_status == "UNKNOWN":
            create_issue(jc, summary, description, alert_id)
    else:
        return False

if __name__ == "__main__":
    main()
