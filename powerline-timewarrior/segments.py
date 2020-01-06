# vim:fileencoding=utf-8:noet
import string
from subprocess import PIPE, Popen
from datetime import datetime

from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info

@requires_segment_info
class TimewarriorBaseSegment(Segment):
    pl = None
    timew_alias = 'timew'

    def execute(self, command):
        self.pl.debug('Executing command: %s' % ' '.join(command))

        proc = Popen(command, stdout=PIPE, stderr=PIPE)
        out, err = [item.decode('utf-8') for item in proc.communicate()]

        if out:
            self.pl.debug('Command output: %s' % out.strip(string.whitespace))
        if err:
            self.pl.debug('Command errors: %s' % err.strip(string.whitespace))

        return out.splitlines(), err.splitlines(), proc.returncode

    def build_segments(self):
        self.pl.debug('Nothing to do')
        return []

    def __call__(self, pl, segment_info, timew_alias='timew'):
        self.pl = pl
        self.timew_alias = timew_alias
        pl.debug('Running Timewarrior: ' + timew_alias)

        if not timew_alias:
            return

        return self.build_segments()

class CurrentTrackSegment(TimewarriorBaseSegment):
    def build_segments(self):
        self.pl.debug('Build current tracked task segment')
        report, err, ret_code = self.execute ([self.timew_alias])
        
        if not err and report and not ret_code:
            current_track = self.get_cur_task (report[0])
            if current_track:
                return [{
                'contents': current_track,
                'highlight_groups': ['timewarrior:current_track'],
                }]
        return []

    def get_cur_task (self, report):
        splitted = report.split('"')
        if splitted[0] == "Tracking ":
            return splitted[1]
        else:
            return report.split(" ")[1]

class TotalWorkingTimeSegment (TimewarriorBaseSegment):
    def build_segments(self):
        self.pl.debug('Build total time of tracked task segment')
        report, err, ret_code = self.execute ([self.timew_alias])
        
        if not err and report and not ret_code:
            total_time = [st for st in report[3].split(" ") if st][1]
            if total_time:
                return [{
                'contents': total_time,
                'highlight_groups': ['timewarrior:total_time'],
                }]
        return []

class BeginWorkingTimeSegment (TimewarriorBaseSegment):
    def __call__ (self, pl, segment_info, timew_alias="timew", format="%H-%M"):
        self.pl = pl
        self.timew_alias = timew_alias
        self.format = format

        if not timew_alias:
            return

        pl.debug ("Running timewarrior: " + self.timew_alias)

        return self.build_segments (self.format)

    def build_segments(self, format="%H-%M"):
        self.pl.debug('Build beginning time of tracked task segment')
        report, err, ret_code = self.execute ([self.timew_alias])
        
        if not err and report and not ret_code:
            full_begin_date = datetime.strptime ([st for st in report[1].split(" ") if st][1], "%Y-%m-%dT%H:%M:%S")
            if full_begin_date:
                return [{
                'contents': full_begin_date.strftime (format),
                'highlight_groups': ['timewarrior:total_time'],
                }]
        return []

current_track = with_docstring(
    CurrentTrackSegment(),
    '''Return information from Timewarrior time tracker.

    It shows the current tracked task

    Highlight groups used: ``timewarrior:current_track``
    ''')

total_time = with_docstring(
    TotalWorkingTimeSegment(),
    '''Return information from Timewarrior time tracker.

    It shows the total elapsed time on the current tracked task.

    Highlight groups used: ``timewarrior:total_time``
    ''')

begin_time = with_docstring(
    BeginWorkingTimeSegment(),
    '''Return information from Timewarrior time tracker.

    It shows the beginning of the current tracked task.

    Highlight groups used: ``timewarrior:begin_time``
    ''')
