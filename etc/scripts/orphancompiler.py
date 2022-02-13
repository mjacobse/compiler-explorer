# -*- coding: utf-8 -*-
# Copyright (c) 2022, Compiler Explorer Authors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from os import listdir
from os.path import isfile, join
import re

COMPILERS_LIST_RE = re.compile(r'compilers=(.*)')
GROUP_NAME_RE = re.compile(r'group\.(.*?)\.')
COMPILER_EXE_RE = re.compile(r'compiler\.(.*?)\.exe')


def process_file(file: str):
    listed_groups = set()
    seen_groups = set()
    listed_compilers = set()
    seen_compilers = set()
    with open(file) as f:
        for line in f:
            match_compilers = COMPILERS_LIST_RE.search(line)
            if match_compilers:
                ids = match_compilers.group(1).split(':')
                for elem_id in ids:
                    if elem_id.startswith('&'):
                        listed_groups.add(elem_id[1:])
                    elif '@' not in elem_id:
                        listed_compilers.add(elem_id)
                continue
            match_group = GROUP_NAME_RE.match(line)
            if match_group:
                seen_groups.add(match_group.group(1))
                continue
            match_compiler = COMPILER_EXE_RE.match(line)
            if match_compiler:
                seen_compilers.add(match_compiler.group(1))
                continue
    bad_compilers = listed_compilers.symmetric_difference(seen_compilers)
    bad_groups = listed_groups.symmetric_difference(seen_groups)
    return file, bad_compilers, bad_groups


def process_folder(folder: str):
    return [process_file(join(folder, f))
            for f in listdir(folder)
            if isfile(join(folder, f))
            and not (f.endswith('.defaults.properties') or f.endswith('.local.properties'))
            and f.endswith('.properties')]


def find_orphans(folder: str):
    result = sorted([r for r in process_folder(folder) if len(r[1]) > 0 or len(r[2]) > 0], key=lambda x: x[0])
    sep = "\n\t"
    for r in result:
        print(f'{r[0]}\nCOMPILERS:\n\t{sep.join(sorted(r[1]))}\nGROUPS:\n\t{sep.join(sorted(r[2]))}\n')


if __name__ == '__main__':
    find_orphans('./etc/config/')
