# -*- coding: utf-8 -*-
'''
pynagcore.cmd: Module for Nagios Core command notifications
'''
__all__ = ['NagiosCoreCmd', ]

try:
    import os
    import sys
    import argparse
    from jinja2 import Template
except ImportError("Cannot import os, sys, jinja2 modules"):
    exit(100)

class NagiosCoreCmd(object):
    """
    Nagios Core Command class.
    """

    def __init__(self, banner):
        """
        Initialize new instance. Check environment and populate macros.
        """
        self.macros = {}
        self.cmdtypes = {
            '1': 'Service Check',
            '2': 'Service notification',
            '3': 'Host checks',
            '4': 'Host notifications',
            '5': 'Service event and/or global service event handler',
            '6': 'Host event and/or global host event handlers',
            '7': 'OCSP command',
            '8': 'OCHP command',
            '9': 'Service Performance data commands',
            '10': 'Host performance data commands', }

        env = os.environ
        self.macros['banner'] = banner or "ALERT FROM NAGIOS CORE"
        self.macros['HOSTNAME'] = env.get('HOSTNAME')
        self.macros['HOSTDISPLAYNAME'] = env.get('HOSTDISPLAYNAME')
        self.macros['HOSTALIAS'] = env.get('HOSTALIAS')
        self.macros['HOSTADDRESS'] = env.get('HOSTADDRESS')
        self.macros['HOSTSTATE'] = env.get('HOSTSTATE')
        self.macros['HOSTSTATEID'] = env.get('HOSTSTATEID')
        self.macros['LASTHOSTSTATE'] = env.get('LASTHOSTSTATE')
        self.macros['LASTHOSTSTATEID'] = env.get('LASTHOSTSTATEID')
        self.macros['HOSTSTATETYPE'] = env.get('HOSTSTATETYPE')
        self.macros['HOSTATTEMPT'] = env.get('HOSTATTEMPT')
        self.macros['MAXHOSTATTEMPTS'] = env.get('MAXHOSTATTEMPTS')
        self.macros['HOSTEVENTID'] = env.get('HOSTEVENTID')
        self.macros['LASTHOSTEVENTID'] = env.get('LASTHOSTEVENTID')
        self.macros['HOSTPROBLEMID'] = env.get('HOSTPROBLEMID')
        self.macros['LASTHOSTPROBLEMID'] = env.get('LASTHOSTPROBLEMID')
        self.macros['HOSTLATENCY'] = env.get('HOSTLATENCY')
        self.macros['HOSTEXECUTIONTIME'] = env.get('HOSTEXECUTIONTIME')
        self.macros['HOSTDURATION'] = env.get('HOSTDURATION')
        self.macros['HOSTDURATIONSEC'] = env.get('HOSTDURATIONSEC')
        self.macros['HOSTDOWNTIME'] = env.get('HOSTDOWNTIME')
        self.macros['HOSTPERCENTCHANGE'] = env.get('HOSTPERCENTCHANGE')
        self.macros['HOSTGROUPNAME'] = env.get('HOSTGROUPNAME')
        self.macros['HOSTGROUPNAMES'] = env.get('HOSTGROUPNAMES')
        self.macros['LASTHOSTCHECK'] = env.get('LASTHOSTCHECK')
        self.macros['LASTHOSTSTATECHANGE'] = env.get('LASTHOSTSTATECHANGE')
        self.macros['LASTHOSTUP'] = env.get('LASTHOSTUP')
        self.macros['LASTHOSTDOWN'] = env.get('LASTHOSTDOWN')
        self.macros['LASTHOSTUNREACHABLE'] = env.get('LASTHOSTUNREACHABLE')
        self.macros['HOSTOUTPUT'] = env.get('HOSTOUTPUT')
        self.macros['LONGHOSTOUTPUT'] = env.get('LONGHOSTOUTPUT')
        self.macros['HOSTPERFDATA'] = env.get('HOSTPERFDATA')
        self.macros['HOSTCHECKCOMMAND'] = env.get('HOSTCHECKCOMMAND')
        self.macros['HOSTACTIONURL'] = env.get('HOSTACTIONURL')
        self.macros['HOSTNOTESURL'] = env.get('HOSTNOTESURL')
        self.macros['HOSTNOTES'] = env.get('HOSTNOTES')
        self.macros['TOTALHOSTSERVICES'] = env.get('TOTALHOSTSERVICES')
        self.macros['TOTALHOSTSERVICESOK'] = env.get('TOTALHOSTSERVICESOK')
        self.macros['TOTALHOSTSERVICESWARNING'] = env.get('TOTALHOSTSERVICESWARNING')
        self.macros['TOTALHOSTSERVICESUNKNOWN'] = env.get('TOTALHOSTSERVICESUNKNOWN')
        self.macros['TOTALHOSTSERVICESCRITICAL'] = env.get('TOTALHOSTSERVICESCRITICAL')

        self.macros['HOSTGROUPALIAS'] = env.get('HOSTGROUPALIAS')
        self.macros['HOSTGROUPMEMBERS'] = env.get('HOSTGROUPMEMBERS')
        self.macros['HOSTGROUPNOTES'] = env.get('HOSTGROUPNOTES')
        self.macros['HOSTGROUPNOTESURL'] = env.get('HOSTGROUPNOTESURL')
        self.macros['HOSTGROUPACTIONURL'] = env.get('HOSTGROUPACTIONURL')

        self.macros['SERVICEDESC'] = env.get('SERVICEDESC')
        self.macros['SERVICEDISPLAYNAME'] = env.get('SERVICEDISPLAYNAME')
        self.macros['SERVICESTATE'] = env.get('SERVICESTATE')
        self.macros['SERVICESTATEID'] = env.get('SERVICESTATEID')
        self.macros['LASTSERVICESTATE'] = env.get('LASTSERVICESTATE')
        self.macros['LASTSERVICESTATEID'] = env.get('LASTSERVICESTATEID')
        self.macros['SERVICESTATETYPE'] = env.get('SERVICESTATETYPE')
        self.macros['SERVICEATTEMPT'] = env.get('SERVICEATTEMPT')
        self.macros['MAXSERVICEATTEMPTS'] = env.get('MAXSERVICEATTEMPTS')
        self.macros['SERVICEISVOLATILE'] = env.get('SERVICEISVOLATILE')
        self.macros['SERVICEEVENTID'] = env.get('SERVICEEVENTID')
        self.macros['LASTSERVICEEVENTID'] = env.get('LASTSERVICEEVENTID')
        self.macros['SERVICEPROBLEMID'] = env.get('SERVICEPROBLEMID')
        self.macros['LASTSERVICEPROBLEMID'] = env.get('LASTSERVICEPROBLEMID')
        self.macros['SERVICELATENCY'] = env.get('SERVICELATENCY')
        self.macros['SERVICEEXECUTIONTIME'] = env.get('SERVICEEXECUTIONTIME')
        self.macros['SERVICEDURATION'] = env.get('SERVICEDURATION')
        self.macros['SERVICEDURATIONSEC'] = env.get('SERVICEDURATIONSEC')
        self.macros['SERVICEDOWNTIME'] = env.get('SERVICEDOWNTIME')
        self.macros['SERVICEPERCENTCHANGE'] = env.get('SERVICEPERCENTCHANGE')
        self.macros['SERVICEGROUPNAME'] = env.get('SERVICEGROUPNAME')
        self.macros['SERVICEGROUPNAMES'] = env.get('SERVICEGROUPNAMES')
        self.macros['LASTSERVICECHECK'] = env.get('LASTSERVICECHECK')
        self.macros['LASTSERVICESTATECHANGE'] = env.get('LASTSERVICESTATECHANGE')
        self.macros['LASTSERVICEOK'] = env.get('LASTSERVICEOK')
        self.macros['LASTSERVICEWARNING'] = env.get('LASTSERVICEWARNING')
        self.macros['LASTSERVICEUNKNOWN'] = env.get('LASTSERVICEUNKNOWN')
        self.macros['LASTSERVICECRITICAL'] = env.get('LASTSERVICECRITICAL')
        self.macros['SERVICEOUTPUT'] = env.get('SERVICEOUTPUT')
        self.macros['LONGSERVICEOUTPUT'] = env.get('LONGSERVICEOUTPUT')
        self.macros['SERVICEPERFDATA'] = env.get('SERVICEPERFDATA')
        self.macros['SERVICECHECKCOMMAND'] = env.get('SERVICECHECKCOMMAND')
        self.macros['SERVICEACKAUTHOR'] = env.get('SERVICEACKAUTHOR')
        self.macros['SERVICEACKAUTHORNAME'] = env.get('SERVICEACKAUTHORNAME')
        self.macros['SERVICEACKAUTHORALIAS'] = env.get('SERVICEACKAUTHORALIAS')
        self.macros['SERVICEACKCOMMENT'] = env.get('SERVICEACKCOMMENT')
        self.macros['SERVICEACTIONURL'] = env.get('SERVICEACTIONURL')
        self.macros['SERVICENOTESURL'] = env.get('SERVICENOTESURL')
        self.macros['SERVICENOTES'] = env.get('SERVICENOTES')

        self.macros['SERVICEGROUPALIAS'] = env.get('SERVICEGROUPALIAS')
        self.macros['SERVICEGROUPMEMBERS'] = env.get('SERVICEGROUPMEMBERS')
        self.macros['SERVICEGROUPNOTES'] = env.get('SERVICEGROUPNOTES')
        self.macros['SERVICEGROUPNOTESURL'] = env.get('SERVICEGROUPNOTESURL')
        self.macros['SERVICEGROUPACTIONURL'] = env.get('SERVICEGROUPACTIONURL')

        self.macros['CONTACTNAME'] = env.get('SERVICEGROUPALIAS')
        self.macros['CONTACTALIAS'] = env.get('CONTACTALIAS')
        self.macros['CONTACTMAIL'] = env.get('CONTACTMAIL')
        self.macros['CONTACTPAGERS'] = env.get('CONTACTPAGERS')
        self.macros['CONTACTADDRESSn'] = env.get('CONTACTADDRESSn')

        self.macros['CONTACTGROUPALIAS'] = env.get('CONTACTGROUPALIAS')
        self.macros['CONTACTGROUPMEMBERS'] = env.get('CONTACTGROUPMEMBERS')

        self.macros['TOTALHOSTSUP'] = env.get('TOTALHOSTSUP')
        self.macros['TOTALHOSTSDOWN'] = env.get('TOTALHOSTSDOWN')
        self.macros['TOTALHOSTSUNREACHABLE'] = env.get('TOTALHOSTSUNREACHABLE')
        self.macros['TOTALHOSTSDOWNUNHANDLED'] = env.get('TOTALHOSTSDOWNUNHANDLED')
        self.macros['TOTALHOSTSUNREACHABLEUNHANDLED'] = env.get('TOTALHOSTSUNREACHABLEUNHANDLED')
        self.macros['TOTALHOSTPROBLEMS'] = env.get('TOTALHOSTPROBLEMS')
        self.macros['TOTALHOSTPROBLEMSUNHANDLED'] = env.get('TOTALHOSTPROBLEMSUNHANDLED')
        self.macros['TOTALSERVICESOK'] = env.get('TOTALSERVICESOK')
        self.macros['TOTALSERVICESWARNING'] = env.get('TOTALSERVICESWARNING')
        self.macros['TOTALSERVICESCRITICAL'] = env.get('TOTALSERVICESCRITICAL')
        self.macros['TOTALSERVICESUNKNOWN'] = env.get('TOTALSERVICESUNKNOWN')
        self.macros['TOTALSERVICESWARNINGUNHANDLED'] = env.get('TOTALSERVICESWARNINGUNHANDLED')
        self.macros['TOTALSERVICESCRITICALUNHANDLED'] = env.get('TOTALSERVICESCRITICALUNHANDLED')
        self.macros['TOTALSERVICESUNKNOWNUNHANDLED'] = env.get('TOTALSERVICESUNKNOWNUNHANDLED')
        self.macros['TOTALSERVICEPROBLEMS'] = env.get('TOTALSERVICEPROBLEMS')
        self.macros['TOTALSERVICEPROBLEMSUNHANDLED'] = env.get('TOTALSERVICEPROBLEMSUNHANDLED')

        self.macros['NOTIFICATIONTYPE'] = env.get('NOTIFICATIONTYPE')
        self.macros['NOTIFICATIONRECIPIENTS'] = env.get('NOTIFICATIONRECIPIENTS')
        self.macros['NOTIFICATIONISESCALATED'] = env.get('NOTIFICATIONISESCALATED')
        self.macros['NOTIFICATIONAUTHOR'] = env.get('NOTIFICATIONAUTHOR')
        self.macros['NOTIFICATIONAUTHORNAME'] = env.get('NOTIFICATIONAUTHORNAME')
        self.macros['NOTIFICATIONAUTHORALIAS'] = env.get('NOTIFICATIONAUTHORALIAS')
        self.macros['NOTIFICATIONCOMMENT'] = env.get('NOTIFICATIONCOMMENT')
        self.macros['HOSTNOTIFICATIONNUMBER'] = env.get('HOSTNOTIFICATIONNUMBER')
        self.macros['HOSTNOTIFICATIONID'] = env.get('HOSTNOTIFICATIONID')
        self.macros['SERVICENOTIFICATIONNUMBER'] = env.get('SERVICENOTIFICATIONNUMBER')
        self.macros['SERVICENOTIFICATIONID'] = env.get('SERVICENOTIFICATIONID')

        self.macros['LONGDATETIME'] = env.get('LONGDATETIME')
        self.macros['SHORTDATETIME'] = env.get('SHORTDATETIME')
        self.macros['DATE'] = env.get('DATE')
        self.macros['TIME'] = env.get('TIME')
        self.macros['TIMET'] = env.get('TIMET')
        self.macros['ISVALIDTIME:'] = env.get('ISVALIDTIME:')
        self.macros['NEXTVALIDTIME:'] = env.get('NEXTVALIDTIME:')

        self.macros['MAINCONFIGFILE'] = env.get('MAINCONFIGFILE')
        self.macros['STATUSDATAFILE'] = env.get('STATUSDATAFILE')
        self.macros['COMMENTDATAFILE'] = env.get('COMMENTDATAFILE')
        self.macros['DOWNTIMEDATAFILE'] = env.get('DOWNTIMEDATAFILE')
        self.macros['RETENTIONDATAFILE'] = env.get('RETENTIONDATAFILE')
        self.macros['OBJECTCACHEFILE'] = env.get('OBJECTCACHEFILE')
        self.macros['TEMPFILE'] = env.get('TEMPFILE')
        self.macros['TEMPPATH'] = env.get('TEMPPATH')
        self.macros['LOGFILE'] = env.get('LOGFILE')
        self.macros['RESOURCEFILE'] = env.get('RESOURCEFILE')
        self.macros['COMMANDFILE'] = env.get('COMMANDFILE')
        self.macros['HOSTPERFDATAFILE'] = env.get('HOSTPERFDATAFILE')
        self.macros['SERVICEPERFDATAFILE'] = env.get('SERVICEPERFDATAFILE')

        self.macros['PROCESSSTARTTIME'] = env.get('PROCESSSTARTTIME')
        self.macros['EVENTSTARTTIME'] = env.get('EVENTSTARTTIME')
        self.macros['ADMINEMAIL'] = env.get('ADMINEMAIL')
        self.macros['ADMINPAGER'] = env.get('ADMINPAGER')
        self.macros['ARGn'] = env.get('ARGn')
        self.macros['USERn'] = env.get('USERn')

        # Legacy key/values people
        self.macros['USERMAIL'] = env.get('USERMAIL')

    def notification(self, args):
        """
        Build a service notification message template.
        """
        self.recipient = args.recipient or self.macros['USERMAIL'] or self.macros['CONTACTGROUPALIAS']

        if args.cmdtype == 2:
            self.subject = args.subject or \
                           "Host {0} alert for {1}".format(self.macros['HOSTSTATE'], self.macros['HOSTALIAS'])
            self.message = Template("***** {{ banner }} *****\n\n" +
                                    "Notification Type: {{ NOTIFICATIONTYPE }}\n\n" +
                                    "Service: {{ SERVICEDESC }}\n" +
                                    "Host: {{ HOSTALIAS }}\n" +
                                    "Address: {{ HOSTADDRESS }}\n" +
                                    "State: {{ SERVICESTATE }}\n\n" +
                                    "Date/Time: {{ LONGDATETIME }}\n\n" +
                                    "Additional Info:\n\n{{ SERVICEOUTPUT }}")

        if args.cmdtype == 4:
            self.subject = args.subject or \
                           "Service {0} alert for {1}".format(self.macros['SERVICESTATE'], self.macros['SERVICEDESC'])
            self.message = Template("***** {{ banner }} *****\n\n" +
                                    "Notification Type: {{ NOTIFICATIONTYPE }}\n" +
                                    "Host: {{ HOSTALIAS }}\n" +
                                    "State: {{ HOSTSTATE }}\n" +
                                    "Address: {{ HOSTADDRESS }}\n" +
                                    "Additional Info:\n\n{{ HOSTOUTPUT }}" +
                                    "Date/Time: {{ LONGDATETIME }}\n\n")
