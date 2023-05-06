## Local setup for Postgres
- In the `week4/` directory, spin up the Postgres database via `docker-compose up -d`
    - If needed, create a new server: `taxi_data` by right-clicking on "Servers" and hit "Register" --> "Server"
    - Need to specify the host address in the "Connection" tab, which should be `pgdatabase`, port is `5432`, username and password is `root`
- In the `zoom` Conda environment, run `pip install dbt-bigquery` and `pip install dbt-postgres`
    - Installing `dbt-bigquery` or `dbt-postgres` will install `dbt-core` and any other dependencies
- Create a `dbt_local/` directory, `cd` into it, and run `dbt init`
- Name the project `taxi_data` and select the Postgres option of a database
- `profiles.yml` should be updated with stock **outputs**.
- Update these outputs to be the correct root username, password, host, port, etc. for the Postgres database
- Copy/Cut the `profiles.yml` file into the `taxi_data` directory that `dbt init` created
- Run `dbt debug`
    - This will check the database connection and display any errors or warnings that it finds