#!/usr/bin/env python3
"""Check complete parallel dispatch and ownership; no live runtime queries."""
import argparse
import json
import re
import sys
from pathlib import Path

STATES = {'ready', 'running', 'blocked', 'done', 'cancelled'}
IDS = {'SET1', 'SET2', 'SET3'}


def validate(plan, workspace):
    errors = []
    root = Path(workspace).resolve()
    scopes, keys = [], {}

    def scope_path(value, owner):
        if not isinstance(value, str) or not value.strip():
            errors.append(f'{owner}: empty or invalid path')
            return None
        if any(c in value for c in '*?[]'):
            errors.append(f'{owner}: scopes must be literal paths: {value}')
            return None
        normalized = value.replace('\\', '/')
        if normalized.startswith('/') or re.match(r'^[A-Za-z]:', normalized):
            errors.append(f'{owner}: path must be workspace-relative: {value}')
            return None
        if ':' in normalized or any(ord(c) < 32 for c in normalized):
            errors.append(f'{owner}: invalid portable path: {value}')
            return None
        components = normalized.split('/')
        if any(part not in ('', '.', '..') and (part.endswith('.') or part.endswith(' ')) for part in components):
            errors.append(f'{owner}: ambiguous Windows path suffix: {value}')
            return None
        resolved = (root / normalized).resolve()
        if not resolved.is_relative_to(root):
            errors.append(f'{owner}: path escapes workspace: {value}')
            return None
        return tuple(part.casefold() for part in resolved.parts)

    def overlaps(a, b):
        return a[:len(b)] == b or b[:len(a)] == a

    def string_list(record, name, owner, allow_empty=False):
        value = record.get(name)
        if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value) or (not value and not allow_empty):
            errors.append(f'{owner}: {name} must be a list of nonempty strings')
            return []
        return value

    def reserve(owner, values):
        current = []
        for value in values:
            path = scope_path(value, owner)
            if path is None:
                continue
            for other, other_path, original in scopes:
                if other != owner and overlaps(path, other_path):
                    errors.append(f'write overlap: {owner} {value} / {other} {original}')
            scopes.append((owner, path, value))
            current.append(path)
        return current

    if not isinstance(plan, dict):
        return ['plan must be a JSON object']
    if type(plan.get('version')) is not int or plan['version'] != 2:
        errors.append('version must be 2; legacy scheduling plans must be revised')
    if plan.get('execution_mode') != 'parallel-only':
        errors.append('execution_mode must be parallel-only; no sequential fallback')
    reviewers = plan.get('concurrent_reviewers')
    if type(reviewers) is not int or not 0 <= reviewers <= 3:
        errors.append('concurrent_reviewers must be an integer from 0 to 3')
        reviewers = 0
    capacity = plan.get('capacity_total')
    required = 13 + reviewers
    if type(capacity) is not int or capacity < required:
        errors.append(f'capacity_total must provide at least {required} total agents; full parallel dispatch unavailable')
    for field in ('run_id', 'objective'):
        if not isinstance(plan.get(field), str) or not plan[field].strip():
            errors.append(f'{field} must be nonempty')
    reserve('chief', string_list(plan, 'chief_write_scope', 'chief', allow_empty=True))
    if isinstance(plan.get('run_id'), str) and plan['run_id'].strip():
        reserve('chief', [f"work/three-set/{plan['run_id']}/plan.json"])
    records = plan.get('sets')
    if not isinstance(records, list) or len(records) != 3:
        return errors + ['sets must contain exactly SET1, SET2, SET3']
    by_id, dependencies = {}, {}
    for entry in records:
        if not isinstance(entry, dict):
            errors.append('each set must be an object')
            continue
        ident = entry.get('id')
        if not isinstance(ident, str) or ident not in IDS or ident in by_id:
            errors.append('invalid or duplicate set ID')
            continue
        by_id[ident] = entry
        if not isinstance(entry.get('objective'), str) or not entry['objective'].strip():
            errors.append(f'{ident}: objective must be nonempty')
        state = entry.get('state')
        if not isinstance(state, str) or state not in STATES:
            errors.append(f'{ident}: invalid state')
        owned = reserve(ident, string_list(entry, 'write_scope', ident))
        for output in string_list(entry, 'outputs', ident):
            path = scope_path(output, ident)
            if path and not any(path[:len(scope)] == scope for scope in owned):
                errors.append(f'{ident}: output is outside owned scope: {output}')
        string_list(entry, 'checks', ident)
        for key in string_list(entry, 'work_keys', ident):
            canonical = ' '.join(key.casefold().split())
            if canonical in keys:
                errors.append(f'duplicate work key: {key} ({keys[canonical]} / {ident})')
            keys[canonical] = ident
        deps = string_list(entry, 'depends_on', ident, allow_empty=True)
        if deps:
            errors.append(f'{ident}: SET completion dependencies serialize teams; redesign for parallel launch')
        dependencies[ident] = deps
        for dep in deps:
            if dep not in IDS or dep == ident:
                errors.append(f'{ident}: invalid dependency {dep}')
    if set(by_id) != IDS:
        errors.append('sets must contain exactly SET1, SET2, SET3')
    visiting, visited = set(), set()

    def visit(ident):
        if ident in visiting:
            errors.append(f'dependency cycle involving {ident}')
            return
        if ident in visited:
            return
        visiting.add(ident)
        for dep in dependencies.get(ident, []):
            if dep in by_id:
                visit(dep)
        visiting.remove(ident)
        visited.add(ident)

    for ident in by_id:
        visit(ident)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--workspace', type=Path, required=True)
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding='utf-8-sig'))
        errors = validate(plan, args.workspace)
    except (OSError, ValueError, RuntimeError) as exc:
        errors = [str(exc)]
    print(json.dumps({'valid': not errors, 'errors': errors,
                      'scope': 'declared SET ownership; semantic overlap and actual edits need agent review'}, ensure_ascii=False, indent=2))
    return 2 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
