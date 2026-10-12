"""Offline syntax, local documentation links, and example delivery-policy checks."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys instead of silently overwriting them."""


def unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise yaml.constructor.ConstructorError(
                'mapping', node.start_mark, f'duplicate key: {key}', key_node.start_mark
            )
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def validate(root):
    errors = []
    manifests = {}
    yaml_paths = sorted(root.glob('manifests/**/*.yaml'))
    yaml_paths += sorted(root.glob('.github/workflows/*.yml'))
    for path in yaml_paths:
        relative = str(path.relative_to(root))
        try:
            documents = list(yaml.load_all(path.read_text(), Loader=UniqueKeyLoader))
            if relative.startswith('manifests/'):
                for document in documents:
                    if not isinstance(document, dict) or not all(
                        document.get(key) for key in ('apiVersion', 'kind', 'metadata')
                    ) or not document['metadata'].get('name'):
                        raise ValueError('resource needs apiVersion, kind and metadata.name')
                manifests[relative] = documents[0]
        except (yaml.YAMLError, ValueError, TypeError, AttributeError) as error:
            errors.append(f'{relative}: {error}')

    for path in sorted(root.rglob('*.md')):
        text = path.read_text()
        if '\ue200' in text or '\ue201' in text or '\ue202' in text:
            errors.append(f'{path.relative_to(root)}: unsupported chat rendering markup')
        # Inline Markdown destinations outside fenced code. External URLs and
        # heading fragments are intentionally excluded; this is an offline check.
        text = re.sub(r'(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$', '', text)
        for target in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text):
            parts = urlsplit(target.strip('<>'))
            if parts.scheme or parts.netloc or not parts.path:
                continue
            destination = (path.parent / unquote(parts.path)).resolve()
            if not destination.is_relative_to(root.resolve()) or not destination.exists():
                errors.append(f'{path.relative_to(root)}: missing local link {target}')

    for environment in ('stage', 'production'):
        key = f'manifests/applications/example-{environment}.yaml'
        app = manifests.get(key)
        if not app:
            errors.append(f'{key}: required example Application missing or invalid')
            continue
        policy = app.get('spec', {}).get('syncPolicy', {})
        if environment == 'production' and 'automated' in policy:
            errors.append(f'{key}: production must retain manual synchronization')
        if environment == 'stage':
            auto = policy.get('automated') or {}
            if auto.get('prune') is not True or auto.get('selfHeal') is not True:
                errors.append(f'{key}: stage must enable pruning and self-healing')
        source = app.get('spec', {}).get('source', {})
        # The external repository path maps to the sample directory under manifests/.
        source_path = source.get('path', '')
        if source_path != f'environments/{environment}' or not (root / 'manifests' / source_path).is_dir():
            errors.append(f'{key}: source path must map to the documented environment example')

    return errors


if __name__ == '__main__':
    errors = validate(ROOT)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    print('PASS: YAML syntax, unique keys, local Markdown links and stage/production policy')
