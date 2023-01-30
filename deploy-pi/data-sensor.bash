#!/bin/bash

set -e

BASE=$(eval /bin/pwd)
params=$(<parameters.txt)

aws cloudformation deploy \
  --stack-name my-timestream-database \
  --template-file "$BASE/timestream-database.yaml" \
  --parameters $params \
  --capabilities CAPABILITY_NAMED_IAM \
  --no-fail-on-empty-changeset