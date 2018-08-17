#!/bin/bash

dx describe "$1" --json | jq -r '{id: .id, name: .name, user: .createdBy.user, job: .createdBy.job }'
