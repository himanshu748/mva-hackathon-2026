import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from annotation_cache import validate_batch, validate_cache, write_manifest
spec=importlib.util.spec_from_file_location('annotate',Path(__file__).resolve().parents[1]/'scripts/04_annotate_all.py')
annotate=importlib.util.module_from_spec(spec);spec.loader.exec_module(annotate)

class AnnotationTests(unittest.TestCase):
    def test_response_coverage_rejects_missing_duplicate_and_foreign(self):
        expected=['synthetic-a','synthetic-b']
        for actual in [['synthetic-a'],['synthetic-a','synthetic-a'],['synthetic-a','synthetic-c']]:
            with self.subTest(actual=actual),self.assertRaises(ValueError):
                validate_batch([{'input':x} for x in actual],expected)
        validate_batch([{'input':x} for x in reversed(expected)],expected)
    def test_network_failure_is_fatal(self):
        with patch.object(annotate.urllib.request,'urlopen',side_effect=OSError('synthetic outage')):
            with self.assertRaises(OSError):annotate.fetch_batch(['synthetic-a'],attempts=1)
    def test_driver_failure_is_fatal_and_no_manifest_written(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'out').mkdir();(root/'out/coding_pass.tsv').write_text('1\t1\tA\tG\t0/1\t10,10\t20\n')
            with patch.object(annotate,'ROOT',root),patch.object(sys,'argv',['annotate']),patch.object(annotate,'fetch_batch',side_effect=OSError('outage')):
                with self.assertRaises(RuntimeError):annotate.main()
            self.assertFalse((root/'out/annotation_manifest.json').exists())
    def test_manifest_detects_changed_input_response_and_missing_batch(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'out/vep_parts').mkdir(parents=True)
            src=root/'out/coding_pass.tsv';src.write_text('1\t1\tA\tG\t0/1\t10,10\t20\n')
            p=root/'out/vep_parts/b0000.json';record={'input':'1 1 . A G . . .','assembly_name':'GRCh38'}
            p.write_text(json.dumps([record]));write_manifest(root,{'origin':'synthetic-test'});validate_cache(root)
            src.write_text('1\t1\tA\tG\t1/1\t0,20\t20\n')
            with self.assertRaises(ValueError):validate_cache(root)
            src.write_text('1\t1\tA\tG\t0/1\t10,10\t20\n')
            record['new_annotation']='changed';p.write_text(json.dumps([record]))
            with self.assertRaises(ValueError):validate_cache(root)
            p.unlink()
            with self.assertRaises(ValueError):validate_cache(root)

if __name__=='__main__':unittest.main()
