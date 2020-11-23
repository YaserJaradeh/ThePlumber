#!/usr/bin/env bash
## Setup
CWD="$(pwd)"

## Run MinIE server
cd minie
mvn exec:java -Dexec.mainClass="uk.ac.ucl.cs.mr.Main" &

cd $CWD

## Run other components

