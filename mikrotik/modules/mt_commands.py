#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Michail Topaloudis
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Executes list of commands. Optionally outputs the results to file."""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.yama.strings import writefile
import ansible.module_utils.network.mikrotik.mikrotik as mikrotik

PATH = '/etc/ansible/config'


def main():
    messages = []
    result = []
    changed = 0
    failed = 0
    unreachable = 1
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True, type='str'),
            port=dict(required=False, type='int', default=22),
            username=dict(required=False, default='admin'),
            password=dict(required=False, type='str'),
            pkeyfile=dict(required=False, type='str'),
            branchfile=dict(required=False, type='str',
                            default='mikrotik/branch.json'),
            db_conffile=dict(required=False, type='str',
                             default='mikrotik/mongodb.json'),
            commands=dict(required=True, type='list'),
            raw=dict(required=False, type='bool', default=False),
            output=dict(required=False, type='str')
        )
    )

    router = mikrotik.Router(
        module.params['host'],
        module.params['port'],
        module.params['username'],
        module.params['password'],
        module.params['pkeyfile'],
        PATH + '/' + module.params['branchfile'],
        PATH + '/' + module.params['db_conffile']
    )

    if router.connect():
        unreachable = 0
        result = router.commands(module.params['commands'],
                                 module.params['raw'])

        if result and module.params['output']:
            if not writefile(module.params['output'], result):
                messages.append('Unable to create Output File.')

    if router.errc():
        failed = 1

    router.disconnect()
    messages.append(router.errors())
    module.exit_json(changed=changed, unreachable=unreachable, failed=failed,
                     result=result, msg=' '.join(messages))


if __name__ == '__main__':
    main()