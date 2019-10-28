Documentation for automated donor registration through aws resources

stuff needed:
1. requirements.txt
2. setup.sh
3. db_record_create.py
4. test_file_2.csv -can be renamed
5. postgresql database setup within rds
6. aws account with user permissions for lambda, s3, rds, vpc

instructions:
1. check contents of python file to see if the formats of records have changed
2. create ec2 linux machine instance, if it doesn't have virtualenv, install it
3. scp test_file, requirements, setup and db_record_create.py to ec2 instance
4. run bash setup.sh to create zip file (zip file must be created within an linux enviroment due to some issues with psycopg2 module that i dont know since im just a random intern)
5. scp zip file back to local machine
6. upload zip file to lambda, set trigger to specified s3 bucket, set timeout to something other than 5 seconds
7. somehow give lambda function access to both aws resources and the internet(couldn't figure this part out)

8. basically followed this guide https://gist.github.com/reggi/dc5f2620b7b4f515e68e46255ac042a7
9. used 3 of the default subnets instead of creating 3 new subnets
10. had same issue as a few of the commenters where it would work properly but couldn't access database through sql client