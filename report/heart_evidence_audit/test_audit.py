import unittest,tempfile,gzip,csv
from pathlib import Path
from audit import read_author,direction
class AuditTests(unittest.TestCase):
 def fixture(self,rows):
  t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);p=Path(t.name)/'a.csv.gz'
  with gzip.open(p,'wt') as f:
   w=csv.writer(f);w.writerow(['gene','log2FC','pvalue','padj']);w.writerows(rows)
  return p
 def test_author_statistics_preserved(self):
  r=read_author(self.fixture([['A','1.3','0.03','0.4'],['B','-2','NA','NA']]));self.assertEqual(r[0]['padj'],'0.4');self.assertEqual(r[1]['pvalue'],'NA')
 def test_duplicate_gene_rejected(self):
  with self.assertRaises(ValueError):read_author(self.fixture([['A',1,.1,.2],['A',2,.1,.2]]))
 def test_invalid_probability_rejected(self):
  with self.assertRaises(ValueError):read_author(self.fixture([['A',1,.1,1.2]]))
 def test_nonfinite_effect_rejected(self):
  with self.assertRaises(ValueError):read_author(self.fixture([['A','inf',.1,.2]]))
 def test_directions(self):self.assertEqual([direction(x) for x in [-1,0,1]],['lower','zero','higher'])
if __name__=='__main__':unittest.main()
