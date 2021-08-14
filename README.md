# Twitter Raw Ingest Script

This repo contains the source code for a containerized python script that will ingest tweets on some topic into dynamoDB using Twitter's filtered stream API

## Env variables
- TOPIC: Topic to ingest tweets for. A rule will be created in the filter API to ingest tweets of that subject

#### Image location - public.ecr.aws/t9y1m9m9/twitter_ingest:latest

#### Continuous Integration - This script is deployed to ECR on pushed to main via github actions