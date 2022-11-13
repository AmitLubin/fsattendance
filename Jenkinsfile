pipeline {
    environment {
        registry = "natibloy/attendance-project"
		registryCredential = 'docker-hub'
		dockerImage = ''
    }
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                script {
                    dockerImage = docker.build("$registry:${env.BUILD_ID}", "./backend")
                }
            }
        }
        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', registryCredential) {
                        dockerImage.push()
                    }
                }
            }
        }
		stage('Clean') {
			steps {
				sh "docker rmi $registry:$BUILD_NUMBER"
			}
		}
		stage('Test') {
			steps {
                withCredentials([file(credentialsId: 'dotenv', variable: 'env')]) {
                    sh """cd /var/lib/jenkins/workspace/attendance-project/
                        bash deploy.sh test""".trim()
                }
			}
		}
		stage('Prod') {
			steps {
                withCredentials([file(credentialsId: 'dotenv', variable: 'env')]) {
                    sh """cd /var/lib/jenkins/workspace/attendance-project/
                        bash deploy.sh prod""".trim()
                }
			}
		}	
    }
}