#!/usr/bin/bash
# first and foremost - input checking!
# check if correct number of arguments were entered:
if [ "$#" -ne 1 ]; then
	echo "Usage: ${0} [test|prod]" >&2
	exit 1
fi
# check input spelling:
machine=$1
if [ $machine != "test" ] && [ $machine != "prod" ]; then
	echo -e "Enter the input correctly: test or prod\nUsage: ${0} [test|prod]" >&2
	exit 1
fi

echo "deploying to ${machine} machine..."
# making sure final-project directory exists and copying to it all the files from the git repository:
rsync -zrv --delete /var/lib/jenkins/workspace/attendance-project/ $machine:/home/ec2-user/final-project/
# connecting to the input machine and running multiple commands:
ssh -T $machine << EOF
	cd final-project/
	bash docker-clean.sh
	export DOTENV=${env}
	docker-compose up -d
	sleep 10
EOF
# if deploying to test move tests directory to test machine and run tests:
if [ $machine == "test" ]; then
	ssh -T test <<-EOF
	cd final-project/tests/
	bash test-back.sh
	bash test-front.sh
	EOF
fi