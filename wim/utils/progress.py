# bentools.progress
#
# Copyright (C) 2012 Benjamin Bengfort
# License: PSF
# Author: Benjamin Bengfort <benjamin@bengfort.com>
# 
# $Id: progress.py [1] bbengfort $

"""
A class that creates a text representation of a progress bar for use in
terminals or on command line interfaces. It does not use the carraige
return or ANSI codes to reset the bar, but rather the Backspace (0x08) chr
to return to the beginning of the line, and should be compatible with most
terminals. 

    >>> pb_ex = ProgressMeter(total=6000, unit='Kb', ticks=25)

    [=======>                ] 17%  58.2 Kb/sec. 

@author: U{Benjamin Bengfort<mailto:benjamin@bengfort.com>
@license: PSF
@url: U{http://code.activestate.com/recipes/473899-progress-meter/}

@requires: Python 2.6

@version: 1.2
@change: I{progress.py [1] bbengfort}
@since: 2012-12-19 12:18:22 -0400

Credits:
    2006-02-16 vishnubob: original code
    2006-02-20 Denis Barmenkov: ANSI codes replaced by Backspace (0x08)
    2010-05-17 Alexis Lopes: Total time taken and time-to-completion
    2012-12-12 Benjamin Bengfort: Package refactoring
"""

__docformat__ = "epytext en"

###########################################################################
## Imports
###########################################################################

import sys
import time

###########################################################################
## Base Progress Meter
###########################################################################

