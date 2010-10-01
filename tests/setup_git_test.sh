#!/bin/sh

#NOTE: this script depends on git being installed and having access to the /tmp directory...

echo Setting up the directory for the git repository
mkdir /tmp/pyvcs-test
mkdir /tmp/pyvcs-test/git-test

cd /tmp/pyvcs-test/git-test
git init
echo this is a test README file for a mock project > README
echo print 'hello, world!' > hello_world.py
git add README
git add hello_world.py
git commit -m "initial add of files to repo"
echo this is a new line added to the README >> README
git commit -a -m "slight change to the README"

