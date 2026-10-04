import json, os, subprocess
from pathlib import Path

def run(role, variables, tags=None, success=True):
 cmd=['ansible-playbook','-i','localhost,','-c','local',str(Path(__file__).with_name('test.yml')),'-e',json.dumps(variables)]
 if tags: cmd+=['--tags',tags]
 result=subprocess.run(cmd,capture_output=True,text=True)
 if (result.returncode==0)!=success: raise AssertionError(result.stdout+result.stderr)
 print(role,tags or 'all','PASS',flush=True)
run('unattended-upgrades',{'unattended_upgrades_enabled':False,'unattended_upgrades_package_whitelist':['openssl'],'unattended_upgrades_upgrade_timer_on_calendar':'*-*-* 03:00:00'})
cfg=subprocess.check_output(['apt-config','dump'],text=True)
assert 'APT::Periodic::Unattended-Upgrade "0"' in cfg
assert 'Unattended-Upgrade::Package-Whitelist:: "openssl"' in cfg
owned=Path('/etc/systemd/system/apt-daily-upgrade.timer.d/override.conf')
assert owned.exists()
run('unattended-upgrades',{'unattended_upgrades_enabled':True})
assert not owned.exists()
cfg=subprocess.check_output(['apt-config','dump'],text=True)
assert 'APT::Periodic::Unattended-Upgrade "1"' in cfg
owned.write_text('# external timer override\n')
run('unattended-upgrades',{})
assert owned.read_text()=='# external timer override\n'
owned.unlink()
print('All regression checks passed.',flush=True)
