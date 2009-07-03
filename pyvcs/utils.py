from difflib import unified_diff

from pyvcs.exceptions import FileDoesNotExist

def generate_unified_diff(repository, changed_files, commit1, commit2):
    diffs = []
    for file_name in changed_files:
        try:
            file1 = repository.file_contents(file_name, commit1)
        except FileDoesNotExist:
            file1 = ''
        try:
            file2 = repository.file_contents(file_name, commit2)
        except FileDoesNotExist:
            file2 = ''
        diffs.append(unified_diff(
            file1.splitlines(), file2.splitlines(), fromfile=file_name,
            tofile=file_name, fromfiledate=commit1, tofiledate=commit2
        ))
    return '\n'.join('\n'.join(map(lambda s: s.rstrip('\n'), diff)) for diff in diffs)