class ProgressMeter(object):
    """
    A simple progress meter object that can be customized in several ways
    to produce a print on the terminal or in the command line of an
    updating progress bar with units/sec and percent complete represented.
    """
    
    def __init__(self, **kwargs):
        
        # Add customizable properties
        self.unit         = str(kwargs.get('unit', 'operations'))  # Label for the unit
        self.total        = int(kwargs.get('total', 100))          # Number of units to process
        self.count        = int(kwargs.get('count', 0))            # Number of units already processed
        self.stdout       = kwargs.get('stdout', sys.stdout)       # Standard IO 
        self.timestamp    = kwargs.get('timestamp', time.time())   # Start time for tracking
        self.meter_ticks  = int(kwargs.get('ticks', 60))           # The number of ticks in meter
        self.rate_refresh = float(kwargs.get('rate_refresh', .5))  # Refresh rate in seconds

        # Add calculated properties
        self.meter_division = float(self.total) / self.meter_ticks
        self.meter_value    = int(self.count / self.meter_division)

        # Add non customizable properties
        self.last_update      = None
        self.rate_history_idx = 0
        self.rate_history_len = 10
        self.rate_history     = [None] * self.rate_history_len
        self.rate_current     = 0.0
        self.last_refresh     = 0
        self.prev_meter_len   = 0
        self.switch_off       = False

    #//////////////////////////////////////////////////////////////////////
    # Properties
    #//////////////////////////////////////////////////////////////////////

    @property
    def percentage(self):
        """
        Calculates the complete percentage. 

        @returns: The percent of the total counted
        @rtype: C{float}
        """
        return (float(self.count) / float(self.total)) * 100

    @property
    def completed(self):
        """
        A property that checks if the count >= the total.

        @rtype: C{bool}
        """
        return self.count >= self.total
        
    #//////////////////////////////////////////////////////////////////////
    # Methods
    #//////////////////////////////////////////////////////////////////////

    def update(self, count, **kwargs):
        """
        Updates the internal counter of the prograss bar by adding the
        value of count to the internal variable count. This is not used to
        set the percentage, but rather to incremenet it by the number of 
        operations completed.

        @param count: The value to increase the internal count by
        @type count: C{int}

        @returns: None
        """
        # Rate of Progress
        now  = time.time()
        rate = 0.0

        # Progress Incrementing
        self.count += count
        self.count = min(self.count, self.total)

        # Calculate Rate of Progress
        if self.last_update:
            delta = now - float(self.last_update)
            if delta:
                rate = count / delta
            else:
                rate = count

            self.rate_history[self.rate_history_idx] = rate
            self.rate_history_idx += 1
            self.rate_history_idx %= self.rate_history_len

            cnt = 0
            total = 0.0

            # Average rate history
            for rate in self.rate_history:
                if rate == None: continue
                cnt += 1
                total += rate
            rate = total / cnt
        self.rate_current = rate
        self.last_update  = now

        # Device Total by Meter Division
        value = int(self.count / self.meter_division)
        if value > self.meter_value:
            self.meter_value = value
        if self.last_refresh:
            if (now - self.last_refresh) > self.rate_refresh or self.completed:
                self.refresh()
        else:
            self.refresh()

    def set(self, count=None, percent=None, **kwargs):
        """
        Sets the progress bar internal counter to the value specified, 
        then updates the progress bar. This does not increment, but rather
        exactly specifies what the count should be. Alternatively the
        approximate percentage can be set and the updated count will be 
        calculated as close the value of the percent variable.
        
        @param count: The value to set the count to.
        @type count: C{int}

        @param percent: The percentage value to set the counter to
        @type percent: C{float}

        @note: What happens if you specify a count less than the current
            count?

        @returns: None
        @raises: C{ValueError}
        """
        if count and percent:
            raise ValueError("Cannot specify both count and percent")

        elif count is not None:
            if count < self.total:
                count = count - self.count
            else:
                self.count = self.total
                count = 0

        elif percent is not None:
            if percent < 100.0:
                count = int((float(percent) / 100) * self.total)
                count = count - self.count
            else:
                self.count = self.total
                count = 0
        else:
            raise ValueError("Specify either count or percent to set")

        self.update(count)

    def reset(self, **kwargs):
        """
        Resets the progress bar to the initial settings, or with new
        settings specified by the keyword arguments to this method, and
        sets the internal count to 0. This is a fast way of reusing the
        same progress bar object for multiple long running operations.

        @returns: None
        """
        unit         = str(kwargs.get('unit', self.unit))
        total        = int(kwargs.get('total', self.total))
        count        = int(kwargs.get('count', 0))
        stdout       = kwargs.get('stdout', self.stdout)
        timestamp    = kwargs.get('timestamp', None)
        meter_ticks  = int(kwargs.get('ticks', self.meter_ticks)) 
        rate_refresh = float(kwargs.get('rate_refresh', self.rate_refresh))

        self.__init__(unit=unt, total=total, count=count, stdout=stdout,
                      timestamp=timestamp, ticks=meter_ticks, rate_refresh=rate_refresh)

    def refresh(self, **kwargs):
        """
        Refreshes the progress bar and writes to sys.stdout. This method
        is usually called internally, but I've exposed it as a public 
        method in order for exteranl customers to call refresh directly,
        even though it is generally not needed.

        @returns: None
        """
        if self.switch_off:
            return

        # Clear line and return cursor to start-of-line
        self._clear_meter()
        # Get meter text
        meter_text = self._get_meter(**kwargs)
        # Write meter and return cursor to start-of-line
        self.stdout.write(meter_text)
        self._cursor_to_start()

        # Check if we're finished
        if self.completed:
            self.stdout.write('\n')
            # Prevent refreshing after we're over a 100%, a safety measure
            # for loops that continue beyond ProgressMeter.set(100) or 
            # ProgressMeter.update(total)
            self.switch_off = True
        self.stdout.flush()

        self.last_refresh = time.time()

    #//////////////////////////////////////////////////////////////////////
    # Internal helper Methods
    #//////////////////////////////////////////////////////////////////////

    def _clear_meter(self):
        """
        Writes spaces to the terminal and then backspaces to the beginning
        of the line -- any method should be able to call this, not just
        refresh.

        @returns: None
        """
        # Write spaces to blank out the line
        clearstr = " " * self.prev_meter_len
        self.stdout.write(clearstr)

        # Return the cursor to the beginning of the line
        self._cursor_to_start()

    def _get_meter(self, **kwargs):
        """
        Creates the meter and the bar for display. 

        @todo: Allow bar and pad chr to be passed in kwargs.

        @returns: The string representation of the progress bar.
        @rtype: C{str}
        """
        pct = self.percentage
        bar = '=' * self.meter_value

        if self.completed:
            pad = "=" * (self.meter_ticks - self.meter_value)
            meter_text = "[%s=%s] %d%%" % (bar, pad, pct)
        else:
            pad = '-' * (self.meter_ticks - self.meter_value)
            meter_text = "[%s>%s] %d%% %.1f %s/sec." % (bar, pad, pct, self.rate_current, self.unit)
        
        # Update the prev_meter_len value for other methods
        self.prev_meter_len = len(meter_text)

        return meter_text

    def _cursor_to_start(self, length=None):
        """
        Returns the cursor to the start of the line in the terminal, using
        the C{prev_meter_len} by default as the number of backspaces, or
        the optional length parameter that can be passed into the method.

        @param length: The number of backspaces to add.
        @type length: C{int}

        @returns: None
        """
        length = length or self.prev_meter_len
        self.stdout.write('\x08' * length)

    #//////////////////////////////////////////////////////////////////////
    # Object Overrides
    #//////////////////////////////////////////////////////////////////////

    def __repr__(self):
        return "<%s: %i/%i>" % (self.__class__.__name__, self.count, self.total)

    def __str__(self):
        return self._get_meter()

###########################################################################
## Time Estimation Progress Meter
###########################################################################

