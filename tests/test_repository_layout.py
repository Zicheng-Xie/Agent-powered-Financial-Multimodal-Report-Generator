"""Offline checks for the reorganized package and its independent modules."""
import ast
from contextlib import redirect_stdout
import importlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
LEGACY_ROOTS = {'Backend', 'data_analysis_agent', 'utils', 'pocketflow', 'config'}


def module_exists(name):
    path = ROOT.joinpath(*name.split('.'))
    return path.with_suffix('.py').is_file() or (path / '__init__.py').is_file()


class RepositoryLayoutTests(unittest.TestCase):
    def test_python_and_notebook_syntax(self):
        for path in ROOT.rglob('*.py'):
            if '.git' in path.parts or '__pycache__' in path.parts:
                continue
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                compile(path.read_bytes(), str(path), 'exec')
        notebook = json.loads((ROOT / 'notebooks/Scrape.ipynb').read_text(encoding='utf-8'))
        for i, cell in enumerate(notebook['cells']):
            if cell['cell_type'] == 'code':
                with self.subTest(cell=i):
                    compile(''.join(cell['source']), f'Scrape.ipynb:cell{i}', 'exec')

    def test_internal_module_references(self):
        for base in ('financial_reports', 'examples', 'scripts'):
            for path in (ROOT / base).rglob('*.py'):
                module = '.'.join(path.relative_to(ROOT).with_suffix('').parts)
                package = module.rsplit('.', 1)[0]
                tree = ast.parse(path.read_bytes())
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        if node.level:
                            name = importlib.util.resolve_name('.' * node.level + (node.module or ''), package)
                        else:
                            name = node.module or ''
                            self.assertNotIn(name.split('.')[0], LEGACY_ROOTS, (path, node.lineno, name))
                        if name.startswith(('financial_reports', 'scripts', 'examples')):
                            with self.subTest(path=str(path), line=node.lineno, module=name):
                                self.assertTrue(module_exists(name), 'Missing internal module: ' + name)
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            self.assertNotIn(alias.name.split('.')[0], LEGACY_ROOTS, (path, node.lineno, alias.name))
                            if alias.name.startswith(('financial_reports', 'scripts', 'examples')):
                                self.assertTrue(module_exists(alias.name), alias.name)

    def test_prompt_modules_import_without_providers(self):
        modules = (
            'financial_reports.templates.structure.prompt_companyorshare',
            'financial_reports.templates.structure.prompt_industry',
            'financial_reports.templates.structure.prompt_macro',
            'financial_reports.templates.content.content_companyorshare',
            'financial_reports.templates.content.content_industry',
            'financial_reports.templates.content.content_macro',
            'financial_reports.templates.analysis.prompts',
        )
        for name in modules:
            with self.subTest(module=name):
                with redirect_stdout(io.StringIO()):
                    module = importlib.import_module(name)
                prompts = [value for key, value in vars(module).items() if not key.startswith('__') and isinstance(value, str)]
                self.assertTrue(prompts, 'No prompt strings exported')
                self.assertTrue(all(value.strip() for value in prompts))

    def test_bundled_workflow_executes_successors(self):
        from financial_reports.vendor.pocketflow import Flow, Node

        class AddOne(Node):
            def prep(self, shared):
                return shared['value']

            def exec(self, value):
                return value + 1

            def post(self, shared, prep_res, exec_res):
                shared['value'] = exec_res

        first, second = AddOne(), AddOne()
        first >> second
        shared = {'value': 3}
        Flow(start=first).run(shared)
        self.assertEqual(shared['value'], 5)


if __name__ == '__main__':
    unittest.main()
