#!/usr/bin/env bash
## Setup
CWD="$(pwd)"

cd $CWD

## Run MinIE server
git clone https://github.com/uma-pi1/minie.git
cd minie
mvn clean compile
mvn assembly:assembly -DdescriptorId=jar-with-dependencies
mvn exec:java -Dexec.mainClass="uk.ac.ucl.cs.mr.Main" &

cd $CWD

## Run other components

