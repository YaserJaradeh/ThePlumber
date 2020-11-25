#!/usr/bin/env bash
## Setup
CWD="$(pwd)"

## Pull and Build MinIE server
gdown https://drive.google.com/uc?id=1jA8Uw7uV94_sPTxvpGyZzgXyDssBjbOj
unzip minie.zip
rm minie.zip
cd minie
mvn clean compile
mvn assembly:assembly -DdescriptorId=jar-with-dependencies

cd $CWD

## Build other components

