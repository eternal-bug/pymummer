import unittest
import os
import filecmp
import fastaq
from pymummer import nucmer

modules_dir = os.path.dirname(os.path.abspath(nucmer.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data')


class TestRunner(unittest.TestCase):
    def test_nucmer_command(self):
        '''test _nucmer_command'''
        tests = [
            [nucmer.Runner('ref', 'qry', 'outfile'), 'nucmer -p pre ref qry'],
            [nucmer.Runner('ref', 'qry', 'outfile', breaklen=42), 'nucmer -p pre -b 42 ref qry'],
            [nucmer.Runner('ref', 'qry', 'outfile', maxmatch=True), 'nucmer -p pre --maxmatch ref qry']
        ]

        for l in tests:
            self.assertEqual(l[0]._nucmer_command('ref', 'qry', 'pre'), l[1])


    def test_delta_filter_command(self):
        '''test _delta_filter_command'''
        tests = [
            [nucmer.Runner('ref', 'qry', 'outfile'), 'delta-filter infile > outfile'],
            [nucmer.Runner('ref', 'qry', 'outfile', min_id=42), 'delta-filter -i 42 infile > outfile'],
            [nucmer.Runner('ref', 'qry', 'outfile', min_length=43), 'delta-filter -l 43 infile > outfile'],
        ]

        for l in tests:
            self.assertEqual(l[0]._delta_filter_command('infile', 'outfile'), l[1])
        

    def test_show_coords_command(self):
        '''test _show_coords_command'''
        tests = [
            [nucmer.Runner('ref', 'qry', 'outfile', coords_header=False), 'show-coords -dTlro -H infile > outfile'],
            [nucmer.Runner('ref', 'qry', 'outfile'), 'show-coords -dTlro infile > outfile']
        ]

        for l in tests:
            self.assertEqual(l[0]._show_coords_command('infile', 'outfile'), l[1])


    def test_write_script(self):
       '''test _write_script'''
       tmp_script = 'tmp.script.sh'
       r = nucmer.Runner('ref', 'qry', 'outfile')
       r._write_script(tmp_script, 'ref', 'qry', 'outfile')
       expected = os.path.join(data_dir, 'nucmer_test_write_script.sh')
       self.assertTrue(filecmp.cmp(expected, tmp_script, shallow=False))
       os.unlink(tmp_script)


    def test_run_nucmer(self):
        '''test run_nucmer'''
        qry = os.path.join(data_dir, 'nucmer_test_qry.fa')
        ref = os.path.join(data_dir, 'nucmer_test_ref.fa')
        tmp_out = 'tmp.nucmer.out'
        runner = nucmer.Runner(ref, qry, tmp_out, coords_header=False)
        runner.run()
        expected = os.path.join(data_dir, 'nucmer_test_out.coords')
        self.assertTrue(filecmp.cmp(tmp_out, expected, shallow=False))
        os.unlink(tmp_out)
        

