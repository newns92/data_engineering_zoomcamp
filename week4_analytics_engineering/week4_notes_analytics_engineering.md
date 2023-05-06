# Analytics Engineering

## What is Analytics Engineering
- To answer this, we have look back at recent developments in the data domain:
    1. Massive parallel processing (MPP) databases
        - We've seen how cloud data warehouses (BigQuery, RedShift, Snowflake, etc.) have lowered the cost of storage and computing
    2. Data-pipelines-as-a-service
        - And how tools like Stich and Fivetran simplify the ETL process
    3. SQL-first
    4. Version control systems
        - Tools like Looker introducing version control systems to the data workflow        
    5. Self-service analytics
        - Different BI tools
    6. Data governance
        - Changed the way the data teams worked and also the way stakeholder consumed that data
- All of the above left gaps in the roles we had in a data team
- Different roles in a traditional data team
    - Data Engineer: prepares and maintain the infrastructure the data team needs
    - Data Analyst: uses data to answer questions and solve problems    
    - Analytics Engineer: introduces good software engineering practices to the efforts of data analysts and data scientists
        - Data analysts and data scientists are not meant to be writing SWE-level code
        - Data engineers don't have the training in how the data is actually going to be used by business users
        - This role fills this gap
- Tooling for analytics engineers
    - Data loading (Fivetran, Stitch, etc.)
    - Data storing (Cloud (Snowflake, BigQuery, RedShift) or on-prem data warehouses, etc.)
    - Data modeling (dbt, Dataform, etc.)
    - Data presentation (BI tools like Google Data Studio, Looker, Mode, Tableau, etc.)


## Data Modelling Concepts
- **ETL vs ELT**
    - ETL
        - Takes longer to implement    
        - But results in slightly more stable and compliant data analysis
        - Higher storage and compute costs
    - ELT
        - Waiting to transform data until it's in the data warehouse
        - Faster and more flexible data analysis
        - Lower cost and lower maintenance (thanks to cloud solutions)
- **Kimball’s Dimensional Modeling**
    - *Objective*:
        - Deliver data that's understandable to the business users
        - Along with delivering fast query performance
    - *Approach*:
        - Prioritize understandibility and query performance over non-redundant data (3NF)
    - Other dimensional modeling approaches: Bill Inmon, Data vault
- **Elements of Dimensional Modeling (*Star* Schema)**
    - **Fact** tables:
        - Measurements, metrics (facts)
        - Corresponds to a business *process*
        - "Verbs" (like Sales or Orders)
    - **Dimension** tables
        - Corresponds to a business *entity*
        - Provides context to a business process (fact)
        - "Nouns" (like Customer or Products)
- **Architecture of Dimensional Modeling**
    - **Staging** layer:
        - Contains the raw data
        - Not meant to be exposed to everyone, just to those who know how to use it
    - **Processing** layer:
        - From raw data to data models
        - Focuses in efficiency
        - Ensuring standards
    - **Presentation** layer:
        - Final presentation of the data
        - Exposure to business stakeholder(s)


