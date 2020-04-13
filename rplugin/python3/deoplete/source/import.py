import os
import re
import typing

from deoplete.base.source import Base
from deoplete.util import expand, Nvim, UserContext, Candidates, debug


class Source(Base):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = 'import'
        self.mark = '[I]'
        self.rank = 500
        self.input_pattern = '^import.+from.+'

    def gather_candidates(self, context: UserContext) -> Candidates:
        try:
            webpack_resolve = self.vim.eval('b:webpack_resolve')
            roots = webpack_resolve['modules']
        except Exception:
            return []

        input_str = re.sub(r'.*[\'"]', '', context['input'])
        input_str_parts = re.split('/', input_str)

        dirs = []
        files = []

        if input_str_parts[0] == '.':
            if input_str.startswith('./'):
                self.gather_candidates_for_dir(os.path.dirname(context['bufpath']), dirs, files)
                return dirs + files
            else:
                return []

        for root in roots:
            paths = [
                os.path.join(root, '/'.join(input_str_parts[:i]))
                for i in range(1, len(input_str_parts))
            ]

            if paths:
                longest_path = paths[-1]

                if (
                    os.path.isfile(longest_path)
                    or os.path.isfile(longest_path + '.js')
                    or os.path.isfile(longest_path + '.jsx')
                ):
                    return []

            existing_dirs = [d for d in paths if os.path.isdir(d)]

            if existing_dirs != paths and not input_str_parts[-1]:
                continue

            if existing_dirs:
                current_dir = existing_dirs[-1]
            elif len(input_str_parts) > 1:
                continue
            else:
                current_dir = root

            self.gather_candidates_for_dir(current_dir, dirs, files)

        return dirs + files

    @staticmethod
    def gather_candidates_for_dir(current_dir, dirs, files):
        try:
            for item in sorted(os.listdir(current_dir), key=str.lower):
                if item[0] != '.':
                    is_dir = os.path.isdir(os.path.join(current_dir, item))
                    item = re.sub(r'.jsx?$', '', item)
                    if is_dir:
                        dirs.append({'word': item, 'abbr': item + '/'})
                    else:
                        files.append({'word': item})
        except PermissionError:
            pass
