# *arr Queue Cleaner

This is a fork of [sonarr-radarr-queue-cleaner](https://github.com/ben16w/sonarr-radarr-queue-cleaner) by [ben16w](https://github.com/ben16w). The fork adds a GitHub Action to build a Docker image and push it to GitHub Packages. The Docker image is available at [here](https://github.com/users/lusoris/packages/container/package/arr-queue-cleaner). 

Install the Docker image with the following command, replacing the environment variables with your own values:

    docker run -d \
        --name arr-queue-cleaner \
        -e LIDARR_RUN_SCRIPT='True' \
        -e LIDARR_URL='http://lidarr:7878' \
        -e LIDARR_API_KEY='123456' \
        -e RADARR_RUN_SCRIPT='True' \
        -e RADARR_URL='http://radarr:7878' \
        -e RADARR_API_KEY='123456' \
        -e READARR_RUN_SCRIPT='True' \
        -e READARR_URL='http://readarr:7878' \
        -e READARR_API_KEY='123456' \
        -e SONARR_RUN_SCRIPT='True' \
        -e SONARR_URL='http://sonarr:8989' \
        -e SONARR_API_KEY='123456' \
        -e WHISPARR_RUN_SCRIPT='True' \
        -e WHISPARR_URL='http://whisparr:7878' \
        -e WHISPARR_API_KEY='123456' \
        -e API_TIMEOUT='3600' \
        ghcr.io/lusoris/arr-queue-cleaner:latest

You can also use the following `docker-compose.yml` file:

    version: '3.7'
    services:
      arr-queue-cleaner:
        image: ghcr.io/lusoris/arr-queue-cleaner:latest
        container_name: arr-queue-cleaner
        environment:
          # LIDARR
          - LIDARR_RUN_SCRIPT=True
          - LIDARR_URL='http://lidarr:7878'
          - LIDARR_API_KEY=123456
          # RADARR
          - RADARR_RUN_SCRIPT=True
          - RADARR_URL='http://radarr:7878'
          - RADARR_API_KEY=123456
          # READARR
          - READARR_RUN_SCRIPT=True
          - READARR_URL='http://readarr:7878'
          - READARR_API_KEY=123456
          # SONARR
          - SONARR_RUN_SCRIPT=True
          - SONARR_URL='http://sonarr:8989'
          - SONARR_API_KEY=123456
          # WHISPARR
          - WHISPARR_RUN_SCRIPT=True
          - WHISPARR_URL='http://whisparr:7878'
          - WHISPARR_API_KEY=123456
          #GENERAL
          - API_TIMEOUT=3600
        restart: always