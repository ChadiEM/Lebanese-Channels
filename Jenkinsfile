pipeline {
    agent none
    triggers {
        githubPush()
    }
    stages {
        stage('Checkout') {
            agent any
            steps {
                checkout scm
            }
        }
        stage('Deploy Locally') {
            agent any
            when {
                branch 'master'
            }
            steps {
                sh 'rsync -Crv ./ /opt/channels/ --delete'
                sh 'sudo /bin/systemctl restart channels.service'
            }
        }
    }
}
