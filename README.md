Description
===========

Nagios event handler for Jira

* Creates issue in Jira when service switched to CRITICAL state
* Creates relationship with similar issues ( same hostname and service name )
* Resolves issue when service switched to OK state

Requirements
============

jira python module can be installed with 

    # pip install jira

Tested on:
* OS: Ubuntu 14.04, Debian Wheezy
* Jira v6.3.8
* Nagios 3.4


Usage
=====


+ Define nagios command in your nagios configuration like so:

        define command{
          command_name    create-jira-issue
          command_line    /etc/nagios3/scripts/jissue.py $SERVICESTATETYPE$  "** $NOTIFICATIONTYPE$ Service Alert: $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$ **" "$SERVICEOUTPUT$" "$SERVICESTATE$" "$HOSTNOTIFICATIONID$" "$SERVICEDESC$"  "$SERVICESTATE$" "$HOSTNAME$"
        }


+ Add event handler to the service definition you wish to generate Jira tickets:

    event_handler  create-jira-issue


+ Modify USER, PASS, API_URL, PROJECT, ISSUETYPE script variables in the script or create a config file for the nagios user like the example config file and place it in ~/.jira4nagios.config
