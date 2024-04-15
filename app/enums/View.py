from enum import Enum

View = Enum('View', [
    'Normal',
    'Compact',
    'Markdown', # TODO Not implemented: A view for copying to Typora
        # Just timecodes and categories, prefixed with '- [ ] '
])
