# cicdsp500

CI/CD example for a Python script that calculates an inversion on the S&amp;P 500 index.

Webapp to provide the user with the estimated quantity of euros given last 2 years of historical data and the DCA amounts to invest.

**DISCLAIMER**:
This is NOT a buy or investment recommendation, just a development and CI/CD practice.

Aron Galdon Gines 2024

## Steps followed

1. Created the app in a `venv` for development.

2. Created `Dockerfile`.

3. Created `docker-componse.yml`. Now we are able to launch the app with `docker compose up`.

4. Followed this tutorial: [Get started with GitHub Actions in Docker docs](https://docs.docker.com/build/ci/github-actions/#get-started-with-github-actions).

    4.1 In *Secrets and variables > Actions*, created a new repository secret named `DOCKERHUB_USERNAME`.

    4.2 Generate an access token in DockerHub and then add it as another secret named `DOCKERHUB_TOKEN`.

    4.3 Create `workflows/docker-image.yml` using GitHub guidance. Now, each commit will update the imagen in DockerHub.

5. Requirements splitted in two: one for testing and the other for production. So for deployment `prod.txt` will be used, and for development and testing stages `test.txt` will be the proper one to use running `pip install -r requirements/test.txt` in our `venv`.

6. Added some unit tests in `test_sp500.py`
