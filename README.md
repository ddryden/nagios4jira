Description
===========

Nagios event handler for Jira

* Creates issue in Jira when service switched to CRITICAL state
* Creates relationship with similar issues ( same hostname and service name )
* Resolves issue when service switched to OK state

Requirements
============

jira-python >= 0.12

Tested on:
* Ubuntu 12.04
* Jira v5.2.9
* Nagios 3.2.3

Usage
=====


define nagios command

    define command{
      command_name    create-jira-issue
      command_line    /etc/nagios3/scripts/jissue.py $SERVICESTATETYPE$  "** $NOTIFICATIONTYPE$ Service Alert: $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$ **" "$SERVICEOUTPUT$" "$SERVICESTATE$" "$HOSTNOTIFICATIONID$" "$SERVICEDESC$"  "$SERVICESTATE$" "$HOSTNAME$"
    }


add event handler to the service definition:

    event_handler  create-jira-issue


modify USER, PASS, API_URL script variables
