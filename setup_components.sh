#!/usr/bin/env bash
## Setup
CWD="$(pwd)"

## Pull and Build MinIE server
git clone https://github.com/uma-pi1/minie.git
cd minie
mvn clean compile
mvn assembly:assembly -DdescriptorId=jar-with-dependencies

cd $CWD

## Build other components

