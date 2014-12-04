__author__ = 'fbrucker'

__all__ = ["ProgressBarPlaceholder", "ProgressBar", "complexity_dissimilarity"]

import datetime
import sys

ESC = '\x1b['


class ProgressBarPlaceholder:
    def __init__(self):
        self.status = ""

    def add(self, number, status=None):
        pass

    def add_max(self, number):
        pass

    def update_status(self, status):
        pass

    def stop(self):
        pass


class ProgressBar(ProgressBarPlaceholder):
    def __init__(self, max_count=0, step=1, outfile=sys.stderr, one_line=True):
        super().__init__()
        self.max_count = max_count
        self.step = step
        self.next_step = 0
        self.current = 0
        self.percent_completion = 0
        self.outfile = outfile
        self.one_line = one_line
        self._former_len = 0

    def add(self, number, status=None):
        self.current += number
        self.percent_completion = 100.0 * self.current / self.max_count
        if self.percent_completion >= 100:
            self.percent_completion = 100
        if status is not None:
            self.update_status(status)
        self._update()

    def add_max(self, max_count):
        self.max_count += max_count

    def update_status(self, status):
        self.status = status
        self._screen()

    def _update(self):
        if self.percent_completion >= self.next_step:
            self._screen()

        while self.percent_completion >= self.next_step and self.next_step <= 100:
            self.next_step += self.step

    def _screen(self):
        if self.status:
            status = "".join((" (", self.status, ") "))
        else:
            status = ""
        to_print = "{0:3.0f}%".format(self.percent_completion) + status + str(datetime.datetime.now())
        if self.one_line and self._former_len:
            self._former_len = len(to_print)
            to_print = "".join((to_print, " " * (self._former_len - len(to_print))))
        else:
            self._former_len = len(to_print)
        print(to_print, end="", flush=True, file=self.outfile)
        if self.one_line:
            print(ESC + str(len(to_print)) + "D", end="", file=self.outfile)
        else:
            print(file=self.outfile)

    def stop(self):
        if self.one_line:
            print("", file=self.outfile)