class TimedProgressMeter(ProgressMeter):
    """
    A progress meter that provides an estimate of the time remaining based
    on the rate of the progress updates, and when complete, prints the 
    total time it took to reach 100%.
    """

    def __init__(self, **kwargs):
        super(TimedProgressMeter, self).__init__(**kwargs)
        self.estimated_duration = []

    #//////////////////////////////////////////////////////////////////////
    # Methods
    #//////////////////////////////////////////////////////////////////////

    def update(self, count, **kwargs):
        """
        Updates the internal counter of the prograss bar by adding the
        value of count to the internal variable count. This is not used to
        set the percentage, but rather to incremenet it by the number of 
        operations completed.

        @param count: The value to increase the internal count by
        @type count: C{int}

        @returns: None

        @note: The override appends to the estimated_duration
        """
        if not self.timestamp: self.timestamp = time.time()
        super(TimedProgressMeter, self).update(count, **kwargs)
        if self.rate_current > 0:
            self.estimated_duration.append((self.total - self.count) / self.rate_current)

    def start(self, **kwargs):
        """
        Sets the progress bar timestamp.

        If this method is not called then ProgressMeter.update() will
        automatically set the timestamp on its first usage. This does not
        override the user specified __init__ settings.

        @returns: None
        """
        if not self.timestamp: self.timestamp = time.time()

    #//////////////////////////////////////////////////////////////////////
    # Internal Helper Methods
    #//////////////////////////////////////////////////////////////////////

    def _get_meter(self, **kwargs):
        """
        Creates the meter and the bar for display. 

        @todo: Allow bar and pad chr to be passed in kwargs.

        @returns: The string representation of the progress bar.
        @rtype: C{str}

        @note: The override adds the time string
        """
        meter_text = super(TimedProgressMeter, self)._get_meter(**kwargs)

        if self.completed:
            time_str = self._completion_time()
        else:
            time_str = self._estimated_time()
            
        meter_text = " ".join((meter_text, time_str))
        
        # Update the prev_meter_len value for other methods
        self.prev_meter_len = len(meter_text)

        return meter_text

    def _completion_time(self):
        """
        Calculates the amount of time it took to complete the operations,
        and returns a string that formats that completion time correctly.

        @returns: The string representation of the completion time.
        @rtype: C{str}
        """
        # Time delta (duration)
        dur = time.time() - self.timestamp

        # Convert to hours, minutes, and seconds
        hours, remainder = divmod(dur, 3600)
        minutes, seconds = divmod(remainder, 60)

        if dur < 60:
            return 'completed in %.f sec.' % seconds
        elif dur >= 60 and dur < 3600:
            return 'completed in %.f min %.f sec.' % (minutes, seconds)
        else:
            if hours == 1:
                return 'completed in %.f hour %.f min %.f sec.' % (hours, minutes, seconds)
            else:
                return 'completed in %.f hours %.f min %.f sec.' % (hours, minutes, seconds)

    def _estimated_time(self):
        """
        Calculates the estimated time remaining based on the refresh rate
        and the current duration, as well as the estimated durations. Then
        returns the string that formats the estimated time correctly.

        @returns: The string representation of the estimated time.
        @rtype: C{str}
        """
        if len(self.estimated_duration) >= 1:
            # parameters to refine time-remaining estimation
            last_estimate = self.estimated_duration[-1]
            if   last_estimate < 15: exp = 1.75; dat = 10
            elif last_estimate >= 15 and last_estimate < 30: exp = 1.5; dat = 15
            elif last_estimate >= 30 and last_estimate < 90: exp = 1.25; dat = 50
            else: exp = 1.00; dat = 50

            # Calculation of time-remaining estimation
            wght_num, wght_den = (0, 0)
            for i in xrange(0, min(len(self.estimated_duration), dat)):
                wght_num += self.estimated_duration[-dat:][i] * ((i+1)**exp)
                wght_den += (i+1)**exp
            est_dur = int(wght_num / wght_den)

            # Convert into hours, minutes, and seconds
            hours, remainder = divmod(est_dur, 3600)
            minutes, seconds = divmod(remainder, 60)

            if est_dur < 60:
                return '%02.f seconds remaining.' % seconds
            elif est_dur >= 60 and est_dur < 3600:
                return '%02.f min %02.f sec remaining.' % (minutes, seconds)
            else:
                if hours == 1:
                    return '%.f hour %02.f min %02.f sec remaining.' % (hours, minutes, seconds)
                else:
                    return '%.f hours %02.f min %02.f sec remaining.' % (hours, minutes, seconds)
        else:
            return "Calculating time remaining..."


###########################################################################
## Main Method for Testing
###########################################################################

if __name__ == "__main__":

    import random

    print "Testing ProgressMeter.update"

    total = 5000
    proga = TimedProgressMeter(total=total, unit='apples')

    while total > 0:
        cnt = random.randint(20, 30)
        proga.update(cnt)
        total -= cnt
        time.sleep(random.uniform(0.25, 0.75))

    print "Testing ProgressMeter.set"

    pct = 0
    progb = ProgressMeter(total=997, unit='oranges', ticks=80)
    while pct < 105:
        pct += random.randint(2, 5)
        progb.set(percent=pct)
        time.sleep(random.uniform(0.25, 0.75))
