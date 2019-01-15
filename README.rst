Django Ethereum (gnosis-py)
############################

.. class:: no-web no-pdf

|travis| |coveralls| |python| |django| |pipy|

Gnosis-py includes a set of libraries to work with Gnosis projects.
Currently `Gnosis Safe <https://github.com/gnosis/safe-contracts>`_ is supported.

Quick start
-----------

Just run ``pip install gnosis-py`` or add it to your **requirements.txt**

Ethereum django utils
---------------------
Now ``django-eth`` is part of this package, you can find it under ``gnosis.eth.django``
You can find a set of helpers for working with Ethereum using Django and Django Rest framework.

It includes:

- Basic serializers (signature, transaction)
- Serializer fields (Ethereum address field, hexadecimal field)
- Model fields (Ethereum address, Ethereum big integer field)
- Utils for testing

Contributors
------------
- Denís Graña (denis@gnosis.pm)
- Giacomo Licari (giacomo.licari@gnosis.pm)
- Uxío Fuentefría (uxio@gnosis.pm)

.. |travis| image:: https://travis-ci.org/gnosis/gnosis-py.svg?branch=master
    :target: https://travis-ci.org/gnosis/gnosis-py
    :alt: Travis CI build

.. |coveralls| image:: https://coveralls.io/repos/github/gnosis/gnosis-py/badge.svg?branch=master
    :target: https://coveralls.io/github/gnosis/gnosis-py?branch=master
    :alt: Coveralls

.. |python| image:: https://img.shields.io/badge/Python-3.6-blue.svg
    :alt: Python 3.6

.. |django| image:: https://img.shields.io/badge/Django-2-blue.svg
    :alt: Django 2

.. |pipy| image:: https://badge.fury.io/py/gnosis-py.svg
    :target: https://badge.fury.io/py/gnosis-py
    :alt: Pypi package
