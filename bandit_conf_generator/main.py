# Copyright 2015 Red Hat Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import argparse
import sys

import yaml

PROG_NAME = 'bandit_conf_generator'


def write_config_file(config, f):
    f.write('# Generated using %s\n' % PROG_NAME)

    # Start by writing profiles
    f.write(yaml.dump({'profiles': config['profiles']},
                      default_flow_style=False))

    # Write the rest of the config.
    del config['profiles']
    for key in config:
        f.write('\n')
        f.write(yaml.dump({key: config[key]}, default_flow_style=False))


def clean_profile(config, project_name):
    """Removes all profiles from CONFIG except the 'All' one.

    This default profile is then renamed after the project that needs this
    bandit configuration.
    """
    config['profiles'] = {project_name: config['profiles']['All']}
    return config


def disable_tests(config, disabled_tests):
    """Disable tests specified using DISABLED_TESTS from CONFIG."""
    for profile in config['profiles']:
        includes = [x for x in config['profiles'][profile]['include']
                    if x not in disabled_tests]
        config['profiles'][profile]['include'] = includes

    for test in disabled_tests:
        try:
            del config[test]
        except KeyError:  # nosec
            # This error is perfectly OK: some tests do not have extra
            # configuration.
            pass

    return config


def parse_args():
    parser = argparse.ArgumentParser(description='Generate a bandit config')
    parser.add_argument('--disable', action='append', default=[],
                        help='tests to disable')
    parser.add_argument('--out', default='bandit.yaml',
                        help='output file')
    parser.add_argument('project_name',
                        help='name of the project for which a configuration '
                             'must be generated')
    parser.add_argument('default_config_file',
                        help='base configuration file')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    with open(args.default_config_file) as f:
        config = yaml.safe_load(f.read())

    config = clean_profile(config, args.project_name)
    config = disable_tests(config, args.disable)

    with open(args.out, 'w') as f:
        write_config_file(config, f)


if __name__ == '__main__':
    sys.exit(main())
