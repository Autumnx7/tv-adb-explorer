import argparse
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('explore',ROOT/'skills/tv-adb-explorer/scripts/explore.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def decision(action='RIGHT',page='home',focus='推荐'):
    return dict(page_id=page,title='首页',focus=focus,status='explore',block_reason='',action=action,safe_to_activate=True,reason='inspect next item',frontier=['settings via RIGHT OK'],observations=['default focus visible'])

class FakeDevice:
    actions=[]
    version='versionName=1.0'
    def __init__(self,*a): pass
    def ready(self): return True
    def start(self,activity,restart=False): self.actions.append(('start',activity,restart))
    def text(self,*a,**kw):
        if a[:3]==('shell','pm','path'): return 'package:/data/app/base.apk'
        if 'resolve-activity' in a: return 'com.example.tv/.Main'
        if a[:3]==('shell','dumpsys','package'): return self.version
        self.actions.append(a)
        return 'test-device'
    def capture(self,d):
        d.mkdir(parents=True,exist_ok=True)
        (d/'screen.png').write_bytes(b'\x89PNG\r\n\x1a\nmock')
        return {'window':'mCurrentFocus=Window{123 u0 com.example.tv/.Main}', 'xml':'<hierarchy><node focused="true" text="推荐"/></hierarchy>','xml_error':'','sha256':'fake'}

class Tests(unittest.TestCase):
    def args(self,p):
        return argparse.Namespace(adb='adb',serial='USB123',package='com.example.tv',out=str(p),activity=None,codex='codex',hours=1,max_steps=2,max_idle=80,min_free_gb=.001,planner_timeout=10)
    def execute(self,args,decisions):
        with patch.object(m,'Device',FakeDevice), patch.object(m,'process',return_value=b'--ignore-user-config --ephemeral --output-schema --image'), patch.object(m,'decide',side_effect=decisions), patch.object(m.time,'sleep'):
            return m.run(args)
    def test_run_resume_and_offline_report(self):
        with tempfile.TemporaryDirectory(prefix='tv test ') as tmp:
            p=Path(tmp); args=self.args(p)
            self.assertEqual(self.execute(args,[decision(),decision('DONE',page='settings')]),0)
            s=json.loads((p/'state.json').read_text()); self.assertEqual(len(s['history']),2)
            self.assertTrue((p/'index.html').is_file()); self.assertFalse((p/'run.lock').exists())
            self.execute(args,[decision('DONE')])
            s=json.loads((p/'state.json').read_text()); self.assertEqual(len(s['history']),3)
            self.assertTrue(s['history'][-1]['resumed'])
            self.assertEqual(s['history'][-1]['step'],3)
    def test_blocked_does_not_end_other_branches(self):
        d=decision('OK'); d.update(status='blocked',block_reason='login required')
        with tempfile.TemporaryDirectory() as tmp:
            self.execute(self.args(tmp),[d,decision('DONE',page='other')])
            s=json.loads((Path(tmp)/'state.json').read_text())
            self.assertEqual(s['history'][0]['action'],'BACK')
            self.assertEqual(len(s['history']),2)
    def test_unsafe_ok_and_unknown_foreground(self):
        c={'window':'mCurrentFocus=Window{123 u0 com.example.tv/.Main}','xml':'<hierarchy/>'}
        self.assertEqual(m.guard(decision('OK',focus='购买'),c,'com.example.tv')[0],'BACK')
        self.assertEqual(m.guard(decision('OK'),c,'com.example.tv')[0],'OK')
        c['window']=''; self.assertEqual(m.guard(decision('OK'),c,'com.example.tv')[0],'BACK')
    def test_schema_rejects_invented_action(self):
        with self.assertRaises(ValueError): m.validate_decision(decision('shell rm'))
        d=decision(); d['safe_to_activate']='true'
        with self.assertRaises(ValueError): m.validate_decision(d)
    def test_failure_budget_preserves_partial(self):
        with tempfile.TemporaryDirectory() as tmp:
            args=self.args(tmp); args.max_steps=5
            self.assertEqual(self.execute(args,[decision(),RuntimeError('quota'),RuntimeError('quota'),RuntimeError('quota')]),2)
            s=json.loads((Path(tmp)/'state.json').read_text()); self.assertEqual(len(s['history']),1)
            self.assertIn('infrastructure_error',s['status']); self.assertTrue((Path(tmp)/'REPORT.md').exists())
    def test_stop_and_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); (p/'STOP').touch()
            self.execute(self.args(tmp),[])
            self.assertEqual(json.loads((p/'state.json').read_text())['status'],'stopped_by_user')
            (p/'run.lock').write_text('123')
            with self.assertRaises(RuntimeError): self.execute(self.args(tmp),[])
    def test_version_change_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            args=self.args(tmp); self.execute(args,[decision('DONE')])
            with patch.object(FakeDevice,'version','versionName=2.0'):
                with self.assertRaises(RuntimeError): self.execute(args,[])
    def test_action_checkpoint_not_replayed(self):
        with tempfile.TemporaryDirectory() as tmp:
            args=self.args(tmp); self.execute(args,[decision('DONE')])
            p=Path(tmp)/'state.json'; s=json.loads(p.read_text()); s['pending_action']={'action':'OK','step':1}; m.dump(p,s)
            self.execute(args,[decision('DONE')]); s=json.loads(p.read_text())
            self.assertEqual(s['uncertain_action']['action'],'OK'); self.assertIsNone(s['pending_action'])
    def test_binary_capture_xml_missing(self):
        dev=m.Device('adb','serial')
        def fake_call(*a,**kw):
            if a[0]=='exec-out': return b'\x89PNG\r\n\x1a\n\x00\xff'
            if 'uiautomator' in a: raise RuntimeError('unsupported')
            return b'mCurrentFocus=Window{123 u0 com.example.tv/.Main}'
        with tempfile.TemporaryDirectory() as tmp, patch.object(dev,'call',side_effect=fake_call):
            c=dev.capture(Path(tmp))
            self.assertIn('unsupported',c['xml_error']); self.assertEqual(c['xml'],'')
            self.assertTrue((Path(tmp)/'screen.png').read_bytes().endswith(b'\x00\xff'))
    def test_foreign_activity_and_network_serial_rejected(self):
        with self.assertRaises(ValueError): m.resolve_activity(FakeDevice(),'com.example.tv','com.foreign/.Main')
        with tempfile.TemporaryDirectory() as tmp:
            args=self.args(tmp); args.serial='192.168.1.2:5555'
            with self.assertRaises(ValueError): self.execute(args,[])

if __name__=='__main__': unittest.main()