## What is dbt?
- ***dbt (Data Build Tool)*** **= a transformation tool that allows anyone that knows SQL to deploy analytics code following software engineering best practices (like modularity, portability, CI/CD, and documentation)**
- After doing the Extracting and the Loading into a data warehouse (ELT), we need to transform this data to present to stakeholders and to be able to perform analysis
- dbt will help us Transform the data in the data warehouse as well as introduce good software engineering practices by defining a **development workflow**
- We do this by adding a **modeling layer** where we transform raw data into a derived model that's persisted back into the data warehouse
- Each **dbt model** is:
    - A `*.sql` file (dbt models    )
    - A `Select~ statement (*no* DDL (Data Definition Language = defines the structure/schema of the database) or DML(Data Manipulation Language, helps deal with managing and manipulating data in the database))
    - A file that dbt will compile and run in our data warehouse
        - It will compile the DDL/DML and push it to our data warehouse
- Again, we turn data warehouse *tables into models* by transforming them from raw data into derived dbt models, which then persist back to the data warehouse
- Can use dbt in 2 ways:
    - **dbt Core**: Open-source project that allows the data transformation
        - The essence of dbt that builds and runs a **dbt project** (SQL and YAML files)
        - Includes SQL compilation logic, **macros**, and database adapters
        - Includes a CLI to run dbt commands *locally*
        - Open-source and free to use
    - **dbt Cloud**: SaaS application to develop and manage dbt projects
        - Web-based IDE to develop, run, and test a dbt project
        - Jobs orchestration
        - Logging and alerting
        - Integrated documentation
        - Free for individuals (one developer seat)
- dbt in BigQuery
    - Development using cloud IDE
    - *No* local installation of dbt core
- dbt in Postgres
    - Cannot connect a local database to dbt Cloud
    - Development using a local IDE of your choice
    - Local installation of dbt core connecting to the Postgres database
    - Running dbt models through the CLI
- In the end, we'll have the taxi trip data loaded into our database/GCS Bucket (along with a CSV file for the taxi zones) as raw data
- We will transform this raw data into transformed data via dbt withing our BigQuery (or Postgres) data warehouse
- In the end, we'll be able to expose this transformed data to a dashboard tool


## Starting/Creating a dbt Project
- dbt provides a starter project with all basic files and folders (https://github.com/dbt-labs/dbt-starter-project)
- A project includes the following files:
    - `dbt_project.yml`: a file used to configure the dbt project
        - If using dbt locally, make sure the profile here matches the one setup during installation in `~/.dbt/profiles.yml`
    - `*.yml` files under folders `models/data/macros`: documentation files
    - CSV files in the `data/` folder: these will be our sources, files described above
    - Files inside `folder/` models: The SQL files contain the scripts to run our models, this will cover staging, core, and a datamarts models
        - At the end, these models will follow a specific structure (https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/taxi_rides_ny/README.md)
- In `dbt_project.yml`, you're able to define global settings (like project name, profile file, models, global variables), along with different configurations
- There are 2 ways to use it:
    1. With the CLI
        - After having installed dbt locally and setup the `profiles.yml` files, in a terminal, run `dbt init` *within the path that we want to start the project in order to clone the starter project*
    2. With dbt Cloud
        - After having set up dbt Cloud credentials (repo and data warehouse), start the project from the web-based IDE


## Development of dbt Models
- ***Anatomy of a dbt model***
    - There's the dbt model itself (a SQL file)
        - Several **materilization** strategies (Table, View, incremental, ephemeral, etc.)
    - dbt takes this and returns compiled code and also runs the compiled code in the data warehouse
- ***The FROM clause of a dbt model***
    - **Sources**: the data loaded to our data warehouse that we use as sources for our models
        - The configuration is defined in the YAML files in the `models/` directory
        - Used with the **source macro** that will resolve the name to the correct schema, plus build the dependencies automatically
        - Source freshness can be defined and tested
    - **Seeds**: CSV files stored in our repository under the `seed/` directory
        - Benefits of version controlling
        - Equivalent to a `copy` command
        - Recommended for data that doesn't change frequently
        - Run via `dbt seed -s file_name`
    - **Ref**: a macro to reference the underlying tables and views that were building the data warehouse
        - Run the same code in any environment, and it will resolve the correct schema for you
        - Dependencies are build automatically
- ***Macros***
    - Use **control structures** (e.g., IF statements and FOR loops) in SQL
    - Use environment variables in your dbt project for production deployments
    - Operate on the results of one query to generate another query
    - Abstract snippets of SQL into reusable macros (anagolous to *functions* in most programming languages)
- ***Packages***
    - Like *libraries* in other programming languages
    - Standalone dbt projects, with models and macros that tackle a specific problem area
    - By adding a package to a project, the package's models and macros will be part of your project
    - Imported in the `packages.yml` file and imported via `dbt deps`
    - A list of useful dbt packages: https://hub.getdbt.com/
- **Variables**
    - Useful for defining values that should be used across the project
    - With a macro, dbt allows us to provide data to models for compilation
    - To use a variables, use the `{{ var('...')}}` function
    - Variables can be defined in 2 ways: In the `dbt_project.yml` file OR on the command line


## Testing and Documenting dbt Models
- **Tests**
    - Assumptions we make about our data
    - These are essentially a `SELECT` SQL query
    - These assumptions get compiled to SQL that returns the amount of failing records
    - Tests are defined *on the column* in a YAML file
    - dbt provides basic tests to check if column values are: unique, not null, accepted values, a foreign key to another table
    - You can create custom tests as queries
- **Documentation**
    - dbt provides a way to generate documentation for a dbt project and render it as a website
    - Documentation for a dbt project includes:
        - Information about your project:
            - Model code (both from the SQL file and the compiled code)
            - Model dependencies
            - Sources
            - Auto-generated DAG from the ref and sources macros
            - Descriptions (from the YAML file) and test
        - Information about your data warehouse (`information_schema`)
            - Column names and data types
            - Table stats like size and rows
    - dbt docs can also be hosted in dbt Cloud


## Deployment of a dbt Project
- **Deployment** = process of running the models created in a DEV environment into a PROD environment
- Deployment and later deployment allows us to continue building models and testing them without affecting PROD
- A deployment environment will normally have a different schema in our data warehouse, and ideally a different user
- A development-deployment workflow is something like:
    1. Develop in a user branch
    2. Open a PR to merge into the main branch
    3. Merge the branch to the main branch
    4. Run the new models in PROD
    5. Schedule the models
- DEV environment (Test, document, and develop) --> Deployemnt (Version control and CI/CD) --> PROD environment
- *Running a dbt project in production*:
    - dbt Cloud includes a scheduler to create jobs to run in production
    - A single job can contain mulitple commands
    - Jobs can be triggered manually or on a schedule
    - Each job keeps a log of runs over time
    - Each run has logs for each command
    - A job can also generate documentation that can be viewed under the run information
    - If dbt source freshness was run, the results can also be viewed at the end of a job
- *What is **Continuous Integration (CI)?***
    - **CI is the practice of regularly merging development branches into a central repository, after which automated builds and tests are run**
    - The goal is to reduce adding bugs to production code and maintain a more stable project
    - dbt allows us to enable CI on PR's
    - It's enabled via webhooks from GitHub or GitLab
    - When a PR is ready to be merged, a webhook is recieved in dbt Cloud that will enqueue a new run of the specific job
    - The run of the CI job will be against a temporary schema
    - No PR will be able to be merged unless the run has been completed successfully


## Visualising the Transformed Data
- We will do this with Google Data Studio and with Metabase
