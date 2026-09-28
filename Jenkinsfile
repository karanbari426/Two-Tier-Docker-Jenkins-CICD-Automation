pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    docker compose build
                '''
            }
        }

        stage('Stop Existing Containers') {
            steps {
                sh '''
                    docker compose down || true
                '''
            }
        }

        stage('Deploy Containers') {
            steps {
                sh '''
                    docker compose up -d
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    sleep 15

                    docker compose ps

                    curl -f http://localhost:5000/health
                '''
            }
        }
    }

    post {

        success {
            echo 'Hospital Staff Management deployed successfully!'
        }

        failure {
            echo 'Deployment failed. Check Jenkins logs.'
        }
    }
}
