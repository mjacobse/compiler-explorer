// Copyright (c) 2019, Compiler Explorer Authors
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//     * Redistributions of source code must retain the above copyright notice,
//       this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above copyright
//       notice, this list of conditions and the following disclaimer in the
//       documentation and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

'use strict';
const monaco = require('monaco-editor');
const asm = require('./asm-mode');

function definition() {
    const ptx = $.extend(true, {}, asm); // deep copy

    // Redefine registers for ptx:
    // Usually ptx registers are in the form "%[pr][0-9]+", but a bunch of magic registers does not follow
    // this scheme (see https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#special-registers ).
    // Thus the register-regex captures everything that starts with a '%'.
    ptx.registers = /%[a-z0-9_\\.]+/;

    // Redefine whitespaces, as asm interprets strings with a leading '@' as comments.
    ptx.tokenizer.whitespace = [
        [/[ \t\r\n]+/, 'white'],
        [/\/\*/, 'comment', '@comment'],
        [/\/\/.*$/, 'comment'],
        [/[#;\\].*$/, 'comment'],
    ];

    // Add predicated instructions to the list of root tokens. Search for an opcode next, which is also a root token.
    ptx.tokenizer.root.push([/@%p[0-9]+/, {token: 'operator', next: '@root'}]);

    return ptx;
}

monaco.languages.register({id: 'ptx'});
monaco.languages.setMonarchTokensProvider('ptx', definition());

export {};
