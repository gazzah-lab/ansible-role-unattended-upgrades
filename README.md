# unattended_upgrades

Standalone Ansible role for Debian. Licensed under MIT. Authors: Aymen Gazzah.

## Installation

```yaml
roles:
  - name: gazzah.unattended_upgrades
    src: https://github.com/gazzah-lab/ansible-role-unattended-upgrades.git
    version: v1.0.0
```

Run `ansible-galaxy role install -r requirements.yml`. Requires ansible-core >= 2.15, collected facts, and root privilege. Runtime smoke tests use Debian 13; other releases declared in metadata require validation in your environment.

## Inventory configuration

Store variables in `group_vars/all/gazzah.unattended_upgrades.yml`, override in group or host directories. These filenames are conventions: Ansible loads the variable contents.

```yaml
unattended_upgrades_manage_systemd: false
unattended_upgrades_origins_patterns:
- origin=Debian,codename=${distro_codename}-security,label=Debian-Security
```

The `manage_service` / `manage_systemd` false values above are for container tests; use their default true on real machines.

Set `unattended_upgrades_enabled: false` to disable periodic unattended upgrades. Origins, blacklist, whitelist, reporting and reboot options are explicit inventory variables. Packaged 20/50 configuration files are restored to their shipped references and registered with ucf; custom settings live in 52unattended-upgrades-gazzah. Review this takeover before adopting the role on existing systems. Nonempty OnCalendar variables create timer drop-ins; resetting them removes only marked drop-ins. Empty proxy/general variables leave those files unmanaged. Keep scheduling choices in group_vars/host_vars. No full vendor service unit is replaced.

## Variables

| Variable | Default |
| --- | --- |
| `unattended_upgrades_packages` | `['unattended-upgrades', 'apt-listchanges']` |
| `unattended_upgrades_apt_install_state` | `present` |
| `unattended_upgrades_apt_update_cache` | `True` |
| `unattended_upgrades_apt_cache_valid_time` | `3600` |
| `unattended_upgrades_config_dir` | `/etc/apt/apt.conf.d` |
| `unattended_upgrades_managed_marker` | `ANSIBLE MANAGED - gazzah.unattended_upgrades` |
| `unattended_upgrades_enabled` | `True` |
| `unattended_upgrades_periodic` | `{}` |
| `unattended_upgrades_config_filename` | `52unattended-upgrades-gazzah` |
| `unattended_upgrades_origins_patterns` | `['origin=Debian,codename=${distro_codename},label=Debian', 'origin=Debian,codename=${distro_codename},label=Debian-Security', 'origin=Debian,codename=${distro_codename}-security,label=Debian-Security']` |
| `unattended_upgrades_package_blacklist` | `[]` |
| `unattended_upgrades_package_whitelist` | `[]` |
| `unattended_upgrades_package_whitelist_strict` | `False` |
| `unattended_upgrades_mail_recipients` | `[]` |
| `unattended_upgrades_mail_sender` | `` |
| `unattended_upgrades_mail_report` | `on-change` |
| `unattended_upgrades_minimal_steps` | `True` |
| `unattended_upgrades_autofix_interrupted_dpkg` | `True` |
| `unattended_upgrades_dpkg_options` | `[]` |
| `unattended_upgrades_remove_unused_kernel_packages` | `True` |
| `unattended_upgrades_remove_new_unused_dependencies` | `True` |
| `unattended_upgrades_remove_unused_dependencies` | `False` |
| `unattended_upgrades_automatic_reboot` | `False` |
| `unattended_upgrades_automatic_reboot_with_users` | `True` |
| `unattended_upgrades_automatic_reboot_time` | `02:00` |
| `unattended_upgrades_syslog_enable` | `False` |
| `unattended_upgrades_syslog_facility` | `daemon` |
| `unattended_upgrades_verbose` | `False` |
| `unattended_upgrades_debug` | `False` |
| `unattended_upgrades_apt_proxy` | `` |
| `unattended_upgrades_apt_general` | `{}` |
| `unattended_upgrades_remove_files` | `[]` |
| `unattended_upgrades_update_timer_on_calendar` | `` |
| `unattended_upgrades_update_timer_randomized_delay_sec` | `15m` |
| `unattended_upgrades_update_timer_persistent` | `True` |
| `unattended_upgrades_upgrade_timer_on_calendar` | `` |
| `unattended_upgrades_upgrade_timer_randomized_delay_sec` | `15m` |
| `unattended_upgrades_upgrade_timer_persistent` | `True` |
| `unattended_upgrades_manage_systemd` | `True` |

See [defaults/main.yml](defaults/main.yml) for comments and [tests/test.yml](tests/test.yml) for a runnable playbook.

## Testing

```sh
python -m pip install 'ansible-core>=2.20,<2.21' ansible-lint yamllint
yamllint -c .yamllint .
ansible-lint --offline -c .ansible-lint .
```

CI also runs the example twice in a disposable Debian 13 container and checks the second run has no changes. No automatic package upgrade, reboot, or cron job execution is triggered by these tests.
