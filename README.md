AWS Wizard
======
Amazaon made easy [aws-wizard.com](https://aws-wizard.com) 



####Done
- domain bucket creation
- cert request
- cloudfront creation
- routing to cloudfront
- route to s3 before routing to cloudfront
- router config (print records)
- router interactive config (interactive check via "host -t ns DOMAIN") //whois updates faster than host-t-ns
- cert interactive config (wait for validation)

####Todo
- clean up command
- update command
- provide feedback on records set propagation status (route53.change-resource-record-sets.output ChangeInfo.Status?)
- multiregional setup support
- handle domains purchased on amazon: add ns records via script?


####Dev Notes
#####Requirements
python 3.7+

#Scripts
- Run py script locally `./run.sh`
- Run landing locally `./run.sh`
- Update landing page in prod `./publish-landing.sh`
- Publish script to test Pypi (watch out versions) `./publish-test-pypi.sh`