Bandit configuration generator
==============================

This tool aims at generating custom Bandit configuration files meant to be used
by OpenStack projects. It should:

* make it easier for project maintainers to write their bandit configuration
  files;
* make it easy to update the configuration files by just re-generating them
  when new versions of Bandit are released, or should the configuration format
  be modified;
* make sure the Bandit configuration files are correct.


Usage
-----

It is pretty straightforward::

    $ bandit-conf-generator \
        --disable try_except_pass \
        --out bandit.yaml
        oslo.messaging \
        ~/openstack/bandit/bandit/config/bandit.yaml
