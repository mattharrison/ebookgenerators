# -*- coding: utf-8
import sys


def fix_bullets(lines):
    """Try to convert bullets to rst style bullets, by indenting lines
    in bullet appropriately"""
    for line in lines:
        if line.startswith('-   '):
            indent = 4
        elif line.startswith('-  '):
            indent = 3
        elif line.startswith('- '):
            indent = 2
        else:
            indent = 0
            yield line
            continue
        if indent:
            buffer = []
            yield '\n'
            buffer.append(line)
            while True:
                next_line = lines.next()
                buffer.append(" "*indent+next_line)
                if not next_line.strip():
                    break
            for line in buffer:
                yield line

def remove_carot_l(lines):
    for line in lines:
        line = line.replace(chr(12), '')
        yield line


def remove_two_spaces(lines):
    for line in lines:
        line = line.replace('  ', ' ')
        yield line


def remove_page(lines):
    for line in lines:
        if line.startswith('Page') or line.startswith('(Page'):
            continue
        else:
            yield line


def remove_foo(lines, foo, remove_blanks=True):
    for line in lines:
        if line.startswith(foo):
            continue
        else:
            yield line


class PeekDone(Exception):
    pass


class Peeker(object):
    def __init__(self, seq, sub_peek=True):
        self.seq = iter(seq)
        self.buffer = []

    def pop(self):
        if self.buffer:
            return self.buffer.pop(0)

    def peek(self, n=0):
        """ this can raise an exception if peeking off the end. be
        aware and handle PeekDone appropriately"""
        try:
            if n == len(self.buffer):
                self.buffer.append(self.seq.next())
        except StopIteration as e:
            raise PeekDone('Exhausted')
        return self.buffer[n]

    def __iter__(self):
         return self

    def next(self):
        if self.buffer:
            return self.buffer.pop(0)
        else:
            return self.seq.next()


def remove_double_returns(lines):
    lines = Peeker(lines)
    for line in lines:
        try:
            next_line = lines.peek()
        except PeekDone as e:
            yield line
            return

        if blank(next_line):
            yield line
            try:
                lines.pop()
            except StopIteration as e:
                pass
        else:
            yield line


def remove_excess_returns(lines):
    for line in lines:
        if blank(line):
            while True:
                if not blank(line):
                    break
                line = lines.next()
        yield line


def ends_paragraph(line):
    return line.strip().endswith('.') or line.strip().endswith('"') or len(line) < 86


def ends_sentence(line):
    return line.endswith('.')


def remove_leading_space(lines):
    for line in lines:
        yield line.lstrip()


def blank(line):
    return not line.strip()


def insert_extra_paragraph_line(lines):
    for line in lines:
        if ends_paragraph(line):
            yield line
            yield '\n'
        else:
            yield line


def insert_rst_sections(lines, section_char='-'):
    """ if we have two blank lines treat as a section divider
    """
    lines = Peeker(lines)
    for line in lines:
        try:
            line1 = lines.peek()
        except PeekDone as e:
            # end of content
            yield line
            return
        if blank(line) and blank(line1):
            yield line
            yield '%s\n' % (section_char*40)
            yield line1
            lines.pop()

        else:
            yield line


def fix_space_in_paragraph(lines):
    """ If paragraphs span pages (often) then there could be extra
    returns in the paragraphs....
    """
    lines = Peeker(lines)
    prev = None
    for line in lines:
        try:
            line2 = lines.peek()
        except PeekDone as e:
            yield line
            return
        try:
            line3 = lines.peek(1)
        except PeekDone as e:
            yield line
            yield line2
            return
        if blank(line2) and (not ends_sentence(line)):
            # don't use line2 so pop it
            lines.pop()
        yield line


def remove_dash_page(lines, prev_lines_remove=3, after_lines_remove=2):
    """
    fix stuff like:

    end of page.


    - 6 -

    Next page...
    """
    lines = Peeker(lines)
    for line in lines:
        try:
            for prev in range(prev_lines_remove):
                lines.peek(prev)
            page = lines.peek(prev_lines_remove)
        except PeekDone as e:
            yield line
            continue
        if page.startswith('-') and page.strip().endswith('-'):
            for prev in range(prev_lines_remove):
                lines.pop()
            # remove page
            lines.pop()
            for after in range(after_lines_remove):
                try:
                    lines.peek()
                    lines.pop()
                except PeekDone as e:
                    continue
        yield line

