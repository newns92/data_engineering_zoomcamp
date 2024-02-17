# dbt Deployment

## Deployment
- **Deployment** is the process of running the models that we created in our *development* (DEV) environment in a *production* (PROD) environment
    - All of the development, testing, and documentation occured in the *development* environment
    - We'd also want *all* of the data in PROD environment, while we can work with limited datasets in DEV to prototype and test
- Doing Development and then deployment *later* on allows us to continue building models and testing them *without affecting our production environment*
- A deployment environment will normally have a different schema in our data warehouse, and *ideally* a different user
- A development-to-deployment workflow will look something like: 
    1. Develop in a user branch in parallel with the main branch
    2. Open a pull request (PR) to merge into the main branch 
    3. Merge the user branch to the main branch
    4. Run the new models in the production environment using the *main* branch 
    5. Schedule the models

## Running a dbt Project in Production
- dbt Cloud includes a **scheduler** wherein we can create jobs to run in *production*
- A *single* job can run *multiple* commands (`dbt run`, `dbt test`, `dbt seed`, `dbt build`, etc.)
- Jobs can be triggered manually or on a schedule (like a CRON schedule)
- Each job will keep a **log** of the runs over time
    - Each **run** will have the logs for each *command*
    - i.e. Jobs provide us with a lot of metadata to view after they run
- A job could also generate documentation, which could also be viewed under the run information
- If dbt Source Freshness was run, those results can also be viewed at the end of a job
    - See https://docs.getdbt.com/docs/deploy/source-freshness
- To create our job:
    - At the top of the Cloud IDE, go to "Deploy" and then "Environments"
        - You should see a DEV environment that was created from the initial dbt Cloud setup
        - Create a new PROD environment named "Production", with a type of "Deployment", then with the latest dbt version
        - Then add your *target* BigQuery dataset (i.e., the dataset *within* the project ID to create/deploy to), and name it something like "prod"
    - Then go to "Deploy" and then "Jobs"
        - Create a *new* job named "dbt build Nightly", with a description of "This is where the data hits production."
        - Make sure this job is in the "Production" environment
        - Under "Execution settings", check off to create documentation *and* source freshness
        - Under "Schedule", create a trigger that runs at 12 UTC with a timing of "hours of the day", and uncheck Saturday and Sunday for the days of the week
        - Under "Advanced settings", make sure that the job inherits the dbt version from the environment, and leave the target as "default" to mean that our target is the PROD database that we defined when creating the environment
            - See more at:
                - https://docs.getdbt.com/docs/quickstarts/overview#create-a-new-job
                - https://discourse.getdbt.com/t/best-practices-for-cicd-deployment/618
        - Click "Save" near the top of the page to save the job
- Now, note that we can also run our job on an ad-hoc basis with the "Run now" button
- Also note that we can trigger the job via an API, and dbt Cloud gives you all the information needed to do so
    - For example, you could use an orchestrator like Mage to create a pipeline that loads fresh data into GCS and *then* triggers a `dbt run` via this API
- In a job run's information, we can see how it was triggered, a GitHub commit SHA, the environment it was run in, the run duration, and the actions (with sub-steps) that were taken, any generated documentation, and the sources
    - It also has a tab for **artifacts** generated by the job run (like model files and various JSON files) that can be downloaded
- Then, to make sure our documentation is hosted on dbt Cloud, click "Explore" of the top of the page
    - Then, click "Settings" for the project at the top right-hand side of the page
    - Click "Edit" for the project details
    - Then, under "Artifacts", make sure that select the "dbt build Nightly" job as the one to generate the documentation *and* to check the source freshness
    - Then "Save" the job
- Then, the "Documentation" tab at the top of the dbt Cloud page will show us our project's documentation (including a lineage graph) *in production*


## What is Continuous Integration?
- **Continuous Integration (CI)** is the software engineering practice of regularly merging *development* branches into a *central* repository, after which *automated* builds and tests are run
- The **goal** is to **reduce adding bugs to the production code and maintain a more stable project** as well as **automating as much as possible**
- dbt allows us to enable CI on pull requests (PR's)
    - CI is enabled via **webhooks** from GitHub or GitLab
    - When a PR is ready to be merged, a webhook is received in dbt Cloud that will **enqueue** a new run of the specified job
    - The run of the CI job will be against a *temporary* schema
    - *No PR will be able to be merged unless the run has been completed successfully*
- To create a CI job in dbt Cloud, go "Deploy" and then "Jobs"
    - Then, under "Create job", select "Continuous integration job"
        - *If you see the "This feature is only available for dbt repositories connected through dbt Cloud's native integration with Github, Gitlab, or Azure DevOps" message*:
            - Follow instructions at https://docs.getdbt.com/docs/cloud/git/connect-github
            - Make sure your project's Clone strategy for your repo is `github_app`
    - Name the new job "CI Checks", add a description like "Avoid breaking production", make sure the environenment is "Production", and make sure "Triggered by pull requests" is switched *on*
        - Note that the pull request trigger will create a new schema, `dtb_cloud_pr`
        - This will be dropped after the PR is closed/merged
    - Keep the default `dbt build --select state:modified+` command
        - This will run anything that has been modified, and their children
    - Make sure to compare everything against "Production", and keep all other settings as their default values
- Now, any PR we make from the dbt Cloud IDE should trigger this job
    - It will compare to other job runs (like our scheduled ones) and identify what has changed