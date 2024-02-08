 ## Mage Next Steps
 - We have now learned how to use Mage, what orchestration is (*dependency management*, facilitated through *automation*), how to implement ETL pipelines in Mage, how to schedule such pipelines on a cadence
 - In the homework, we built a pipeline from scratch that loaded compressed CSV data, transformed it, and loaded it to Postgres and GCS Buckets (along with BiqQuery), all the while implementing engineering best practices such as code reusage and assertions
 - To learn even more about Mage, we can use their documentation: http://docs.mage.ai
    - They also provide guides: https://docs.mage.ai/guides
    - We can also join their Slack: https://www.mage.ai/chat
- Some more advanced Mage concepts to consider tackling next are:
    - Deployment
        - This would be hosting a pipeline somewhere, having them run on a server on a scheduled cadence so that we're not running everything locally on our machines
            - See the optional Deployment video for the course, starting with https://www.youtube.com/watch?v=zAwAX5sxqsg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb
    - Pipelines
        - We've worked with batch pipelines, but Mage has other options such as streaming and data integration
        - These could be explored for other personal projects or for production-ready systems
    - Alerting
        - For example, one could hook up Slack to Mage so that one could recieve alerts about pipelines failures or other statuses for their DAGS
    - Triggers and Scheduling
        - There is additional scheduling functionality outside of the simple example from this course
- For some general data engineering advice (in terms of continuing to grow and improve as one):
    - Continue with and complete the Zoomcamp
    - Personal Projects
        - Fun as well as helpful to learn and to add to your portfolio in order to show people your passions and/or what you're interested
    - Books and online resources/texts
        - Forums
        - Slack/Discord communities
    - Engaging with the Data Engineering community
        - Meetups
        - Conferences
        - LinkedIn
        - Blogs