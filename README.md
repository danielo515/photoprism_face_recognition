# Photoprism face-recognition project

This project aims to add face recognition to photoprism from outside of it.

This is meant to run as a sidecar process/container, and it will connect to the photoprism database and API and will use the existing data there
to perform face recognition.

## Why use the api instead of just pick the files

The reason we use the API is because photoprism already has created smaller versions of each photo, which is nice for faster face recognition processing.
We consider that quering the API for the existing thumbnails is the best and more resliant way to get them because:
- Thumbnails are stored on a very complex folder structure
- We have extra information about them as the photo they come from etc

## State of the project

This project is just a proof of concept from now, and should not be used by anyone but me 😄.
